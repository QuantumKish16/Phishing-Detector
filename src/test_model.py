import pickle
from preprocess import clean_text,extract_url_features
from scipy.sparse import hstack
import numpy as np

model = pickle.load(open(r"D:\Phishing-Detector\models\phishing_model.pkl", "rb"))
vectorizer = pickle.load(open(r"D:\Phishing-Detector\models\vectorizer.pkl", "rb"))

sample_email = '''email here'''

cleaned = clean_text(sample_email)
vec = vectorizer.transform([cleaned])
sender_email = "services@paypal-accounts.com"
extra = np.array([extract_url_features(sample_email, sender_email)])
sample_vec = hstack([vec,extra])
prediction = model.predict(sample_vec)

print("Prediction:", prediction[0])
if (prediction == 1):
    print("Prediction: Phishing")
else:
    print("prediction: Safe")