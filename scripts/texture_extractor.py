import zipfile
import sys
from pathlib import Path

# Searching for jar files in the directory
fichiers_jar = list(Path('../versions').glob('*.jar'))

# Exit cleanly if no .jar files are found
if len(fichiers_jar) == 0:
    print("No .jar files found")
    sys.exit()

jar_file = fichiers_jar[0]
# Get the version name without the .jar extension
version_name = jar_file.stem
final_dir = Path("../extracted_assets") / version_name

compteur_fichiers = 0

with zipfile.ZipFile(jar_file, 'r') as archive:
    every_path = archive.namelist()

    for path in every_path:
        # Ignore directory entries
        if path.endswith('/'):
            continue

        # Only keep .json for models and .png for textures
        if path.startswith("assets/minecraft/models/block/") and path.endswith(".json"):
            clean_path = path.replace("assets/minecraft/models/block/", "models/", 1)

        elif path.startswith("assets/minecraft/textures/block/") and path.endswith(".png"):
            clean_path = path.replace("assets/minecraft/textures/block/", "textures/", 1)

        else:
            # Skip other files
            continue

        target_file = final_dir / clean_path

        # Create parent directories if they don't exist
        target_file.parent.mkdir(parents=True, exist_ok=True)

        # Read data from the zip and write it to the new file
        with target_file.open('wb') as f_out:
            f_out.write(archive.read(path))

        compteur_fichiers += 1

print(f"Extracted {compteur_fichiers} files to {final_dir}")