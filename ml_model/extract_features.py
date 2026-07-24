import os
import numpy as np  # type: ignore[import]
import pandas as pd  # type: ignore[import]
import librosa  # type: ignore[import]

DATASET_FOLDER = "dataset"
CLASSES = ["pest", "no_pest"]
N_MFCC = 40
OUTPUT_CSV = "features.csv"

def extract_mfcc(file_path, n_mfcc=N_MFCC):
    y, sr = librosa.load(file_path, sr=22050)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc)
    mfcc_mean = np.mean(mfcc.T, axis=0)
    return mfcc_mean

def main():
    rows = []
    for label in CLASSES:
        folder = os.path.join(DATASET_FOLDER, label)
        if not os.path.isdir(folder):
            print(f"WARNING: {folder} nahi mila, skip kar raha hoon.")
            continue

        files = [f for f in os.listdir(folder) if f.lower().endswith(".wav")]
        print(f"{label}: {len(files)} files mil gayi, processing...")

        for fname in files:
            fpath = os.path.join(folder, fname)
            try:
                features = extract_mfcc(fpath)
                row = list(features) + [label, fname]
                rows.append(row)
            except Exception as e:
                print(f"  Skip {fname}: {e}")

    if not rows:
        print("Koi files process nahi hui.")
        return

    columns = [f"mfcc_{i+1}" for i in range(N_MFCC)] + ["label", "filename"]
    df = pd.DataFrame(rows, columns=columns)
    df.to_csv(OUTPUT_CSV, index=False)
    print(f"\nDone! {len(df)} rows '{OUTPUT_CSV}' mein save ho gayi.")
    print(df["label"].value_counts())

if __name__ == "__main__":
    main()