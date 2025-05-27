import pandas as pd
import numpy as np
import os
from PIL import Image
from tqdm import tqdm

# === SETTINGS ===
input_csv = "/Users/anielamac/Desktop/thesis/dataset CK/ckextended.csv"  # path to the input file
output_img_dir = "ck_images"  # folder for images
output_csv = "ck_converted_for_game.csv"  # converted csv path

# === EMOTION MAPPING ===
emotion_map = {
    0: "Angry",
    1: "Disgust",
    2: "Fear",
    3: "Happy",
    4: "Sad",
    5: "Surprise",
    6: "Neutral",
    7: "Contempt"
}

# === PREPARE OUTPUT DIR ===
os.makedirs(output_img_dir, exist_ok=True)

# === LOAD CSV ===
df = pd.read_csv(input_csv)

# === PROCESS AND SAVE IMAGES ===
image_paths = []
emotions = []

print("Converting pixel strings to images...")
for i, row in tqdm(df.iterrows(), total=len(df)):
    try:
        pixels = np.array(row['pixels'].split(), dtype=np.uint8).reshape(48, 48)
        emotion_label = emotion_map.get(row['emotion'], "Unknown")
        filename = f"ck_{i:04d}.png"
        img_path = os.path.join(output_img_dir, filename)

        Image.fromarray(pixels).save(img_path)

        image_paths.append(filename)
        emotions.append(emotion_label)

    except Exception as e:
        print(f"Error on row {i}: {e}")

# === SAVE NEW CSV ===
converted_df = pd.DataFrame({
    "filename": image_paths,
    "emotion": emotions,
    "difficulty": [0.5] * len(image_paths)  # default medium difficulty
})

converted_df.to_csv(output_csv, index=False)
print(f"\nSaved {len(converted_df)} images and CSV to:")
print(f"- Images: {output_img_dir}")
print(f"- CSV: {output_csv}")
