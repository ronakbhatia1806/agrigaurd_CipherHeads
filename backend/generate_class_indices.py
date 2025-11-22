import os
import json

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(ROOT, "data", "New Plant Diseases Dataset(Augmented)", "New Plant Diseases Dataset(Augmented)", "train")
OUTPUT = os.path.join(ROOT, "model", "class_indices.json")

def generate_class_indices():
    if not os.path.exists(DATA_DIR):
        raise FileNotFoundError(f"Dataset not found: {DATA_DIR}")

    classes = sorted(os.listdir(DATA_DIR))  # sorted list for stable ordering

    class_map = {str(i): cls for i, cls in enumerate(classes)}

    with open(OUTPUT, "w") as f:
        json.dump(class_map, f, indent=4)

    print("class_indices.json created:")
    print(json.dumps(class_map, indent=4))


if __name__ == "__main__":
    generate_class_indices()
