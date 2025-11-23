import os
import json
import numpy as np
from tensorflow.keras.models import load_model as keras_load_model

# Resolve the absolute path to the project root (one level up from this file)
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Paths to model and class indices
MODEL_PATH = os.path.join(ROOT_DIR, "model", "mobilenet_v2.h5")
CLASS_INDICES_PATH = os.path.join(ROOT_DIR, "model", "class_indices.json")

def load_model():
    """Load the trained Keras model.

    Returns:
        keras.Model: The loaded model ready for inference.
    """
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")
    model = keras_load_model(MODEL_PATH)
    return model

def get_class_names():
    """Load the class index mapping from the JSON file.

    Returns:
        list: Ordered list of class names where the index corresponds to the model's output index.
    """
    if not os.path.exists(CLASS_INDICES_PATH):
        raise FileNotFoundError(f"Class indices file not found at {CLASS_INDICES_PATH}")
    with open(CLASS_INDICES_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    # Convert dict of index->name to ordered list
    ordered = [data[str(i)] for i in range(len(data))]
    return ordered
