import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

# ===================== 1. Load your dataset =====================
DATA_PATH = "water_data.csv"

if not os.path.exists(DATA_PATH):
    raise FileNotFoundError(f"{DATA_PATH} not found. Please make sure your dataset exists.")

df = pd.read_csv(DATA_PATH)

# Check required columns
required_columns = ["pH", "TDS", "Hardness", "Nitrate", "Element"]
for col in required_columns:
    if col not in df.columns:
        raise ValueError(f"Missing column in dataset: {col}")

# ===================== 2. Prepare Features & Labels =====================
X = df[["pH", "TDS", "Hardness", "Nitrate"]]
y = df["Element"]  # Target label: Uranium, Cesium, Radium, etc.

# ===================== 3. Train-Test Split =====================
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ===================== 4. Train Random Forest Classifier =====================
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate accuracy
accuracy = model.score(X_test, y_test)
print(f"✅ Model trained successfully! Accuracy: {accuracy:.2f}")

# ===================== 5. Save Model =====================
os.makedirs("models", exist_ok=True)
MODEL_PATH = "models/element_detector.pkl"
joblib.dump(model, MODEL_PATH)
print(f"💾 Model saved at {MODEL_PATH}")
