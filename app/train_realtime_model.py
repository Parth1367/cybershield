import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# Load dataset
df = pd.read_csv("data/phishing.csv")
df = df.drop_duplicates()

# Improved deployable features
selected_features = [
    "qty_dot_url",
    "qty_hyphen_url",
    "qty_underline_url",
    "qty_slash_url",
    "qty_questionmark_url",
    "qty_equal_url",
    "qty_at_url",
    "qty_and_url",
    "qty_exclamation_url",
    "qty_space_url",
    "length_url",
    "url_shortened"
]

# Use only features that exist in dataset
X = df[selected_features]
y = df["phishing"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = RandomForestClassifier(
    n_estimators=300,
    max_depth=20,
    min_samples_split=5,
    min_samples_leaf=2,
    random_state=42
)

model.fit(X_train, y_train)

y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)

print("Improved Realtime Model Accuracy:", acc)
print("\nClassification Report:\n")
print(classification_report(y_test, y_pred))

joblib.dump(model, "model/phishing_model.pkl")
joblib.dump(selected_features, "model/feature_names.pkl")

print("\nImproved model saved successfully in /model folder")