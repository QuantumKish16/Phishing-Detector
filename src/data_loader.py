import pandas as pd
from sklearn.model_selection import train_test_split

def load_data(path):
    df = pd.read_csv(path)
    X = df['text']
    y = df['label']
    return train_test_split(X, y, test_size=0.2, random_state=42)
