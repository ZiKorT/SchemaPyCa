import zipfile
from pathlib import Path

def extract_version(jar_path: Path, output_base_dir: Path):
    version_name = jar_path.stem
    final_dir = output_base_dir / version_name

    compteur_fichiers = 0

    print(f"Extracting {version_name}.jar...")

    with zipfile.ZipFile(jar_path, 'r') as archive:
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
                continue

            target_file = final_dir / clean_path

            # Create parent directories if they don't exist
            target_file.parent.mkdir(parents=True, exist_ok=True)

            # Read data from the zip and write it to the new file
            with target_file.open('wb') as f_out:
                f_out.write(archive.read(path))

            compteur_fichiers += 1

    print(f"Extracted {compteur_fichiers} files to {final_dir}")