import os
import pandas as pd
import matplotlib
matplotlib.use("Agg")   # Important: saves graphs without display issue
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay,
    roc_curve,
    auc
)

# ==============================
# CURRENT FOLDER CHECK
# ==============================
print("Current folder:", os.getcwd())

# ==============================
# CREATE GRAPHS FOLDER
# ==============================
OUTPUT_DIR = "graphs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ==============================
# LOAD DATASET
# ==============================
df = pd.read_csv("data/phishing.csv")

print("\nDataset Loaded Successfully!")
print("Shape:", df.shape)
print("Missing Values:", df.isnull().sum().sum())
print("Duplicate Rows:", df.duplicated().sum())

# ==============================
# CLEAN DATA
# ==============================
df = df.drop_duplicates()

# ==============================
# FEATURES AND TARGET
# ==============================
X = df.drop("phishing", axis=1)
y = df["phishing"]

print("\nFeature Shape:", X.shape)
print("Target Shape:", y.shape)

# ==============================
# TRAIN TEST SPLIT
# ==============================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print("Train Shape:", X_train.shape)
print("Test Shape:", X_test.shape)

# ==============================
# RANDOM FOREST MODEL
# ==============================
rf_model = RandomForestClassifier(
    n_estimators=200,
    random_state=42
)

print("\nTraining Random Forest...")
rf_model.fit(X_train, y_train)

y_pred = rf_model.predict(X_test)
rf_acc = accuracy_score(y_test, y_pred)

print("\nRandom Forest Accuracy:", rf_acc)

print("\n===== CLASSIFICATION REPORT =====")
print(classification_report(y_test, y_pred))

# ==============================
# LOGISTIC REGRESSION MODEL
# ==============================
print("\nTraining Logistic Regression...")

lr_model = LogisticRegression(max_iter=3000)
lr_model.fit(X_train, y_train)

lr_pred = lr_model.predict(X_test)
lr_acc = accuracy_score(y_test, lr_pred)

print("Logistic Regression Accuracy:", lr_acc)

# ==============================
# FEATURE IMPORTANCE
# ==============================
importance = rf_model.feature_importances_

feat_df = pd.DataFrame({
    "Feature": X.columns,
    "Importance": importance
}).sort_values(by="Importance", ascending=False)

print("\nTop 10 Important Features:")
print(feat_df.head(10))

# ==============================
# SAVE FEATURE IMPORTANCE GRAPH
# ==============================
top10 = feat_df.head(10)

plt.figure(figsize=(10, 6))
plt.barh(top10["Feature"], top10["Importance"])
plt.xlabel("Importance")
plt.ylabel("Features")
plt.title("Top 10 Important Features")
plt.gca().invert_yaxis()
plt.tight_layout()

feature_path = os.path.join(OUTPUT_DIR, "feature_importance.png")
plt.savefig(feature_path, dpi=300, bbox_inches="tight")
plt.close()

print("Saved:", feature_path)

# ==============================
# SAVE CONFUSION MATRIX GRAPH
# ==============================
cm = confusion_matrix(y_test, y_pred)

disp = ConfusionMatrixDisplay(confusion_matrix=cm)
disp.plot(cmap="Blues")

plt.title("Confusion Matrix - Random Forest")
plt.tight_layout()

confusion_path = os.path.join(OUTPUT_DIR, "confusion_matrix.png")
plt.savefig(confusion_path, dpi=300, bbox_inches="tight")
plt.close()

print("Saved:", confusion_path)

# ==============================
# SAVE ROC CURVE GRAPH
# ==============================
y_prob = rf_model.predict_proba(X_test)[:, 1]

fpr, tpr, thresholds = roc_curve(y_test, y_prob)
roc_auc = auc(fpr, tpr)

plt.figure(figsize=(8, 6))
plt.plot(fpr, tpr, label=f"ROC Curve (AUC = {roc_auc:.2f})")
plt.plot([0, 1], [0, 1], linestyle="--")
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curve - Random Forest")
plt.legend(loc="lower right")
plt.tight_layout()

roc_path = os.path.join(OUTPUT_DIR, "roc_curve.png")
plt.savefig(roc_path, dpi=300, bbox_inches="tight")
plt.close()

print("Saved:", roc_path)

# ==============================
# SAVE MODEL COMPARISON GRAPH
# ==============================
models = ["Random Forest", "Logistic Regression"]
accuracies = [rf_acc, lr_acc]

plt.figure(figsize=(8, 5))
plt.bar(models, accuracies)
plt.ylim(0.8, 1.0)
plt.ylabel("Accuracy")
plt.title("Model Accuracy Comparison")
plt.tight_layout()

comparison_path = os.path.join(OUTPUT_DIR, "model_comparison.png")
plt.savefig(comparison_path, dpi=300, bbox_inches="tight")
plt.close()

print("Saved:", comparison_path)

# ==============================
# FINAL MESSAGE
# ==============================
print("\nGraphs saved successfully in 'graphs' folder:")
print("1. feature_importance.png")
print("2. confusion_matrix.png")
print("3. roc_curve.png")
print("4. model_comparison.png")

print("\nProject Completed Successfully!")