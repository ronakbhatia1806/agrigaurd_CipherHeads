import sys, os

# --- FIX: Add project root to Python path ---
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ROOT)

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
from PIL import Image
import io

from model_loader import load_model, get_class_names
from security.verify.verify_image import verify_image
from security.verify.verify_salted import verify_salted_image

app = FastAPI(title="Agriguard API")

# --- CORS for frontend ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080",
        "http://127.0.0.1:8080",
        "http://localhost:5173",  # Default Vite port
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

MODEL = load_model()
CLASS_NAMES = get_class_names()
IMG_SIZE = (224, 224)

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Agriguard API is running",
        "version": "1.0.0",
        "endpoints": {
            "/predict": "POST - Upload an image for disease prediction",
            "/": "GET - API information (this endpoint)"
        },
        "status": "healthy"
    }

def preprocess_image_bytes(image_bytes: bytes) -> np.ndarray:
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    img = img.resize(IMG_SIZE)
    arr = np.array(img, dtype=np.float32) / 255.0
    arr = np.expand_dims(arr, axis=0)
    return arr


@app.options("/predict")
async def predict_options():
    """Handle CORS preflight requests"""
    return {"message": "OK"}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        print(f"[INFO] ========== NEW PREDICTION REQUEST ==========")
        print(f"[INFO] Received file: {file.filename}")
        print(f"[INFO] Content type: {file.content_type}")
        
        try:
            image_bytes = await file.read()
            print(f"[INFO] Read {len(image_bytes)} bytes")
        except Exception as e:
            print(f"[ERROR] Failed to read file: {str(e)}")
            raise HTTPException(status_code=400, detail=f"Failed to read file: {str(e)}")

        print("[INFO] Running integrity verification...")
        integrity = verify_image(image_bytes)
        print(f"[INFO] Integrity result: {integrity}")
        
        print("[INFO] Running salted verification...")
        salted = verify_salted_image(image_bytes)
        print(f"[INFO] Salted result: {salted}")

        try:
            print("[INFO] Preprocessing image...")
            batch = preprocess_image_bytes(image_bytes)
            print(f"[INFO] Batch shape: {batch.shape}")
        except Exception as e:
            print(f"[ERROR] Image preprocessing failed: {str(e)}")
            raise HTTPException(status_code=400, detail=f"Image preprocessing failed: {str(e)}")

        try:
            print("[INFO] Running model prediction...")
            preds = MODEL.predict(batch)[0]
            print(f"[INFO] Predictions shape: {preds.shape}")
        except Exception as e:
            print(f"[ERROR] Model prediction failed: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Model prediction failed: {str(e)}")

        pred_idx = int(np.argmax(preds))
        confidence = float(np.max(preds))
        pred_label = CLASS_NAMES[pred_idx]
        
        print(f"[INFO] Prediction: {pred_label} ({confidence:.2%})")

        return {
            "integrity_verified": integrity.get("verified"),
            "integrity_matched_file": integrity.get("matched_file"),
            "integrity_distance": integrity.get("distance"),
            "salted_authenticated": salted.get("authenticated"),
            "salted_match": salted.get("matched_image"),
            "prediction_index": pred_idx,
            "prediction_label": pred_label,
            "prediction_confidence": confidence
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"[ERROR] Unexpected error in predict endpoint: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

