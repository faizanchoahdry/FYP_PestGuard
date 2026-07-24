"""
augment_dataset.py

Purpose:
  Chunke asal dataset chota hai (13 files), ye script har audio file se
  naye "augmented" versions banata hai taake dataset size badhe:
    1. Pitch shift (awaaz ka pitch thora upar/neeche)
    2. Noise addition (halka background noise mila kar)
    3. Time stretch (thora fast/slow kar ke)

  Ye standard ML technique hai jab real data limited ho -- ise
  "data augmentation" kehte hain. Model isse zyada robust seekhta hai,
  sirf ek exact recording "yaad" nahi karta (overfitting kam hota hai).

How to use:
  python augment_dataset.py
"""

import os
import random
import numpy as np
import librosa
import soundfile as sf

DATASET_FOLDER = "dataset"
CLASSES = ["pest", "no_pest"]
SR = 22050  # sab files isi sample rate pe standardize honge

def pitch_shift(y, sr, n_steps):
    return librosa.effects.pitch_shift(y=y, sr=sr, n_steps=n_steps)

def add_noise(y, noise_level=0.005):
    noise = np.random.randn(len(y))
    return y + noise_level * noise

def time_stretch(y, rate):
    return librosa.effects.time_stretch(y=y, rate=rate)

def main():
    total_created = 0

    for label in CLASSES:
        folder = os.path.join(DATASET_FOLDER, label)
        if not os.path.isdir(folder):
            print(f"WARNING: {folder} nahi mila, skip kar raha hoon.")
            continue

        # Sirf original files pe kaam karo (jo pehle se augmented hain unko dubara skip karo)
        original_files = [f for f in os.listdir(folder)
                           if f.lower().endswith(".wav") and "_aug" not in f]

        print(f"\n{label}: {len(original_files)} original files mili, augmenting...")

        for fname in original_files:
            fpath = os.path.join(folder, fname)
            base_name = os.path.splitext(fname)[0]

            try:
                y, sr = librosa.load(fpath, sr=SR)

                # 1. Pitch shift up
                y_pitch_up = pitch_shift(y, sr, n_steps=2)
                sf.write(os.path.join(folder, f"{base_name}_aug_pitchup.wav"), y_pitch_up, sr)

                # 2. Pitch shift down
                y_pitch_down = pitch_shift(y, sr, n_steps=-2)
                sf.write(os.path.join(folder, f"{base_name}_aug_pitchdown.wav"), y_pitch_down, sr)

                # 3. Noise added
                y_noise = add_noise(y)
                sf.write(os.path.join(folder, f"{base_name}_aug_noise.wav"), y_noise, sr)

                # 4. Time stretch (thora tez)
                y_fast = time_stretch(y, rate=1.15)
                sf.write(os.path.join(folder, f"{base_name}_aug_fast.wav"), y_fast, sr)

                # 5. Time stretch (thora slow)
                y_slow = time_stretch(y, rate=0.85)
                sf.write(os.path.join(folder, f"{base_name}_aug_slow.wav"), y_slow, sr)

                total_created += 5
                print(f"  {fname} -> 5 naye versions bana diye")

            except Exception as e:
                print(f"  Skip {fname}: {e}")

    print(f"\nDone! Total {total_created} naye augmented files banaye gaye.")
    print("Ab dataset/pest aur dataset/no_pest folders check karein -- files kaafi zyada ho jayengi.")

if __name__ == "__main__":
    main()