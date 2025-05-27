import tkinter as tk
import time
from screens.emotion_question import EmotionQuestionScreen
from PIL import Image, ImageTk
from screens.trial_screen import TrialScreen
import sys, os

frame_color = "#9090EE"     #purple
bg_color = "#D3EAA6"        # soft pastel green
text_color = "#0E314A"      # dark blue


class StartGame:
    def __init__(self, root, game_state):
        self.root = root
        self.gs = game_state
        self.root.configure(bg=bg_color)

        self.main_frame = tk.Frame(root, bg=bg_color)


        base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))

        flower_left_raw = Image.open(os.path.join(base_path, "visualization", "flower_left.png")).resize((200, 370))
        self.flower_left = ImageTk.PhotoImage(flower_left_raw)

        flower_right_raw = Image.open(os.path.join(base_path, "visualization", "flower_right.png")).resize((200, 370))
        self.flower_right = ImageTk.PhotoImage(flower_right_raw)

        button_green_raw = Image.open(os.path.join(base_path, "visualization", "button_purple.png")).resize((400, 160))
        self.button_green = ImageTk.PhotoImage(button_green_raw)

        self.label = tk.Label(
            self.main_frame,
            text="Świetna robota!\nZaczynamy grę!",
            font=("Monocraft", 80),
            bg=bg_color,
            fg=text_color,
            wraplength=1000,
            justify="center"
        )

        self.label2 = tk.Label(
            self.main_frame,
            text=f"Zobaczysz {self.gs.num_questions} pytań! Gotowy? \n Kliknij przycisk poniżej! Stoper zaczyna odliczanie!",
            font=("Monocraft", 40),
            bg=bg_color,
            fg=text_color,
            wraplength=1000,
            justify="center"
        )

        self.start_button = tk.Label(
            self.main_frame,
            image=self.button_green,
            text="Start",
            compound="center",
            font=("Monocraft", 50, "bold"),
            fg=text_color,
            bg=bg_color
        )
        self.start_button.image = self.button_green
        self.start_button.bind("<ButtonPress-1>", lambda e: self.start_game())

    def render(self):
        self.main_frame.pack(fill="both", expand=True)
        self.label.pack(pady=130)
        self.label2.pack(pady=0)
        self.start_button.pack(pady=0)

        screen_width = self.root.winfo_screenwidth()

        flower_label = tk.Label(self.root, image=self.flower_left, bg=bg_color)
        flower_label.image = self.flower_left
        flower_label.place(x=30, rely=0.5, anchor="w")  

        flower_label2 = tk.Label(self.root, image=self.flower_right, bg=bg_color)
        flower_label2.image = self.flower_right
        flower_label2.place(x=screen_width-30-200, rely=0.5, anchor="w") 

    def start_game(self):
        self.gs.start_time = time.time()
        self.main_frame.pack_forget()
        EmotionQuestionScreen(self.root, self.gs).render()

