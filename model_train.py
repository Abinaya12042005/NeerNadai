"""
model_train.py
----------------
Idhu namma "AI element" - RandomForest ML model.
Area-wise consumption data vachi, "wastage risk" (Low/Medium/High) predict pannum model.

Run: python model_train.py
Output: model/wastage_model.pkl  (used live by app.py)

NOTE: Idhu Google Colab-layum run pannalam - just upload the
area_wise_consumption.csv to Colab and run this same code in a cell.
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report
import joblib
import os

# 1. Load the area-wise consumption data
df = pd.read_csv("data/area_wise_consumption.csv")

# 2. Create the target label: wastage risk category based on Wastage_LPCD
#    (this is our "ground truth" for training - rule derived from CPHEEO norms)
def risk_label(w):
    if w < 10:
        return "Low"
    elif w < 30:
        return "Medium"
    else:
        return "High"

df["Wastage_Risk"] = df["Wastage_LPCD"].apply(risk_label)

# 3. Feature engineering - what the model learns from
le_area = LabelEncoder()
df["Area_Code"] = le_area.fit_transform(df["Area"])
df["Date_parsed"] = pd.to_datetime(df["Date"], format="%d-%m-%Y")
df["Month"] = df["Date_parsed"].dt.month
df["DayOfWeek"] = df["Date_parsed"].dt.dayofweek

FEATURES = ["Area_Code", "Population_Served", "Actual_LPCD", "Month", "DayOfWeek"]
X = df[FEATURES]
y = df["Wastage_Risk"]

# 4. Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# 5. Train RandomForest
model = RandomForestClassifier(n_estimators=200, max_depth=8, random_state=42)
model.fit(X_train, y_train)

# 6. Evaluate
preds = model.predict(X_test)
print("Model performance on test set:")
print(classification_report(y_test, preds))

# 7. Save model + label encoder for the Flask app
os.makedirs("model", exist_ok=True)
joblib.dump(model, "model/wastage_model.pkl")
joblib.dump(le_area, "model/area_encoder.pkl")
joblib.dump(FEATURES, "model/feature_list.pkl")

print("\nSaved: model/wastage_model.pkl, model/area_encoder.pkl")
