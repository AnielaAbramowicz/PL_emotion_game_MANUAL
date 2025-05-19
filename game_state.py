import pandas as pd
import random
import os


class GameState:
    def __init__(self, root, num_questions, session_folder):
        self.session_folder = session_folder
        self.root = root
        # self.csv_path = "/Users/anielamac/Desktop/thesis/face recognition + difficulty/all_emotions_difficulty_sorted.csv"
        # self.dataset_folder = "/Users/anielamac/Desktop/thesis/face recognition + difficulty/my_own_dataset"
        self.csv_path = "/Users/anielamac/Desktop/thesis/dataset CK/ck_emotion_difficulty.csv"
        self.dataset_folder = "/Users/anielamac/Desktop/thesis/dataset CK/ck_images"

        #self.csv_path = "/Users/anielamac/Desktop/thesis/dataset CK/ck_converted_for_game.csv"
        #self.dataset_folder = "/Users/anielamac/Desktop/thesis/dataset CK/ck_images"
        
        self.df = pd.read_csv(self.csv_path)
        #print(self.df.head())

        self.num_questions = num_questions  



        self.full_df = pd.read_csv(self.csv_path).reset_index(drop=True)
        self.df["shown"] = False  # Reset shown status 
        self.df = self.df[self.df["shown"] == False].reset_index(drop=True)
        self.shown_filenames = []
       # self.df = self.full_df.copy()

        self.emotion_prob = {"Angry" : 1/6, "Disgust": 1/6, "Fear": 1/6, "Happy": 1/6, "Sad": 1/6,"Surprise": 1/6}
    
        self.emotion_suppression = {
            "Angry": 0,
            "Disgust": 0,
            "Fear": 0,
            "Happy": 0,
            "Sad": 0,
            "Surprise": 0 
        }

        self.currect_score = []
        self.current_respond_time = []
        self.currect_correctness = []
        self.currect_feeliing = []

        self.manual_difficulty = None  # “easy”, “medium”, “hard”, or None
        #self.manual_override_rounds = 0  # how many rounds we pause adaptation


        self.current_index = len(self.df) // 2
        self.score = 0
        self.round = 0
        self.max_rounds = 5
        self.shown_indices = []
        self.stage = "emotion_question"
        self.feedback = {"feeling": None}
        self.difficulty = "medium"  # default difficulty
        self.end_callback = None  # to be set in main


    def select_next_image(self):
        performance = sum(self.currect_score) / len(self.currect_score) if self.currect_score else 0.5
        last_difficulty = getattr(self, "last_difficulty", 0.5)

        # New: adjust center slightly based on performance
        if performance < 0.5:
            center = max(0.0, last_difficulty - 0.1)  # back off
        elif performance > 0.7:
            center = min(1.0, last_difficulty + 0.05)  # increase slowly
        else:
            center = last_difficulty  # hold steady

        # Difficulty adjustment window
        min_scale, max_scale = 0.1, 0.2
        growth_rounds = 5
        change_factor = min_scale + (max_scale - min_scale) * min(self.round, growth_rounds) / growth_rounds
        low, high = center, min(1.0, performance * change_factor + center)

        # Filter images in current range and not yet shown
        candidates = self.df[
            (self.df["difficulty"] >= low) &
            (self.df["difficulty"] <= high) &
            (~self.df["filename"].isin(self.shown_filenames))
        ].copy()

        # If no candidates, fallback to full range (excluding shown)
        if candidates.empty:
            candidates = self.df[~self.df["filename"].isin(self.shown_filenames)].copy()

        # Identify emotions actually available in the candidates
        available_emotions = candidates["folder_label"].str.title().unique()
        available_emotions = [e for e in available_emotions if e in self.emotion_prob]

        if not available_emotions:
            raise ValueError("No available emotions found in current difficulty range!")

        # Build normalized probabilities only for available emotions
        filtered_probs = {e: self.emotion_prob[e] for e in available_emotions}
        total = sum(filtered_probs.values())
        if total == 0:
            filtered_probs = {e: 1 / len(filtered_probs) for e in filtered_probs}
        else:
            filtered_probs = {e: p / total for e, p in filtered_probs.items()}

        # Try sampling only from candidates that match the chosen emotion
        for _ in range(30):  # retry a few times
            emotion_choice = random.choices(list(filtered_probs.keys()), list(filtered_probs.values()))[0]
            matching = candidates[candidates["folder_label"].str.title() == emotion_choice]
            if not matching.empty:
                break
            print("need to find new picture ")
        else:
            raise ValueError("No valid image found for any emotion in candidates.")
        


        chosen_row = matching.sample(1).iloc[0]

        # Mark image as shown
        self.df.at[self.df[self.df["filename"] == chosen_row["filename"]].index[0], "shown"] = True
        self.shown_filenames.append(chosen_row["filename"])
        self.last_difficulty = chosen_row["difficulty"]
        self.current_index = self.df[self.df["filename"] == chosen_row["filename"]].index[0]

        # Log
        current_score = self.currect_score[-1] if self.currect_score else 0.0
        with open(os.path.join(self.session_folder, "difficulty.txt"), "a") as f:
            f.write(
                f"Round {self.round} - Center: {center:.3f},Current Score: {current_score:.3f}, Performance: {performance:.3f}, "
                f"Factor: {change_factor:.3f}, New low-high: ({low:.3f}-{high:.3f}), "
                f"Chosen Emotion: {emotion_choice}, Selected Difficulty: {self.last_difficulty:.3f}\n"
            )


        return chosen_row


    def update_emotion_probabilities(self):
        base_emotions = list(self.emotion_prob.keys())
        total_weight = 0.0
        temp_probs = {}

        for emo in base_emotions:
            stage = self.emotion_suppression.get(emo, 0)
            if stage == 0:
                prob = 1/6
            elif stage == 1:
                prob = 0.0
            elif stage == 2:
                prob = 0.05
            elif stage == 3:
                prob = 0.10
            elif stage >= 4:
                prob = 1/6
                self.emotion_suppression[emo] = 0  # Reset after restoration
            temp_probs[emo] = prob
            total_weight += prob

        # Normalize probabilities so they sum to 1
        for emo in base_emotions:
            if total_weight > 0:
                self.emotion_prob[emo]= temp_probs[emo]/ total_weight
            else:
                self.emotion_prob[emo]= 1/len(base_emotions)

        # Advance suppression stages where needed
        for emo in base_emotions:
            if 1 <= self.emotion_suppression[emo] <= 3:
                self.emotion_suppression[emo] += 1

        # Log current state to file
        with open(os.path.join(self.session_folder, "emotion_probabilities.txt"), "a") as f:
            f.write(f"Round {self.round} | Emotion Probabilities:\n")
            for emo in base_emotions:
                f.write(f"  {emo}: {self.emotion_prob[emo]:.3f} (stage {self.emotion_suppression[emo]})\n")
            f.write("\n")
