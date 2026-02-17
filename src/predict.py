import pickle

model = pickle.load(open(r'D:\Phishing-Detector\models\phishing_model.pkl', 'rb'))
vectorizer = pickle.load(open(r'D:\Phishing-Detector\models\vectorizer.pkl', 'rb'))

def predict_email(text):
    vec = vectorizer.transform([text])
    pred = model.predict(vec)[0]
    return pred
