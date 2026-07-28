"""
extract_features.py

Purpose:
  dataset/pest/ aur dataset/no_pest/ folders se saari .wav files parh kar
  MFCC features nikalta hai aur ek single features.csv banata hai.
  Yehi CSV agle step (train_model.py) mein use hoga.

How to use:
  python extract_features.py
"""

import os
import numpy as np
import pandas as pd
import librosa

DATASET_FOLDER = "dataset"
CLASSES = ["termite", "rodent", "no_pest"]   # ab teen classes hain
N_MFCC = 40                     # kitne MFCC coefficients nikalne hain (standard value)
OUTPUT_CSV = "features.csv"

def extract_mfcc(file_path, n_mfcc=N_MFCC):
    # audio load karo (sr=None matlab original sample rate rakho)
    y, sr = librosa.load(file_path, sr=22050)  # sab files ko 22050 Hz pe standardize karo
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc)
    # Sirf average nahi, standard deviation (variation) bhi lete hain --
    # isse thora zyada acoustic detail capture hoti hai (jaise pattern kitna
    # "consistent" ya "varying" hai poori clip mein). Ye termite jaisi
    # subtle/repetitive sounds ko behtar differentiate karne mein madad karta hai.
    mfcc_mean = np.mean(mfcc.T, axis=0)
    mfcc_std = np.std(mfcc.T, axis=0)
    return np.concatenate([mfcc_mean, mfcc_std])

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
        print("Koi files process nahi hui. Pehle dataset/pest aur dataset/no_pest folders check karein.")
        return

    columns = ([f"mfcc_mean_{i+1}" for i in range(N_MFCC)]
               + [f"mfcc_std_{i+1}" for i in range(N_MFCC)]
               + ["label", "filename"])
    df = pd.DataFrame(rows, columns=columns)
    df.to_csv(OUTPUT_CSV, index=False)
    print(f"\nDone! {len(df)} rows '{OUTPUT_CSV}' mein save ho gayi.")
    print(df["label"].value_counts())

if __name__ == "__main__":
    main()