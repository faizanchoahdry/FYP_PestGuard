import os
import shutil

RAW_FOLDER = "InsectSounds"
OUTPUT_FOLDER = "dataset"

PEST_KEYWORDS = ["termite", "coptotermes", "reticulitermes", "isoptera"]
NO_PEST_KEYWORDS = ["background", "noise", "plane", "wind", "empty"]

def main():
    pest_dir = os.path.join(OUTPUT_FOLDER, "pest")
    no_pest_dir = os.path.join(OUTPUT_FOLDER, "no_pest")
    unsorted_dir = os.path.join(OUTPUT_FOLDER, "unsorted")

    for d in [pest_dir, no_pest_dir, unsorted_dir]:
        os.makedirs(d, exist_ok=True)

    if not os.path.isdir(RAW_FOLDER):
        print(f"ERROR: '{RAW_FOLDER}' folder nahi mila. RAW_FOLDER path check karein.")
        return

    count = {"pest": 0, "no_pest": 0, "unsorted": 0}

    for root, _, files in os.walk(RAW_FOLDER):
        for fname in files:
            if not fname.lower().endswith(".wav"):
                continue

            lower_name = fname.lower()
            src_path = os.path.join(root, fname)

            if any(k in lower_name for k in PEST_KEYWORDS):
                dst = os.path.join(pest_dir, fname)
                count["pest"] += 1
            elif any(k in lower_name for k in NO_PEST_KEYWORDS):
                dst = os.path.join(no_pest_dir, fname)
                count["no_pest"] += 1
            else:
                dst = os.path.join(unsorted_dir, fname)
                count["unsorted"] += 1

            shutil.copy2(src_path, dst)

    print("Done! File counts:")
    print(f"  pest/     -> {count['pest']} files")
    print(f"  no_pest/  -> {count['no_pest']} files")
    print(f"  unsorted/ -> {count['unsorted']} files (inventory CSV dekh kar manually classify karein)")

if __name__ == "__main__":
    main()