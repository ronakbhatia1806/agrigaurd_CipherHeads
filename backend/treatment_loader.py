import json
import os

# Resolve root directory (project root)
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

TREATMENTS_PATH = os.path.join(ROOT_DIR, "backend", "treatments", "disease_treatments.json")

def load_treatments():
    """Load the disease treatments JSON file.
    Returns:
        dict: Mapping of disease label to treatment info.
    """
    if not os.path.exists(TREATMENTS_PATH):
        raise FileNotFoundError(f"Treatments file not found at {TREATMENTS_PATH}")
    with open(TREATMENTS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def get_treatment_for_disease(disease_label: str, severity: str):
    """Retrieve treatment info for a given disease and severity.
    Args:
        disease_label: The label returned by the model (e.g., "Potato___Early_blight").
        severity: "low", "moderate", or "high" (calculated from confidence).
    Returns:
        dict with keys:
            - treatments (list of strings)
            - severity_note (string)
            - has_custom_treatment (bool)
    """
    data = load_treatments()
    default = {
        "treatments": [],
        "severity_note": "No specific treatment information available.",
        "has_custom_treatment": False,
    }
    info = data.get(disease_label, default)
    # If treatments is a dict keyed by severity, fetch appropriate list
    treatments = info.get("treatments", [])
    if isinstance(treatments, dict):
        treatments = treatments.get(severity, [])
    return {
        "treatments": treatments,
        "severity_note": info.get("severity_note", ""),
        "has_custom_treatment": bool(treatments),
    }

def calculate_severity(confidence: float) -> str:
    """Map confidence (0-1) to a severity string.
    Low confidence => high severity (more uncertain -> treat as severe).
    """
    if confidence >= 0.8:
        return "low"
    elif confidence >= 0.5:
        return "moderate"
    else:
        return "high"
