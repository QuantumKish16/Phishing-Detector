import pandas as pd
import pickle
import os
import numpy as np

from sklearn.svm import LinearSVC
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import cross_val_score
from preprocess import clean_text, extract_url_features
from scipy.sparse import hstack


# 1. Load Dataset
data = pd.read_csv(r"D:\Phishing-Detector\data\raw_emails.csv")

# Combine relevant text columns into a single feature
data["text"] = data["subject"].fillna("") + " " + data["body"].fillna("")

# Clean text for TF-IDF
data["clean_text"] = data["text"].apply(clean_text)

# Extract URL features from ORIGINAL text

data["url_features"] = data.apply(
    lambda row: extract_url_features(row["text"], row["sender"]),
    axis=1
)



X = data["clean_text"]
y = data["label"]

# 2. Split Dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42,stratify=y
)

# 3. Convert Text to Numerical Features (TF-IDF)
vectorizer = TfidfVectorizer(
    stop_words="english",
    max_features=10000,
    ngram_range=(1, 2)   # add bigrams
)

X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

X_train_extra = list(data.loc[X_train.index, "url_features"])
X_test_extra = list(data.loc[X_test.index, "url_features"])

# Convert to array

X_train_extra = np.array(X_train_extra)
X_test_extra = np.array(X_test_extra)

# Combine features
X_train_final = hstack([X_train_vec, X_train_extra])
X_test_final = hstack([X_test_vec, X_test_extra])

# 4. Train Model



model = LogisticRegression(
    max_iter=3000,
    solver="liblinear"
)


model.fit(X_train_final, y_train)

# 5. Evaluate Model
y_pred = model.predict(X_test_final)

print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n")
print(classification_report(y_test, y_pred))

# 6. Save Model and Vectorizer
os.makedirs(r"D:\Phishing-Detector\models", exist_ok=True)

pickle.dump(model, open(r"D:\Phishing-Detector\models\phishing_model.pkl", "wb"))
pickle.dump(vectorizer, open(r"D:\Phishing-Detector\models\vectorizer.pkl", "wb"))

print("\nModel saved as phishing_model.pkl")

print("Total dataset size:", len(X))
print("Training size:", len(X_train))
print("Test size:", len(X_test))
y_pred = model.predict(X_test_final)

print("Predictions made:", len(y_pred))
print("Test labels:", len(y_test))
print(data["label"].value_counts())

cv_scores = cross_val_score(model, X_train_final, y_train, cv=5)

print("Cross-validation scores:", cv_scores)
print("Average CV accuracy:", cv_scores.mean())
from sklearn.metrics import confusion_matrix
print(confusion_matrix(y_test, y_pred))

