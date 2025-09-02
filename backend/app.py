import io
import base64
import torch
from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
from diffusers import StableDiffusionPipeline

# --- 1. AI MODEL SETUP (This runs only once when the server starts) ---

# Define the base model from Hugging Face. v1.5 is a reliable choice.
# This model will be downloaded the first time you run the server.
BASE_MODEL_ID = "runwayml/stable-diffusion-v1-5"

# Check if a CUDA-enabled GPU is available and set the device
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
print(f"--- Using device: {DEVICE} ---")

# Load the base Stable Diffusion pipeline
# This pipeline will be kept in memory to avoid reloading on every request
print(f"--- Loading base model '{BASE_MODEL_ID}'... This may take a while. ---")
pipe = StableDiffusionPipeline.from_pretrained(
    BASE_MODEL_ID, torch_dtype=torch.float16 if DEVICE == "cuda" else torch.float32
)
pipe = pipe.to(DEVICE)
print("--- Base model loaded successfully. ---")


# --- 2. FLASK APP INITIALIZATION ---
app = Flask(__name__)
CORS(app, resources={r"/generate": {"origins": "http://localhost:5173"}})


# --- 3. IMAGE GENERATION & PROCESSING ---
def generate_initial_image(prompt, negative_prompt, lora_path):
    """
    This function now generates a REAL image using the pre-loaded pipeline
    and applies your LoRA model.
    """
    try:
        print("--- Generating 512x512 Image ---")
        print(f"Prompt: {prompt}")
        print(f"Applying LoRA: {lora_path}")

        # Load the LoRA weights onto the base model.
        # The `lora_path` comes from the frontend selection.
        pipe.load_lora_weights(lora_path)

        # Generate the image. This is the main inference step.
        # You can adjust parameters like `num_inference_steps` and `guidance_scale`.
        image = pipe(
            prompt,
            negative_prompt=negative_prompt,
            num_inference_steps=30,
            guidance_scale=7.5,
        ).images[
            0
        ]  # .images[0] gets the PIL Image

        print("--- Image generated successfully. ---")

        # Unload the LoRA weights so the next request starts fresh
        pipe.unload_lora_weights()

        return image

    except Exception as e:
        print(f"An error occurred during image generation: {e}")
        # Unload weights in case of an error to be safe
        pipe.unload_lora_weights()
        return None


def downscale_image(img, size=(16, 16)):
    """
    Downscales a single PIL Image object to a target size
    using Nearest Neighbor resampling. (No changes needed here)
    """
    try:
        resized_image = img.resize(size, Image.Resampling.NEAREST)
        print(f"Successfully downscaled image to {size[0]}x{size[1]}px.")
        return resized_image
    except Exception as e:
        print(f"Could not downscale image. Error: {e}")
        return None


# --- 4. API ENDPOINT (Minor changes) ---


@app.route("/generate", methods=["POST"])
def generate():
    """
    The main API endpoint. Receives data, calls the generation and downscaling functions.
    """
    data = request.get_json()
    prompt = data.get("prompt")
    negative_prompt = data.get("negativePrompt")

    # This now represents the FILENAME of your LoRA model
    lora_model_file = data.get("checkpointModel")

    if not prompt or not lora_model_file:
        return jsonify({"error": "Prompt and Checkpoint Model are required."}), 400

    # Construct the full path to the LoRA file
    # We assume a 'loras' folder exists inside the 'backend' directory.
    full_lora_path = f"./loras/{lora_model_file}"

    initial_img = generate_initial_image(prompt, negative_prompt, full_lora_path)
    if initial_img is None:
        return (
            jsonify({"error": "Failed to generate initial image. Check backend logs."}),
            500,
        )

    pixel_art_img = downscale_image(initial_img)
    if pixel_art_img is None:
        return jsonify({"error": "Failed to downscale image."}), 500

    buffered = io.BytesIO()
    pixel_art_img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

    print("--- Request Complete ---")
    return jsonify({"images": [f"data:image/png;base64,{img_str}"]})


# --- 5. RUN THE SERVER ---
if __name__ == "__main__":
    app.run(debug=True, port=5000)
