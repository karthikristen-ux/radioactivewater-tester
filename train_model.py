import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

# -------------------------------
# 1. Generate Synthetic Dataset
# -------------------------------
np.random.seed(42)

n_samples = 500

data = {
    "pH": np.random.uniform(5.5, 9.0, n_samples),
    "Nitrate": np.random.uniform(0, 100, n_samples),
    "TDS": np.random.uniform(50, 1500, n_samples),
    "Hardness": np.random.uniform(20, 500, n_samples),
    "Uranium": np.random.uniform(0, 100, n_samples),
}

df = pd.DataFrame(data)

# Define safety rules (you can tweak as needed)
def label(row):
    if row["pH"] < 6.5 or row["pH"] > 8.5:
        return 1  # Unsafe
    if row["Nitrate"] > 45:
        return 1
    if row["TDS"] > 500:
        return 1
    if row["Hardness"] > 300:
        return 1
    if row["Uranium"] > 30:
        return 1
    return 0  # Safe

df["Label"] = df.apply(label, axis=1)

# -------------------------------
# 2. Train-Test Split
# -------------------------------
X = df[["pH", "Nitrate", "TDS", "Hardness", "Uranium"]]
y = df["Label"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# -------------------------------
# 3. Train Model
# -------------------------------
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

accuracy = model.score(X_test, y_test)
print(f"✅ Model trained with accuracy: {accuracy:.2f}")

# -------------------------------
# 4. Save Model
# -------------------------------
os.makedirs("models", exist_ok=True)
joblib.dump(model, "models/contaminant_model.pkl")
print("💾 Model saved at models/contaminant_model.pkl")
