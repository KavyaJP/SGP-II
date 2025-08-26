import os
import io
import base64
from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image

# --- Flask App Initialization ---
app = Flask(__name__)
# Enable CORS to allow your React frontend to communicate with this server
CORS(app, resources={r"/generate": {"origins": "http://localhost:5173"}})


# --- Image Generation & Processing ---


def generate_initial_image(prompt, negative_prompt, model_checkpoint):
    """
    !!! PLACEHOLDER FUNCTION !!!
    This is where you should put your actual Stable Diffusion/Lora model inference code.

    - Load your specified `model_checkpoint`.
    - Use the `prompt` and `negative_prompt` to generate an image.
    - The function should return a 512x512 PIL Image object.

    For now, this function just creates a simple placeholder image.
    """
    print("--- Generating 512x512 Image (Placeholder) ---")
    print(f"Prompt: {prompt}")
    print(f"Negative Prompt: {negative_prompt}")
    print(f"Model: {model_checkpoint}")

    # Placeholder: Create a simple gradient image
    img = Image.new("RGB", (512, 512), color="red")
    pixels = img.load()
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            # Simple gradient based on position
            r = i * 255 // img.size[0]
            g = j * 255 // img.size[1]
            b = 128
            pixels[i, j] = (r, g, b)

    print("Placeholder image created successfully.")
    return img


def downscale_image(img, size=(16, 16)):
    """
    Downscales a single PIL Image object to a target size
    using Nearest Neighbor resampling to maintain the pixel art style.
    """
    try:
        # Resize the image using the Nearest Neighbor method
        # This is the key step for preserving the pixel art style
        resized_image = img.resize(size, Image.Resampling.NEAREST)
        print(f"Successfully downscaled image to {size[0]}x{size[1]}px.")
        return resized_image
    except Exception as e:
        print(f"Could not downscale image. Error: {e}")
        return None


# --- API Endpoint ---


@app.route("/generate", methods=["POST"])
def generate():
    """
    The main API endpoint. It receives generation parameters from the frontend,
    creates an image, downscales it, and returns it as a Base64 string.
    """
    # Get data from the incoming request
    data = request.get_json()
    prompt = data.get("prompt")
    negative_prompt = data.get("negativePrompt")
    model_checkpoint = data.get("checkpointModel")

    if not prompt or not model_checkpoint:
        return jsonify({"error": "Prompt and Checkpoint Model are required."}), 400

    # 1. Generate the initial high-resolution image
    #    (Replace this with your actual model call)
    initial_img = generate_initial_image(prompt, negative_prompt, model_checkpoint)
    if initial_img is None:
        return jsonify({"error": "Failed to generate initial image."}), 500

    # 2. Downscale the image to the target pixel art size
    pixel_art_img = downscale_image(initial_img)
    if pixel_art_img is None:
        return jsonify({"error": "Failed to downscale image."}), 500

    # 3. Convert the final image to a Base64 string to send in the JSON response
    buffered = io.BytesIO()
    # We save as PNG to preserve quality
    pixel_art_img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

    print("--- Request Complete ---")
    # Send the image back to the frontend
    return jsonify({"images": [f"data:image/png;base64,{img_str}"]})


# --- Run the Server ---
if __name__ == "__main__":
    # Runs the Flask server on http://127.0.0.1:5000
    app.run(debug=True, port=5000)
