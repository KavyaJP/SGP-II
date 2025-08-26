import os
from PIL import Image

# --- Configuration ---
# 1. The folder where your 512x512 generated images are located.
input_folder = "input_images"

# 2. The folder where the new 16x16 images will be saved.
output_folder = "downscaled_images"
# -------------------


def downscale_images(source_folder, destination_folder, size):
    """
    Downscales all images in a source folder to a target size
    and saves them in a destination folder using Nearest Neighbor resampling.
    """
    # Create the output folder if it doesn't already exist
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
        print(f"Created directory: {destination_folder}")

    # Get a list of all files in the input folder
    files = os.listdir(source_folder)

    # Loop through each file
    for filename in files:
        # Check if the file is an image
        if filename.lower().endswith((".png", ".jpg", ".jpeg", ".bmp")):
            try:
                # Construct the full file path
                file_path = os.path.join(source_folder, filename)

                # Open the image
                with Image.open(file_path) as img:
                    # Resize the image using the Nearest Neighbor method
                    # This is the key step for preserving the pixel art style
                    resized_image = img.resize(size, Image.Resampling.NEAREST)

                    # Construct the output path
                    output_path = os.path.join(destination_folder, filename)

                    # Save the new, downscaled image
                    resized_image.save(output_path)
                    print(
                        f"Successfully downscaled '{filename}' to {size[0]}x{size[1]} px."
                    )

            except Exception as e:
                print(f"Could not process {filename}. Error: {e}")


# --- Run the script ---
if __name__ == "__main__":
    x = int(input("Enter Width: "))
    y = int(input("Enter Height: "))
    target_size = (x, y)
    downscale_images(input_folder, output_folder, target_size)
