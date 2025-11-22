import sys, os
import json
from PIL import Image
import imagehash

# Add project root (agriguard/) to PYTHONPATH
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(ROOT_DIR)

from security.verify.qrng_salt_generator import generate_salt

PHASH_DB = r"C:/Users/RonakB/Desktop/agriguard/security/dataset/image_hashes.json"
OUTPUT_DB = r"C:/Users/RonakB/Desktop/agriguard/security/dataset/salted_hashes.json"


def generate_all_salted_hashes():
    if not os.path.exists(PHASH_DB):
        print("ERROR: image_hashes.json not found.")
        return

    with open(PHASH_DB, "r") as f:
        data = json.load(f)

    output = []

    for entry in data:
        phash = entry["phash"]
        filename = entry["filename"]

        # One salt per image (fixed)
        salt = generate_salt()

        # salted "hash" is just concatenation, no extra hash
        salted_value = phash + salt

        output.append({
            "filename": filename,
            "phash": phash,
            "salt": salt,
            "salted_value": salted_value
        })

    with open(OUTPUT_DB, "w") as f:
        json.dump(output, f, indent=4)

    print(f"Saved salted values to: {OUTPUT_DB}")
    print(f"Total entries generated: {len(output)}")


if __name__ == "__main__":
    generate_all_salted_hashes()
