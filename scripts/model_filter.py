
import json
from pathlib import Path

dossier_models = Path('../extracted_assets/26.1/models')
json_files = list(dossier_models.glob('*.json'))
real_block = []

# Scanning json files
for fichier in json_files:
    with open(fichier, 'r', encoding='utf-8') as f:
        data = json.load(f)
        parent_name = data.get("parent")
        # verifying if the block is a cube
        if parent_name is not None and "cube" in parent_name:
            real_block.append(fichier.stem)
print(f"{len(real_block)} blocks found")