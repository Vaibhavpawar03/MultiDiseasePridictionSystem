import os
import joblib
import numpy as np

from sklearn.datasets import load_diabetes, load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


MODEL_DIR = "models"
os.makedirs(MODEL_DIR, exist_ok=True)


# =========================
# DIABETES MODEL
# =========================
def train_diabetes():
    print("Training Diabetes Model...")

    # Using diabetes dataset (converted to classification)
    data = load_diabetes()
    X = data.data
    y = data.target

    # Convert regression → classification
    y = (y > np.mean(y)).astype(int)

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.2, random_state=42
    )

    model = RandomForestClassifier()
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)

    print("Diabetes Accuracy:", acc)

    joblib.dump(model, os.path.join(MODEL_DIR, "diabetes_model.pkl"))
    joblib.dump(scaler, os.path.join(MODEL_DIR, "diabetes_scaler.pkl"))


# =========================
# HEART MODEL (synthetic)
# =========================
def train_heart():
    print("Training Heart Model...")

    # Fake dataset (for now)
    X = np.random.rand(500, 13)
    y = np.random.randint(0, 2, 500)

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.2, random_state=42
    )

    model = RandomForestClassifier()
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)

    print("Heart Accuracy:", acc)

    joblib.dump(model, os.path.join(MODEL_DIR, "heart_model.pkl"))
    joblib.dump(scaler, os.path.join(MODEL_DIR, "heart_scaler.pkl"))


# =========================
# BREAST CANCER MODEL
# =========================
def train_breast_cancer():
    print("Training Breast Cancer Model...")

    data = load_breast_cancer()
    X = data.data
    y = data.target

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.2, random_state=42
    )

    model = RandomForestClassifier()
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)

    print("Breast Cancer Accuracy:", acc)

    joblib.dump(model, os.path.join(MODEL_DIR, "breast_cancer_model.pkl"))
    joblib.dump(scaler, os.path.join(MODEL_DIR, "breast_cancer_scaler.pkl"))


# =========================
# RUN ALL
# =========================
if __name__ == "__main__":
    train_diabetes()
    train_heart()
    train_breast_cancer()

    print("\nALL MODELS TRAINED SUCCESSFULLY ✅")