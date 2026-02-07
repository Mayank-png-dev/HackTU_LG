from fastapi import FastAPI
import requests
import joblib
import numpy as np
import pandas as pd

# -----------------------
# Load models
# -----------------------
voting_model = joblib.load("voting_model.pkl")
stacked_model = joblib.load("stacked_model.pkl")
scaler = joblib.load("scaler.pkl")

app = FastAPI()

ESP32_IP = "http://172.25.90.172/read"   # change if needed


# -----------------------
# Yellowness index logic (copied from notebook)
# -----------------------
def compute_yellowness(r, g, b, c):
    rgb = np.array([[r, g, b]], dtype=float)
    rgb_norm = rgb / max(c, 1e-6)

    gray_world_avg = np.mean(rgb_norm, axis=0)
    rgb_balanced = np.clip(rgb_norm / (gray_world_avg + 1e-6), 0, 1)

    gamma = 2.2
    rgb_linear = np.power(rgb_balanced, gamma)

    M = np.array([
        [0.4124564, 0.3575761, 0.1804375],
        [0.2126729, 0.7151522, 0.0721750],
        [0.0193339, 0.1191920, 0.9503041]
    ])

    xyz = rgb_linear @ M.T
    X, Y, Z = xyz[0]

    Cx, Cz = 1.2769, 1.0592
    yi = 100 * (Cx * X - Cz * Z) / max(Y, 1e-6)

    return yi


# -----------------------
# Prediction API
# -----------------------
@app.get("/predict")
def predict(age: int, gender: str, height: float, weight: float):

    # get ESP32 data
    sensor = requests.get(ESP32_IP).json()

    # BMI
    h_m = height / 100
    bmi = weight / (h_m * h_m)

    # gender mapping
    gender_val = 1.0 if gender.lower() == "male" else 0.0

    # yellowness
    yi = compute_yellowness(
        sensor["r"],
        sensor["g"],
        sensor["b"],
        1.0  # intensity already normalized in many cases
    )

    df = pd.DataFrame([{
        "Age": age,
        "Gender": gender_val,
        "BodyTemp": sensor["bodyTemp"],
        "LiverTemp": sensor["thermalMax"],
        "GSR": sensor["gsr"],
        "BMI": bmi,
        "Yellowness Index": yi
    }])

    X = scaler.transform(df)

    # Prefer using predicted probabilities to compute a meaningful confidence
    try:
        p_vote = voting_model.predict_proba(X)[0][1]
    except Exception:
        # fallback to deterministic prediction if predict_proba isn't available
        p_vote = float(voting_model.predict(X)[0])

    try:
        p_stack = stacked_model.predict_proba(X)[0][1]
    except Exception:
        p_stack = float(stacked_model.predict(X)[0])

    # Ensemble probability (average of model probabilities)
    ensemble_prob = float((p_vote + p_stack) / 2)

    risk = "High" if ensemble_prob >= 0.5 else "Low"
    confidence = int(round(ensemble_prob * 100))

    return {
        "risk": risk,
        "confidence": confidence,
        "models": {
            "Voting": int(round(p_vote)),
            "Stacked": int(round(p_stack)),
            "Voting_proba": float(p_vote),
            "Stacked_proba": float(p_stack)
        },
        "sensor": sensor
    }

