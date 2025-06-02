import pandas as pd
import random
import sys, os

# === Color Theme ===
frame_color = "#9090EE"     #purple
bg_color = "#D3EAA6"        # soft pastel green
text_color = "#0E314A"      # dark blue
error_color = "#EFA355"     # soft red
success_color = "#93C47D"       # soft green

class GameState:
    def __init__(self, root, num_questions, session_folder):
        self.session_folder = session_folder
        self.root = root

        base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))

        self.csv_path = os.path.join(base_path, "dataset_CK", "ck_emotion_difficulty.csv")
        self.dataset_folder = os.path.join(base_path, "dataset_CK", "ck_images")
        self.df = pd.read_csv(self.csv_path)

        self.num_questions = num_questions  

        self.full_df = pd.read_csv(self.csv_path).reset_index(drop=True)
        self.df = self.full_df.copy() 
        self.df["shown"] = False  # Reset shown status 
        self.df = self.df[self.df["shown"] == False].reset_index(drop=True)
        self.shown_filenames = []
      
        self.emotion_prob = {"Angry" : 1/6, "Disgust": 1/6, "Fear": 1/6, "Happy": 1/6, "Sad": 1/6,"Surprise": 1/6}
    
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
        avaible = self.df[self.df["shown"] == False]
        if avaible.empty:
            avaible = self.full_df.copy()
        idx = random.choice(avaible.index)
        row = avaible.loc[idx]

        self.df.at[idx, "shown"] = True
        self.shown_filenames.append(row["filename"])
        self.current_index = idx
        
        return row 


    def set_difficulty(self, level, manual= False):
        self.current_index = 0 
             
        self.difficulty = level
        df_full = self.full_df.copy()
        df_full = df_full[~df_full["filename"].isin(self.shown_filenames)].reset_index(drop=True)

        length = len(df_full)

        if level == "easy":
            self.df = df_full.sort_values(by="difficulty").iloc[:int(length * 0.33)].reset_index(drop=True)
        elif level == "medium":
            self.df = df_full.sort_values(by="difficulty").iloc[int(length * 0.33):int(length * 0.66)].reset_index(drop=True)
        elif level == "hard":
            self.df = df_full.sort_values(by="difficulty").iloc[int(length * 0.66):].reset_index(drop=True)

        self.current_index = len(self.df) // 2
