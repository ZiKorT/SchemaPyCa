from pathlib import Path
import sys

# Import our custom scripts as modules
from scripts.texture_extractor import extract_version
from scripts.color_averager import calculate_averages

# Setup root directories based on main.py location
ROOT_DIR = Path(__file__).parent
VERSIONS_DIR = ROOT_DIR / 'Versions'
EXTRACTED_DIR = ROOT_DIR / 'extracted_assets'
RESULTS_DIR = ROOT_DIR / 'results'


def main():
    # Find all .jar files in the Versions folder
    jar_files = list(VERSIONS_DIR.glob('*.jar'))

    if not jar_files:
        print(f"Error: No .jar files found in {VERSIONS_DIR}")
        sys.exit()

    print(f"Found {len(jar_files)} version(s) to process.\n")

    # Process each version one by one
    for jar_path in jar_files:
        version_name = jar_path.stem
        print(f"{"=" * 40}")
        print(f"PROCESSING VERSION: {version_name}")
        print(f"{"=" * 40}")

        # Step 1: Extract files
        extract_version(jar_path, EXTRACTED_DIR)

        # Step 2: Calculate colors and generate CSV
        calculate_averages(version_name, EXTRACTED_DIR, RESULTS_DIR)

        print("\n")

    print("All versions processed successfully.")


if __name__ == "__main__":
    main()