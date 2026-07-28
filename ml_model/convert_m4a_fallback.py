import os
import sys
from pydub import AudioSegment

folder_name = sys.argv[1] if len(sys.argv) > 1 else "rodent"
FOLDER = os.path.join("dataset", folder_name)

def main():
    if not os.path.isdir(FOLDER):
        print(f"ERROR: {FOLDER} nahi mila.")
        return

    for fname in os.listdir(FOLDER):
        if not fname.lower().endswith(".m4a"):
            continue

        fpath = os.path.join(FOLDER, fname)
        name = os.path.splitext(fname)[0]
        new_path = os.path.join(FOLDER, f"{name}.wav")

        try:
            audio = AudioSegment.from_file(fpath, format="m4a")
            audio.export(new_path, format="wav")
            os.remove(fpath)
            print(f"Converted: {fname} -> {name}.wav")
        except Exception as e:
            print(f"FAILED: {fname} -- {e}")
            print("Ffmpeg install hona zaroori hai. Neeche instructions dekhein.")

if __name__ == "__main__":
    main()