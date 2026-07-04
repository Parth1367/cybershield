import joblib
import pandas as pd
from urllib.parse import urlparse
from .feature_extractor import extract_features

# Load model and feature names
model = joblib.load("model/phishing_model.pkl")
feature_names = joblib.load("model/feature_names.pkl")

# Trusted domains
TRUSTED_DOMAINS = {
    "google.com",
    "www.google.com",
    "chatgpt.com",
    "www.chatgpt.com",
    "openai.com",
    "www.openai.com",
    "microsoft.com",
    "www.microsoft.com",
    "amazon.com",
    "www.amazon.com",
    "github.com",
    "www.github.com",
    "youtube.com",
    "www.youtube.com"
}

def predict_url(url):
    parsed = urlparse(url)
    domain = parsed.netloc.lower()

    # Allowlist override
    if domain in TRUSTED_DOMAINS:
        return 0, 0.01

    # Extract features
    features = extract_features(url)

    # Convert to DataFrame
    df = pd.DataFrame([features])

    # Ensure same feature order
    for col in feature_names:
        if col not in df.columns:
            df[col] = 0

    df = df[feature_names]

    # Prediction
    prediction = model.predict(df)[0]
    probability = model.predict_proba(df)[0][1]

    return prediction, probability