import imagehash
from PIL import Image
import json
import os

import io

# Dynamic path
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
HASH_DB_PATH = os.path.join(ROOT, "model", "image_hashes.json")

# Load hash database once
if os.path.exists(HASH_DB_PATH):
    with open(HASH_DB_PATH, "r") as f:
        HASH_DB = json.load(f)
else:
    HASH_DB = []
    print(f"Warning: Hash DB not found at {HASH_DB_PATH}")


def verify_image(image_input, threshold=5):
    """
    Returns True if image matches a known dataset image (integrity passed),
    False otherwise.
    threshold: max Hamming distance allowed between pHashes.
    """

    try:
        # Compute pHash of incoming image
        if isinstance(image_input, bytes):
            img = Image.open(io.BytesIO(image_input))
        else:
            img = Image.open(image_input)
        
        incoming_hash = imagehash.phash(img)

        # Compare with stored hashes
        for entry in HASH_DB:
            stored_hash = imagehash.hex_to_hash(entry["phash"])
            dist = incoming_hash - stored_hash

            if dist <= threshold:
                return {
                    "verified": True,
                    "matched_file": entry["filename"],
                    "distance": dist
                }

        return {
            "verified": False,
            "matched_file": None,
            "distance": None
        }
    except Exception as e:
        print(f"Error in verify_image: {e}")
        return {
            "verified": False,
            "matched_file": None,
            "distance": None
        }


if __name__ == "__main__":
    test = verify_image(r"C:/Users/RonakB/Desktop/agriguard/test/test_image.jpg")
    print(test)

