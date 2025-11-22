import os
import json
from PIL import Image
import imagehash

# PATH TO YOUR TRAIN DATASET
DATASET_DIR = r"C:/Users/RonakB/Desktop/agriguard/data/New Plant Diseases Dataset(Augmented)/New Plant Diseases Dataset(Augmented)/train"

# SAVE HASHES HERE
OUTPUT_HASH_FILE = r"C:/Users/RonakB/Desktop/agriguard/model/image_hashes.json"

hash_map = {}

print("\n=== Generating perceptual hashes (pHash) for dataset images ===\n")

for root, dirs, files in os.walk(DATASET_DIR):
    for file in files:
        if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
            full_path = os.path.join(root, file)

            try:
                img = Image.open(full_path)
                img_hash = str(imagehash.phash(img))

                relative_path = os.path.relpath(full_path, DATASET_DIR)

                hash_map[relative_path] = img_hash

            except Exception as e:
                print(f"Error processing {file}: {e}")

with open(OUTPUT_HASH_FILE, "w") as f:
    json.dump(hash_map, f, indent=4)

print("\nHashes saved to:", OUTPUT_HASH_FILE)
print("Total images hashed:", len(hash_map))
print("\n=== DONE ===")
