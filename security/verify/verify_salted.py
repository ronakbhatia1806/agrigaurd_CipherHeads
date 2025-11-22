import sys, os
import json
from PIL import Image
import imagehash

import io

# Add project root
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(ROOT_DIR)

SALTED_DB = os.path.join(ROOT_DIR, "security", "dataset", "salted_hashes.json")


def verify_salted_image(image_input):
    if not os.path.exists(SALTED_DB):
        return {"authenticated": False, "matched_image": None}

    with open(SALTED_DB, "r") as f:
        data = json.load(f)

    try:
        # Compute pHash of uploaded image
        if isinstance(image_input, bytes):
            img = Image.open(io.BytesIO(image_input)).convert("RGB")
        else:
            img = Image.open(image_input).convert("RGB")
            
        phash_user = str(imagehash.phash(img))

        # Check against all stored salted values
        for entry in data:
            salt = entry["salt"]
            stored_salted = entry["salted_value"]

            candidate = phash_user + salt

            if candidate == stored_salted:
                return {
                    "authenticated": True,
                    "matched_image": entry["filename"]
                }

        return {
            "authenticated": False,
            "matched_image": None
        }
    except Exception as e:
        print(f"Error in verify_salted_image: {e}")
        return {
            "authenticated": False,
            "matched_image": None
        }
