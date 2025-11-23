import os
import sys
import json

# Add project root (agriguard2) to PYTHONPATH so we can import the salt generator
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(ROOT_DIR)

import secrets

def generate_salt():
    """Generate a simple random hex salt (16 characters)."""
    return secrets.token_hex(8)

# Paths to the source pHash DB and the output salted DB
PHASH_DB = os.path.join(ROOT_DIR, "security", "dataset", "image_hashes.json")
OUTPUT_DB = os.path.join(ROOT_DIR, "security", "dataset", "salted_hashes.json")


def generate_all_salted_hashes():
    """Read image_hashes.json, generate a random salt for each entry,
    concatenate the salt with the existing pHash, and write the result to
    salted_hashes.json.
    """
    if not os.path.exists(PHASH_DB):
        print(f"[ERROR] pHash DB not found at {PHASH_DB}")
        return

    with open(PHASH_DB, "r", encoding="utf-8") as f:
        data = json.load(f)

    output = []
    for entry in data:
        phash = entry.get("phash")
        filename = entry.get("filename")
        # Generate a fresh salt (e.g., 16‑byte hex string)
        salt = generate_salt()
        salted_value = f"{salt}{phash}"
        output.append({
            "filename": filename,
            "phash": phash,
            "salt": salt,
            "salted_value": salted_value,
        })

    # Write the new salted DB (overwrite if it exists)
    with open(OUTPUT_DB, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=4)
    print(f"[INFO] Saved salted values to: {OUTPUT_DB}")
    print(f"[INFO] Total entries generated: {len(output)}")


if __name__ == "__main__":
    generate_all_salted_hashes()
