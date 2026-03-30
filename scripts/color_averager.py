import json
import csv
import sys
from pathlib import Path
from PIL import Image

# Setup paths and find the extracted version
extracted_assets_dir = Path('../extracted_assets')
version_dirs = [d for d in extracted_assets_dir.iterdir() if d.is_dir()]

if not version_dirs:
    print("No version directory found in ../extracted_assets")
    sys.exit()

version_dir = version_dirs[0]
version_name = version_dir.name

# Define directories for models and textures
models_dir = version_dir / 'models'
textures_dir = version_dir / 'textures'

json_files = list(models_dir.glob('*.json'))
valid_blocks = []

# Find all valid cube blocks from JSON models
for file in json_files:
    with open(file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        parent_name = data.get("parent")

        if parent_name is not None and "cube" in parent_name:
            valid_blocks.append((file.stem, data))

# Dictionary to store final RGB colors
block_colors = {}

# Process each valid block to find its texture
for block_name, data in valid_blocks:
    textures_dict = data.get("textures")

    if textures_dict is not None:

        # Get the 'all' texture or the first valid string
        texture_raw = textures_dict.get("all")

        if not isinstance(texture_raw, str):
            texture_raw = None

        if texture_raw is None:
            for val in textures_dict.values():
                if isinstance(val, str) and not val.startswith("#"):
                    texture_raw = val
                    break

        if texture_raw is None or texture_raw.startswith("#"):
            continue

        # Clean texture name and check if image exists
        texture_name = texture_raw.split('/')[-1]
        image_path = textures_dir / f"{texture_name}.png"

        if image_path.exists():

            try:
                img = Image.open(image_path).convert("RGBA")

                total_r, total_g, total_b = 0, 0, 0
                valid_pixels = 0

                # Calculate average color of opaque pixels
                for x in range(img.width):
                    for y in range(img.height):
                        r, g, b, a = img.getpixel((x, y))

                        if a == 255:
                            total_r += r
                            total_g += g
                            total_b += b
                            valid_pixels += 1

                if valid_pixels > 0:
                    avg_r = round(total_r / valid_pixels)
                    avg_g = round(total_g / valid_pixels)
                    avg_b = round(total_b / valid_pixels)

                    block_colors[block_name] = (avg_r, avg_g, avg_b)

            except Exception as e:
                print(f"Error processing {texture_name}.png: {e}")

# Ensure directories exist and save to CSV
results_dir = Path('../results')
results_dir.mkdir(parents=True, exist_ok=True)
csv_path = results_dir / f'{version_name}.csv'

with open(csv_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['block_name', 'r', 'g', 'b'])

    for block, (r, g, b) in block_colors.items():
        writer.writerow([block, r, g, b])