from flask import Flask, render_template, request
import pickle
import os

from preprocess import clean_text, extract_url_features
from scipy.sparse import hstack
import numpy as np

app = Flask(
    __name__,
    template_folder=r"D:\Phishing-Detector\templates",
    static_folder=r"D:\Phishing-Detector\static"
)


# Load model
model = pickle.load(open(r"D:\Phishing-Detector\models\phishing_model.pkl", "rb"))
vectorizer = pickle.load(open(r"D:\Phishing-Detector\models\vectorizer.pkl", "rb"))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    email_text = request.form.get("email", "")
    sender_email = request.form.get("sender", "")



    # 1️⃣ Clean text for TF-IDF
    cleaned_text = clean_text(email_text)
    vector = vectorizer.transform([cleaned_text])

    # 2️⃣ Extract URL features from ORIGINAL text
    url_extra = np.array([extract_url_features(email_text, sender_email)])

    


    # 3️⃣ Combine TF-IDF + URL features
    final_input = hstack([vector, url_extra])

    # 4️⃣ Predict
    probabilities = model.predict_proba(final_input)[0]
    phishing_prob = probabilities[1]

    if phishing_prob > 0.35:   # custom threshold
        prediction = 1
    else:
        prediction = 0

    confidence = round(phishing_prob * 100, 2)
    security_score = round(100 - confidence, 2)

    if prediction == 1:
        result = "⚠️ Phishing Detected!"
    else:
        result = "✅ Email is Safe"

    return render_template(
    "index.html",
    prediction_text=result,
    confidence=confidence,
    security_score=security_score
)



if __name__ == "__main__":
    app.run(debug=True)
