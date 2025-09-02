import os
import io
import base64
import torch
from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
from diffusers import StableDiffusionPipeline

# --- 1. CONFIGURATION & SETUP ---

# Define paths to the specific model subdirectories
MODELS_DIR = os.path.join(os.path.dirname(__file__), "..", "models")
CHECKPOINTS_DIR = os.path.join(MODELS_DIR, "checkpoint")
LORAS_DIR = os.path.join(MODELS_DIR, "lora")
print(f"--- Checkpoints directory: {CHECKPOINTS_DIR} ---")
print(f"--- LoRAs directory: {LORAS_DIR} ---")

# Ensure directories exist
for path in [CHECKPOINTS_DIR, LORAS_DIR]:
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"--- Created directory: {path} ---")

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
print(f"--- Using device: {DEVICE} ---")

# --- NEW: Pipeline Cache ---
# This dictionary will hold loaded checkpoint models to avoid reloading them on every request.
# Key: checkpoint filename, Value: loaded pipeline object
loaded_pipelines = {}


# --- 2. FLASK APP INITIALIZATION ---
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})


# --- 3. UTILITY FUNCTIONS ---
def get_model_files(directory):
    """Scans a directory for model files."""
    allowed_extensions = {".safetensors", ".ckpt", ".bin", ".pt"}
    try:
        files = os.listdir(directory)
        return [
            f
            for f in files
            if any(f.lower().endswith(ext) for ext in allowed_extensions)
        ]
    except FileNotFoundError:
        return []  # Return empty list if the directory doesn't exist yet


# --- 4. API ENDPOINTS ---


@app.route("/api/checkpoints", methods=["GET"])
def get_checkpoints():
    """Returns a list of available checkpoint model filenames."""
    checkpoints = get_model_files(CHECKPOINTS_DIR)
    print(f"--- Found checkpoints: {checkpoints} ---")
    return jsonify({"models": checkpoints})


@app.route("/api/loras", methods=["GET"])
def get_loras():
    """Returns a list of available LoRA model filenames."""
    loras = get_model_files(LORAS_DIR)
    print(f"--- Found LoRAs: {loras} ---")
    return jsonify({"models": loras})


@app.route("/api/generate", methods=["POST"])
def generate():
    """
    Handles image generation. Loads a checkpoint and optionally applies a LoRA.
    """
    data = request.get_json()
    prompt = data.get("prompt")
    negative_prompt = data.get("negativePrompt")
    checkpoint_file = data.get("checkpointModel")
    lora_file = data.get("loraModel")  # Can be None or empty

    if not prompt or not checkpoint_file:
        return jsonify({"error": "Prompt and Checkpoint Model are required."}), 400

    try:
        # --- DYNAMIC PIPELINE LOADING ---
        pipe = None
        if checkpoint_file in loaded_pipelines:
            print(f"--- Using cached pipeline for: {checkpoint_file} ---")
            pipe = loaded_pipelines[checkpoint_file]
        else:
            print(f"--- Loading new pipeline for: {checkpoint_file} ---")
            checkpoint_path = os.path.join(CHECKPOINTS_DIR, checkpoint_file)
            if not os.path.exists(checkpoint_path):
                return (
                    jsonify({"error": f"Checkpoint file not found: {checkpoint_file}"}),
                    404,
                )

            pipe = StableDiffusionPipeline.from_pretrained(
                checkpoint_path,
                torch_dtype=torch.float16 if DEVICE == "cuda" else torch.float32,
                local_files_only=True,  # Assumes model is fully downloaded
            )
            pipe = pipe.to(DEVICE)
            loaded_pipelines[checkpoint_file] = pipe  # Cache the loaded pipeline
            print(f"--- Pipeline for {checkpoint_file} loaded and cached. ---")

        # --- APPLY LORA (if selected) ---
        if lora_file:
            lora_path = os.path.join(LORAS_DIR, lora_file)
            if not os.path.exists(lora_path):
                return jsonify({"error": f"LoRA file not found: {lora_file}"}), 404
            print(f"--- Applying LoRA: {lora_file} ---")
            pipe.load_lora_weights(lora_path)

        # --- IMAGE GENERATION ---
        image = pipe(
            prompt,
            negative_prompt=negative_prompt,
            num_inference_steps=30,
            guidance_scale=7.5,
        ).images[0]
        print("--- Image generated successfully. ---")

    except Exception as e:
        print(f"An error occurred during image generation: {e}")
        return (
            jsonify(
                {"error": f"Generation failed. Check backend logs for details: {e}"}
            ),
            500,
        )
    finally:
        # --- UNLOAD LORA ---
        # Unload LoRA weights to ensure the base checkpoint is clean for the next request.
        if lora_file and "pipe" in locals() and pipe is not None:
            pipe.unload_lora_weights()
            print(f"--- Unloaded LoRA: {lora_file} ---")

    # --- DOWNSCALING & RESPONSE ---
    pixel_art_img = image.resize((16, 16), Image.Resampling.NEAREST)
    buffered = io.BytesIO()
    pixel_art_img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

    print("--- Request Complete ---")
    return jsonify({"images": [f"data:image/png;base64,{img_str}"]})


# --- 5. RUN THE SERVER ---
if __name__ == "__main__":
    app.run(debug=True, port=5000)
