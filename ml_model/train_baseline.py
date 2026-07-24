import pandas as pd
from sklearn.model_selection import GroupShuffleSplit
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import joblib

df = pd.read_csv("features.csv")

# Zaroori fix: augmented files ko unki "original" file ke sath group karna hai,
# taake ek file ke saare versions (original + augmented: pitchup/pitchdown/noise/fast/slow)
# hamesha train ya test mein SATH rahein, kabhi split na hon.
# Warna model train mein ek file ka "sibling" dekh chuka hota hai, aur test mein
# uska doosra version aane par easily sahi predict kar leta hai -- ye asal
# generalization nahi, "data leakage" hai (isi wajah se pehle 100% accuracy aayi thi).
df["base_id"] = df["filename"].str.replace(
    r"_aug_(pitchup|pitchdown|noise|fast|slow)", "", regex=True
)
df["base_id"] = df["base_id"].str.replace(".wav", "", regex=False)

feature_cols = [c for c in df.columns if c.startswith("mfcc_")]
X_all = df[feature_cols]
y_all = df["label"]

gss = GroupShuffleSplit(n_splits=1, test_size=0.3, random_state=42)
train_idx, test_idx = next(gss.split(df, groups=df["base_id"]))

X_train, X_test = X_all.iloc[train_idx], X_all.iloc[test_idx]
y_train, y_test = y_all.iloc[train_idx], y_all.iloc[test_idx]

print(f"Train set: {len(X_train)} samples, {df.iloc[train_idx]['base_id'].nunique()} unique original recordings")
print(f"Test set:  {len(X_test)} samples, {df.iloc[test_idx]['base_id'].nunique()} unique original recordings\n")

model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

print("Classification Report:")
print(classification_report(y_test, y_pred))
print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))
print("Accuracy Score: {:.4f}".format(accuracy_score(y_test, y_pred)))

joblib.dump(model, "baseline_model.pkl")
print("\nModel 'baseline_model.pkl' mein save ho gaya.")