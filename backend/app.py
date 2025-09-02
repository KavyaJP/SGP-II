import os
import io
import time
import logging
import torch
import base64
from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
from diffusers import StableDiffusionPipeline
import peft

# --- 1. SETUP ---
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})
logging.basicConfig(level=logging.INFO)

# --- NEW: Define Output Paths at the project root ---
ROOT_DIR = os.path.join(os.path.dirname(__file__), "..")
OUTPUT_DIR = os.path.join(ROOT_DIR, "output")
DOWNSCALED_DIR = os.path.join(OUTPUT_DIR, "downscaled")

# Define model paths
MODELS_DIR = os.path.join(ROOT_DIR, "models")
CHECKPOINTS_DIR = os.path.join(MODELS_DIR, "checkpoint")
LORAS_DIR = os.path.join(MODELS_DIR, "lora")

# Ensure all directories exist
for path in [CHECKPOINTS_DIR, LORAS_DIR, OUTPUT_DIR, DOWNSCALED_DIR]:
    if not os.path.exists(path):
        os.makedirs(path)
        logging.info(f"--- Created directory: {path}")

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
logging.info(f"--- Using device: {DEVICE} ---")

# Cache for loaded pipelines
MODEL_CACHE = {}


# --- 2. UTILITY & API ENDPOINTS (No changes here) ---
def get_model_files(directory):
    allowed_extensions = {".safetensors", ".ckpt", ".bin", ".pt"}
    try:
        files = os.listdir(directory)
        return [
            f
            for f in files
            if any(f.lower().endswith(ext) for ext in allowed_extensions)
        ]
    except FileNotFoundError:
        return []


@app.route("/api/checkpoints", methods=["GET"])
def get_checkpoints():
    checkpoints = get_model_files(CHECKPOINTS_DIR)
    return jsonify({"models": checkpoints})


@app.route("/api/loras", methods=["GET"])
def get_loras():
    loras = get_model_files(LORAS_DIR)
    return jsonify({"models": loras})


# --- 3. GENERATION LOGIC ---
@app.route("/api/generate", methods=["POST"])
def generate():
    start_time = time.time()
    data = request.get_json()

    prompt = data.get("prompt")
    negative_prompt = data.get("negativePrompt")
    checkpoint_file = data.get("checkpointModel")
    lora_file = data.get("loraModel")

    if not prompt or not checkpoint_file:
        return jsonify({"error": "Prompt and Checkpoint are required."}), 400

    pipe = None
    try:
        # Load pipeline from cache or disk
        if checkpoint_file in MODEL_CACHE:
            pipe = MODEL_CACHE[checkpoint_file]
        else:
            checkpoint_path = os.path.join(CHECKPOINTS_DIR, checkpoint_file)
            pipe = StableDiffusionPipeline.from_single_file(
                checkpoint_path, torch_dtype=torch.float32, safety_checker=None
            )
            pipe.to(DEVICE)
            MODEL_CACHE[checkpoint_file] = pipe

        # Apply LoRA if selected
        if lora_file and lora_file != "":
            lora_path = os.path.join(LORAS_DIR, lora_file)
            pipe.load_lora_weights(lora_path)

        # Generate the 512x512 image
        logging.info("--- Generating 512x512 image... ---")
        image = pipe(
            prompt, negative_prompt=negative_prompt, num_inference_steps=25
        ).images[0]
        logging.info("--- Image generated successfully. ---")

        # --- NEW: SAVE THE IMAGES ---
        timestamp = int(time.time())
        filename = f"{timestamp}_{prompt[:20].replace(' ', '_')}.png"

        full_size_path = os.path.join(OUTPUT_DIR, filename)
        image.save(full_size_path)
        logging.info(f"--- Saved full-size image to: {full_size_path} ---")

        pixel_art_img = image.resize((16, 16), Image.Resampling.NEAREST)
        downscaled_path = os.path.join(DOWNSCALED_DIR, filename)
        pixel_art_img.save(downscaled_path)
        logging.info(f"--- Saved downscaled image to: {downscaled_path} ---")

        # --- FIX: Convert image to Base64 and send in JSON ---
        buffered = io.BytesIO()
        pixel_art_img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

        end_time = time.time()
        logging.info(
            f"--- Total generation time: {end_time - start_time:.2f} seconds ---"
        )

        return jsonify({"images": [f"data:image/png;base64,{img_str}"]})

    except Exception as e:
        logging.error(f"!!! An error occurred during generation: {e}")
        return jsonify({"error": str(e)}), 500

    finally:
        if lora_file and lora_file != "" and pipe is not None:
            pipe.unload_lora_weights()


# --- 4. RUN THE SERVER ---
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
