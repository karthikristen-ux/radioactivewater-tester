import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

# Example dataset (replace with real CSV if available)
df = pd.DataFrame({
    "pH": np.random.uniform(6, 9, 200),
    "TDS": np.random.uniform(100, 1500, 200),
    "Nitrate": np.random.uniform(0, 100, 200),
    "Hardness": np.random.uniform(50, 500, 200),
    "CPM": np.random.uniform(5, 100, 200),  # counts per minute from GM tube
    "Element": np.random.choice(["Uranium", "Cesium", "Strontium", "Safe"], 200)
})

X = df[["pH", "TDS", "Nitrate", "Hardness", "CPM"]]
y = df["Element"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

print("✅ Accuracy:", model.score(X_test, y_test))

# Save model
os.makedirs("models", exist_ok=True)
joblib.dump(model, "models/water_model.pkl")
print("💾 Model saved at models/water_model.pkl")
