import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

# Load dataset
df = pd.read_csv("water_dataset.csv")  # Your CSV file

# Features & Label
X = df.drop("Element", axis=1)
y = df["Element"]

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

# Accuracy
accuracy = model.score(X_test, y_test)
print(f"✅ Model trained with accuracy: {accuracy:.2f}")

# Save model
import os
os.makedirs("models", exist_ok=True)
joblib.dump(model, "models/element_model.pkl")
print("💾 Model saved at models/element_model.pkl")
