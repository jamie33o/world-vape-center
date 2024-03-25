from PIL import Image
import os


for folder in os.listdir("media"):
    full_path = os.path.join("media", folder)

    if os.path.isdir(full_path):
        if os.path.exists(full_path) and len(os.listdir(full_path)) > 0:
            for filename in os.listdir(full_path):
                if filename.endswith(".png"):
                    input_path = os.path.join(full_path, filename)
                    output_path = os.path.join(
                        full_path, os.path.splitext(filename)[0] + ".webp"
                    )

                    # Open the PNG image
                    im = Image.open(input_path)

                    # Save it as WebP
                    im.save(output_path, "WEBP")

            print("Conversion completed.")
