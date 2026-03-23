import joblib
import numpy as np

model = joblib.load("tone_model.pkl")

def predict_params(rms, centroid, zcr):
    features = np.array([[rms, centroid, zcr]])
    return model.predict(features)[0]
