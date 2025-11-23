# Agriguard AI

A lightweight image classifier for crop health that runs on mobile or edge devices. It combines a MobileNetV2 model for disease detection with a dual-layer image-integrity system using pHash and a QRNG-influenced salt scheme.

## 🔍 Overview

Agriguard AI analyzes leaf photos to determine whether a crop is Healthy or Diseased and can optionally identify the disease type. The pipeline also validates image authenticity to prevent tampering or replay attacks.

## ✨ Key features

* Fast, lightweight MobileNetV2 model trained on the New Plant Diseases Dataset (Augmented)
* pHash based similarity check for image integrity
* Quantum-influenced salted values for authentication
* Local JSON storage for salted values for simple deployment
* FastAPI backend and lightweight frontend suitable for edge or mobile usage

## 🧭 How it works

1. User uploads a leaf photo via the frontend.
2. Backend saves the image to a temporary file.
3. pHash integrity check runs to find similar images in the trusted dataset.
4. Salted-value authentication compares uploaded pHash + stored salt values.
5. If checks pass, the MobileNetV2 model predicts Healthy vs Diseased and returns confidence and class.
6. Backend returns a single JSON response containing integrity, authentication, and prediction results.

## ⚙️ Requirements

* Python 3.10
* venv with required packages: TensorFlow, qiskit, qiskit-aer, imagehash, pillow, fastapi, uvicorn
* Node.js and npm for frontend (if using React/Vite)

## 🧰 Project layout

```
agriguard/
  backend/
    main.py
    model_loader.py
  model/
    mobilenet_v2.h5
  security/
    verify/
      verify_image.py
      verify_salted.py
      qrng_salt_generator.py
    dataset/
      image_hashes.json
      salted_hashes.json
      generate_dataset_phash.py
      generate_salted_hashes.py
  frontend/
    package.json
    src/
```

## 🚀 Setup and run (quick)

1. Create and activate venv

```bash
python -m venv venv
venv\Scripts\activate
```

2. Install backend dependencies

```bash
pip install -r backend/requirements.txt
```

3. Generate pHashes (run once)

```bash
python security\dataset\generate_dataset_phash.py
```

4. Generate salted values (run once)

```bash
python security\dataset\generate_salted_hashes.py
```

5. Start backend

```bash
cd backend
python main.py
```

6. Start frontend

```bash
cd frontend
npm install
npm run dev
```

7. Open UI at [http://localhost:5173](http://localhost:5173) and use the upload flow. Backend docs at [http://localhost:8000/docs](http://localhost:8000/docs)

## 🧪 Testing flow

* Upload a known dataset image to confirm integrity_verified true and salted_authenticated true
* Upload a new farmer image to confirm integrity_verified false but model still returns prediction

## 🔐 Security notes

* salted_value is pHash + salt (string concatenation) stored in `salted_hashes.json`
* Salt generator uses QRNG-styled logic; salts are generated once per dataset image
* Use HTTPS in production and consider moving salted DB to a secure store like MongoDB for scaling

## 🛠 Troubleshooting

* If backend import errors occur, ensure venv is active and you ran `sys.path` fix in `main.py` when launching from backend folder
* If TensorFlow errors appear on import, check numpy, scipy, protobuf versions and match TensorFlow supported versions
* If frontend shows failed fetch, ensure API calls point to `http://localhost:8000/predict` and CORS is enabled in backend

## 📁 Resources

* Hackathon guidance PDF: `/mnt/data/Hackathon AI_ML Project Guidance.pdf`

## 📞 Contact

For implementation questions, reach the dev team in the project channel or open an issue in the repo.

---

Thank you for using Agriguard AI. Good luck with the demo 🎯
