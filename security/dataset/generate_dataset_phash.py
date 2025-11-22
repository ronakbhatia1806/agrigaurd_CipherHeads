import os
import json
from PIL import Image
import imagehash

DATASET_DIR = r"C:/Users/RonakB/Desktop/agriguard/data/New Plant Diseases Dataset(Augmented)/New Plant Diseases Dataset(Augmented)/train"
OUTPUT_JSON = r"C:/Users/RonakB/Desktop/agriguard/security/dataset/image_hashes.json"

entries = []

for root, dirs, files in os.walk(DATASET_DIR):
    for file in files:
        if file.lower().endswith((".jpg",".jpeg",".png",".bmp",".tiff")):
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, DATASET_DIR)

            try:
                img = Image.open(full_path)
                ph = str(imagehash.phash(img))
                entries.append({
                    "filename": rel_path.replace("\\", "/"),
                    "phash": ph
                })
            except:
                pass

with open(OUTPUT_JSON, "w") as f:
    json.dump(entries, f, indent=4)

print(f"[OK] Generated pHashes: {len(entries)}")
print(f"Saved to: {OUTPUT_JSON}")

