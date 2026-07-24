"""
sort_with_csv.py

Purpose:
  inventory.csv padh kar dataset/unsorted folder ki files ko sahi
  category mein move karta hai:
    - Category D (D.1 - D.7 only = asli termites) -> dataset/pest/
    - Category I (background/plane/wind noise)     -> dataset/no_pest/
    - Baaki (other insects, not termite)            -> dataset/other/ (project ke liye directly use nahi honge)

How to use:
  python sort_with_csv.py
"""

import os
import re
import shutil
import pandas as pd

UNSORTED_DIR = os.path.join("dataset", "unsorted")
PEST_DIR = os.path.join("dataset", "pest")
NO_PEST_DIR = os.path.join("dataset", "no_pest")
OTHER_DIR = os.path.join("dataset", "other")
CSV_FILE = "inventory.csv"

# Termite File IDs (asli termites, headbanging/feeding sounds)
TERMITE_IDS = ["D.1", "D.2", "D.3", "D.4", "D.5", "D.6a", "D.6b", "D.7"]
# Background noise File IDs
NOISE_IDS = ["I.1", "I.2", "I.3", "I.4", "I.5", "I.6", "I.7"]

def normalize(s):
    # File ID jaise "D.4" ko match karne ke liye alag formats try karenge
    # e.g. filename mein "D.4", "D_4", "D-4", "D4" ho sakta hai
    return re.sub(r"[^a-z0-9]", "", s.lower())

def find_file_for_id(file_id, files):
    target = normalize(file_id)
    for f in files:
        if target in normalize(f):
            return f
    return None

def main():
    for d in [PEST_DIR, NO_PEST_DIR, OTHER_DIR]:
        os.makedirs(d, exist_ok=True)

    if not os.path.isdir(UNSORTED_DIR):
        print(f"ERROR: '{UNSORTED_DIR}' nahi mila.")
        return

    df = pd.read_csv(CSV_FILE)
    # Longer File IDs pehle match karo (e.g. "D.10" se pehle "D.1" try na ho)
    df["_id_len"] = df["File ID"].astype(str).str.len()
    df = df.sort_values("_id_len", ascending=False)
    files = os.listdir(UNSORTED_DIR)

    moved = {"pest": 0, "no_pest": 0, "other": 0}
    not_found = []

    for _, row in df.iterrows():
        file_id = str(row["File ID"]).strip()
        match = find_file_for_id(file_id, files)

        if match is None:
            not_found.append(file_id)
            continue

        files.remove(match)  # taake ye file dobara kisi aur ID se match na ho
        src = os.path.join(UNSORTED_DIR, match)

        if file_id in TERMITE_IDS:
            dst = os.path.join(PEST_DIR, match)
            moved["pest"] += 1
        elif file_id in NOISE_IDS:
            dst = os.path.join(NO_PEST_DIR, match)
            moved["no_pest"] += 1
        else:
            dst = os.path.join(OTHER_DIR, match)
            moved["other"] += 1

        shutil.move(src, dst)

    print("Done! Moved:")
    print(f"  pest/     -> +{moved['pest']} files")
    print(f"  no_pest/  -> +{moved['no_pest']} files")
    print(f"  other/    -> +{moved['other']} files")
    print(f"\nCSV mein {len(not_found)} File IDs ke liye matching file nahi mili (filename pattern shayad alag hai).")
    if not_found:
        print("Missing:", not_found[:10], "..." if len(not_found) > 10 else "")

    remaining = os.listdir(UNSORTED_DIR)
    print(f"\n'unsorted' folder mein ab {len(remaining)} files bachi hain (jo CSV mein match nahi hui).")

if __name__ == "__main__":
    main()
