"""
convert_to_wav.py

Purpose:
  dataset/termite folder mein agar .mp3 (ya doosre formats) files hain,
  unhe sab .wav mein convert karta hai -- taake baaki scripts
  (extract_features.py, augment_dataset.py) ke sath consistent rahein.

How to use:
  python convert_to_wav.py
"""

import os
import librosa
import soundfile as sf

FOLDER = os.path.join("dataset", "termite")
TARGET_SR = 22050

def main():
    if not os.path.isdir(FOLDER):
        print(f"ERROR: {FOLDER} nahi mila.")
        return

    converted = 0
    skipped = 0

    for fname in os.listdir(FOLDER):
        fpath = os.path.join(FOLDER, fname)
        name, ext = os.path.splitext(fname)
        ext = ext.lower()

        if ext == ".wav":
            skipped += 1
            continue

        if ext not in [".mp3", ".m4a", ".ogg", ".flac", ".aac"]:
            print(f"  Skip (unknown format): {fname}")
            continue

        try:
            y, sr = librosa.load(fpath, sr=TARGET_SR)
            new_path = os.path.join(FOLDER, f"{name}.wav")
            sf.write(new_path, y, sr)
            os.remove(fpath)  # purani file (mp3 wagera) hata do
            print(f"  Converted: {fname} -> {name}.wav")
            converted += 1
        except Exception as e:
            print(f"  ERROR converting {fname}: {e}")

    print(f"\nDone! {converted} files converted, {skipped} already .wav thi.")

if __name__ == "__main__":
    main()