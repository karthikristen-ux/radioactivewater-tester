import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

# ===================== 1. Load dataset =====================
df = pd.read_csv("water_data.csv")  # Make sure 'Element' column exists

# Features & Labels
X = df[["pH", "TDS", "Hardness", "Nitrate"]]
y = df["Element"]  # Categorical: Uranium, Cesium, Radium, etc.

# ===================== 2. Train-Test Split =====================
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ===================== 3. Train Random Forest Classifier =====================
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Accuracy
accuracy = model.score(X_test, y_test)
print(f"✅ Model trained successfully! Accuracy: {accuracy:.2f}")

# ===================== 4. Save Model =====================
os.makedirs("models", exist_ok=True)
joblib.dump(model, "models/element_detector.pkl")
print("💾 Model saved at models/element_detector.pkl")
