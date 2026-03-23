import joblib
import numpy as np

model = joblib.load("src/AI/models/tone_model_1.1.pkl")

def predict_params(rms, centroid, zcr):
    features = np.array([[rms, centroid, zcr]])
    return model.predict(features)[0]
