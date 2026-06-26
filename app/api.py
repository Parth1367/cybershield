import os
from flask import Flask, request, jsonify, render_template
from predictor import predict_url

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")

app = Flask(__name__, template_folder=TEMPLATE_DIR)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()

    if not data or "url" not in data:
        return jsonify({"error": "Please provide a URL"}), 400

    url = data["url"]
    prediction, probability = predict_url(url)

    if probability >= 0.85:
        result = "Phishing Website"
    elif probability >= 0.45:
        result = "Suspicious Website"
    else:
        result = "Legitimate Website"

    return jsonify({
        "url": url,
        "prediction": int(prediction),
        "result": result,
        "phishing_probability": float(round(probability, 4))
    })

if __name__ == "__main__":
    app.run(debug=True)