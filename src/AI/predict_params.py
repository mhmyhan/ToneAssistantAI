import joblib
import pandas as pd
import os

BASE_DIR = os.path.dirname(__file__)
MODEL_PATH = os.path.join(BASE_DIR, "models", "tone_model_1.1.pkl")

model = joblib.load(MODEL_PATH)


def predict_params(rms, centroid, zcr):
    features = pd.DataFrame([{
        "rms": rms,
        "centroid": centroid,
        "zcr": zcr
    }])

    return model.predict(features)[0]
