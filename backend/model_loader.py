import os
import json
import tensorflow as tf

# Get project root (assuming backend/model_loader.py is one level deep)
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

MODEL_PATH = os.path.join(ROOT, "model", "mobilenet_v2.h5")
CLASS_INDEX_PATH = os.path.join(ROOT, "model", "class_indices.json")


def load_model():
    """Loads trained MobileNetV2 model from disk."""
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Model not found at: {MODEL_PATH}")

    # Fix for loading older models with 'groups' parameter in DepthwiseConv2D
    class CustomDepthwiseConv2D(tf.keras.layers.DepthwiseConv2D):
        def __init__(self, **kwargs):
            kwargs.pop('groups', None)
            super().__init__(**kwargs)

    model = tf.keras.models.load_model(MODEL_PATH, custom_objects={'DepthwiseConv2D': CustomDepthwiseConv2D})
    return model


def get_class_names():
    """Loads class index → label mapping from JSON."""
    if not os.path.exists(CLASS_INDEX_PATH):
        raise FileNotFoundError(f"class_indices.json not found at: {CLASS_INDEX_PATH}")

    with open(CLASS_INDEX_PATH, "r") as f:
        class_idx = json.load(f)

    # Convert {"0": "Apple___scab", ...} → list sorted by index
    sorted_labels = [class_idx[str(i)] for i in range(len(class_idx))]

    return sorted_labels
