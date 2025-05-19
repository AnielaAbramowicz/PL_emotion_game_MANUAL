import tkinter as tk
from screens.reason_feedback import ReasonFeedbackScreen
import time
import tkinter as tk
from tkinter import font as tkFont
from PIL import Image, ImageTk
from tkinter import Label
import os


frame_color = "#9090EE"     #purple
bg_color = "#D3EAA6"        # soft pastel green
text_color = "#0E314A"      # dark blue

class FeelingFeedbackScreen:
    def __init__(self, root, game_state):
        self.root = root
        self.gs = game_state
        self.feelings = ["Zaniepokojony 😰", "Znudzony 😐", "Neutralny 🙂", "Zainteresowanie 🤔"]
        self.time_beg = None
        self.root.configure(bg= bg_color)

        button_orange_raw = Image.open("/Users/anielamac/Desktop/thesis/visualization/button_purple2.png").resize((450, 150))
        self.button_orange = ImageTk.PhotoImage(button_orange_raw)

        flower_left_raw = Image.open("/Users/anielamac/Desktop/thesis/visualization/flower_left.png").resize((200,370))
        self.flower_left = ImageTk.PhotoImage(flower_left_raw)

        flower_right_raw = Image.open("/Users/anielamac/Desktop/thesis/visualization/flower_right.png").resize((200,370))
        self.flower_right = ImageTk.PhotoImage(flower_right_raw)
        
        self.label = tk.Label(root, text="Jak się teraz czujesz?", font=("Monocraft", 35), bg= bg_color, fg=text_color)
        self.frame = tk.Frame(root, bg=bg_color)
        self.buttons = []

    def render(self):
        self.clear()
        self.label.config(font=("Monocraft",60 ))



        self.label.pack(pady=100)
        self.frame.pack(pady=15)

        self.time_beg  = time.time()

        for idx,feeling in enumerate(self.feelings):
            row = idx //2
            col = idx % 2
            btn = tk.Label(self.frame,image=self.button_orange, text=feeling,compound="center", font=("Monocraft", 35),padx= 5, pady= 5,bg=bg_color,  fg=text_color )
            btn.image = self.button_orange
            btn.bind("<Button-1>", lambda e, f=feeling: self.handle_choice(f))
            btn.grid(row=row, column=col, padx=30,pady=20)

            self.buttons.append(btn)

        screen_width = self.root.winfo_screenwidth()

        flower_label = tk.Label(self.root, image=self.flower_left, bg=bg_color)
        flower_label.image = self.flower_left
        flower_label.place(x=30, rely=0.5, anchor="w")  

        flower_label2 = tk.Label(self.root, image=self.flower_right, bg=bg_color)
        flower_label2.image = self.flower_right
        flower_label2.place(x=screen_width-30-200, rely=0.5, anchor="w") 


    def handle_choice(self, feeling):
        self.gs.feedback["feeling"] = feeling
        translation_dict = {
            "Zaniepokojony": "Anxious",
            "Znudzony": "Bored",
            "Neutralny": "Neutral",
            "Zainteresowanie": "Joy/Interest"
        }


        # extract base word without emoji
        base = feeling.split()[0]  # e.g., "Zaniepokojony 😰" → "Zaniepokojony"
        english_label = translation_dict.get(base, "Unknown")
        
        if "Znudzony" in feeling:
            score = 1
        elif "Zaniepokojony" in feeling:
            score = -1
        else:
            score = 0     
        self.gs.currect_feeliing.append(score)

        time_spent = time.time() - self.time_beg
        with open(os.path.join(self.gs.session_folder, "feeling_answers.txt"), "a") as f:
            f.write(f"{time_spent:.2f} seconds - Feeling: {english_label}\n")
        
        self.clear()
        ReasonFeedbackScreen(self.root, self.gs).render()

    def clear(self):
        self.label.pack_forget()
        self.frame.pack_forget()
        for btn in self.buttons:
            btn.destroy()
        self.buttons.clear()
