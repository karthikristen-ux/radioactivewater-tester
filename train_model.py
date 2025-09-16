import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

# -------------------------------
# Load Dataset
# -------------------------------
data_path = "water_dataset.csv"
df = pd.read_csv(data_path)

# -------------------------------
# Check required columns
# -------------------------------
required_cols = ["pH","TDS","Hardness","Nitrate","Conductivity","Element"]
for col in required_cols:
    if col not in df.columns:
        raise ValueError(f"Missing column in dataset: {col}")

# -------------------------------
# Prepare Features & Labels
# -------------------------------
X = df[["pH","TDS","Hardness","Nitrate","Conductivity"]]
y = df["Element"]  # Uranium, Cesium, Radium

# -------------------------------
# Train-Test Split
# -------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# -------------------------------
# Train Random Forest Model
# -------------------------------
model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

accuracy = model.score(X_test, y_test)
print(f"✅ Model trained with accuracy: {accuracy:.2f}")

# -------------------------------
# Save Model
# -------------------------------
os.makedirs("models", exist_ok=True)
joblib.dump(model, "models/element_model.pkl")
print("💾 Model saved at models/element_model.pkl")
