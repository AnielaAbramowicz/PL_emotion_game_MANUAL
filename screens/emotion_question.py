import tkinter as tk
from tkinter import messagebox
from screens.feeling_feedback import FeelingFeedbackScreen
from utils.image_loader import load_image
import time
import tkinter as tk
from tkinter import font as tkFont
from PIL import Image, ImageTk
from tkinter import Label
import os
import sys

# === Color Theme ===
frame_color = "#9090EE"     #purple
bg_color = "#D3EAA6"        # soft pastel green
text_color = "#0E314A"      # dark blue
error_color = "#EFA355"     # soft red
success_color = "#93C47D"       # soft green


class EmotionQuestionScreen:
    def __init__(self, root, game_state):
        self.root = root
        self.label_translation = {
        "angry": "Złość",
        "disgust": "Wstręt",
        "fear": "Strach",
        "happy": "Radość",
        "sad": "Smutek",
        "surprise": "Zaskoczenie"
        }


        self.gs = game_state
        self.emotions = ["Złość", "Wstręt", "Strach", "Radość", "Smutek", "Zaskoczenie"]
        self.time_beg = None

        # Działa zarówno lokalnie, jak i po spakowaniu przez PyInstaller
        base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))

        button_blue_raw = Image.open(os.path.join(base_path, "visualization", "buttom_blue.png")).resize((300, 70))
        self.button_blue = ImageTk.PhotoImage(button_blue_raw)

        button_yellow_raw = Image.open(os.path.join(base_path, "visualization", "buttom_yellow.png")).resize((370, 120))
        self.button_yellow = ImageTk.PhotoImage(button_yellow_raw)

        message_red_raw = Image.open(os.path.join(base_path, "visualization", "mess_red.png")).resize((400, 150))
        self.message_red = ImageTk.PhotoImage(message_red_raw)

        button_purple_raw = Image.open(os.path.join(base_path, "visualization", "button_purple.png")).resize((200, 60))
        self.button_purple = ImageTk.PhotoImage(button_purple_raw)

        flower_left_raw = Image.open(os.path.join(base_path, "visualization", "flower_left.png")).resize((200, 370))
        self.flower_left = ImageTk.PhotoImage(flower_left_raw)

        flower_right_raw = Image.open(os.path.join(base_path, "visualization", "flower_right.png")).resize((200, 370))
        self.flower_right = ImageTk.PhotoImage(flower_right_raw)

        self.difficulty_var = tk.StringVar(value=self.gs.difficulty)
        #self.difficulty_dropdown = tk.OptionMenu(root, self.difficulty_var, "easy", "medium", "hard", command=self.set_difficulty)
        self.main_frame = tk.Frame(root, bg=bg_color)
        self.question_label = tk.Label(self.main_frame, text="", font=("Monocraft", 60), fg=text_color,bg=bg_color )
        self.score_count = tk.Label(self.main_frame,image=self.button_yellow,  text=f"Punkty: {self.gs.score}", font=("Monocraft", 50), fg=text_color,bg=bg_color, compound="center")

        self.image_label = None
        self.button_frame = tk.Frame(self.main_frame, bg=bg_color)
        self.buttons = []

    def render(self):
        self.clear()
        self.time_beg = time.time()
        #self.difficulty_dropdown.place(x=10, y=10)
        self.main_frame.pack(fill=tk.BOTH,expand=True)

        self.main_frame.tkraise()
        
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.image_width = int(screen_width*0.5)
        image_height = int(screen_height*0.4)
        
        self.question_label.config(text="Jaką emocję widzisz?")
        self.score_count.pack(pady=5)
        self.question_label.pack(pady=0)
        row = self.gs.select_next_image()
        img_path = os.path.join(self.gs.dataset_folder, row["filename"])
        img = load_image(img_path, size=(self.image_width,image_height))
                
        img_frame = tk.Frame(self.main_frame, bd=10,relief=tk.RAISED,bg=frame_color)
        img_frame.pack(pady=5)

        self.image_label = tk.Label(img_frame,image=img)
        self.image_label.image = img
        #self.image_label.pack(side=tk.LEFT, padx=(0, 20))
        self.image_label.pack(padx=4,pady=4)

        # round_label = tk.Label(
        #     self.main_frame,
        #     text=f"Round {self.gs.round + 1} / {self.gs.num_questions}",
        #     font=("Pixel Operator 8", 30, "bold"),
        #     fg=text_color,
        #     bg=bg_color,

        # )
        # round_label.place(x=10, y=10)


        flower_label = tk.Label(self.main_frame, image=self.flower_left, bg=bg_color)
        flower_label.image = self.flower_left
        flower_label.place(x=30, rely=0.5, anchor="w")  

        flower_label2 = tk.Label(self.main_frame, image=self.flower_right, bg=bg_color)
        flower_label2.image = self.flower_right
        flower_label2.place(x=screen_width-30-200, rely=0.5, anchor="w") 



        for widget in self.root.place_slaves():
            widget.lift()


        self.button_frame.pack(pady=20)
        # Split buttons into two rows
        row1 = tk.Frame(self.button_frame, bg=bg_color)
        row2 = tk.Frame(self.button_frame, bg=bg_color)
        row1.pack(pady=10)
        row2.pack(pady=10)

        for idx, emo in enumerate(self.emotions):
            btn = Label(
                row1 if idx < 3 else row2,
                image=self.button_blue,
                text=emo,
                compound="center",
                # anchor="center",
                font=("Monocraft", 35),
                fg=text_color,
                bg=bg_color,
                padx=0,
                pady=-10
            )
            btn.image = self.button_blue
            btn.pack(side=tk.LEFT, padx=4)
            btn.bind("<ButtonRelease-1>", lambda e, emotion=emo: self.check_answer(emotion))
            self.buttons.append(btn)


        difficulty_frame = tk.Frame(self.main_frame, bg=bg_color)
        difficulty_frame.place(x=10, y=10)

        title_label = tk.Label(
            difficulty_frame,
            text="SELECT DIFFICULTY",
            font=("Monocraft", 25, "bold"),
            bg=bg_color,
            fg=text_color
        )
        title_label.pack(anchor="w")

        self.difficulty_buttons = {}
        for level in ["randomowy", "łatwy", "średni", "trudny"]:
            btn_frame = tk.Frame(difficulty_frame, bg=frame_color if self.gs.difficulty == level else bg_color, bd=5, relief=tk.RIDGE)
            btn_frame.pack(side=tk.LEFT, padx=5)

            btn = tk.Label(
                btn_frame,
                text=level.upper(),
                font=("Monocraft", 17, "bold"),
                bg=bg_color,
                fg=text_color,
                padx=10,
                pady=5
            )
            btn.pack()
            btn.bind("<ButtonRelease-1>", lambda e, lvl=level: self.set_difficulty(lvl))
            self.difficulty_buttons[level] = btn_frame
            
    def translation(self, emotion):
        if emotion == "angry":
            emotion = "złość"
        elif emotion == "disgust":
            emotion = "Wstręt"
        elif emotion == "fear":
            emotion = "Strach"
        elif emotion == "happy":
            emotion = "Radość"
        elif emotion == "sad":
            emotion = "Smutek"
        elif emotion == "surprise":
            emotion = "Zaskoczenie"


        return emotion
        



    def set_difficulty(self, level):
        self.gs.set_difficulty(level)
        self.selected_difficulty = level

        # Update frame backgrounds to reflect selection
        for lvl, frame in self.difficulty_buttons.items():
            frame.config(bg=frame_color if lvl == level else bg_color)

        # Load and show new image
        row = self.gs.select_next_image()

        self.update_image(row)







    def update_image(self, row):
        # Load the image
        image_path = os.path.join(self.gs.dataset_folder, row["filename"])

        image_height = int(self.root.winfo_screenheight() * 0.4)
        img = Image.open(image_path).resize((self.image_width, image_height))
        photo = ImageTk.PhotoImage(img)

        # Update image label
        self.image_label.configure(image=photo)
        self.image_label.image = photo  # Keep reference


    def check_answer(self, selected):
        correct_label = self.gs.df.iloc[self.gs.current_index]["folder_label"].lower()
        correct_label = self.translation(correct_label)
        self.gs.round += 1
        
        correctness = 1 if selected.lower() == correct_label.lower() else 0
        if correctness:
            self.gs.score +=1
      
         
        filename = self.gs.df.iloc[self.gs.current_index]["filename"]
        self.gs.shown_filenames.append(filename)
        
        time_spent = time.time() - self.time_beg
        self.gs.currect_correctness.append(correctness)
        self.gs.current_respond_time.append(time_spent)

        with open(os.path.join(self.gs.session_folder,"questions_times.txt"), "a") as f:
            f.write(f"{time_spent:.2f} seconds, correctness: {correctness}\n")

        self.show_feedback(correctness, correct_label.capitalize())
        self.gs.last_img_path = os.path.join(
            self.gs.dataset_folder,
            self.gs.df.iloc[self.gs.current_index]['filename']
        )

    def show_feedback(self, correctness, correct_answer):
        self.button_frame.pack_forget()

        is_correct = correctness == 1
        bg_color = success_color if correctness == 1 else error_color




        # Container to center the feedback box
        container = tk.Frame(self.main_frame, bg=self.main_frame["bg"])
        container.pack(pady=10)

        # Box that mimics image width and has padding
        self.feedback_frame = tk.Frame(container,width=self.image_width, padx=40, pady=20, bd=10, relief=tk.GROOVE, bg=bg_color)

        # self.feedback_frame = tk.Label(container,
        #                                bg= bg_color, width=400, height=150, compound="center")
        # self.feedback_frame.image = self.message_red
        self.feedback_frame.pack()
        translated = self.label_translation.get(correct_answer.lower(), correct_answer)
        msg = (
            "Twoja odpowiedź jest poprawna!\nGratulacje! Spróbujmy kolejnej!"
            if is_correct else
            f"Twoja odpowiedź jest niepoprawna.\nDasz radę!\nPoprawna odpowiedź to: {translated}"

        )
        label = tk.Label(
            self.feedback_frame,
            text=msg,
            font=("Monocraft", 19),
            bg=bg_color,
            fg=text_color,  # dark blue
            justify="center",
            wraplength=600
        )
        label.pack(pady=5)

        btn = tk.Label(
            self.feedback_frame, image= self.button_purple,
            text="Następne pytanie",
            compound="center",
            font=("Monocraft", 16, "bold"),
            fg = text_color,
            bg=bg_color, 
        )
        btn.image = self.button_purple
        btn.bind("<ButtonRelease-1>", lambda e: self. proceed_after_feedback())
        btn.pack(pady=5)


    def proceed_after_feedback(self):
        self.feedback_frame.destroy()
        self.clear()


        # Log difficulty for each round
        with open(os.path.join(self.gs.session_folder, "selected_difficulty.txt"), "a") as f:
            f.write(f"Round {self.gs.round } - Final selected difficulty: {self.gs.difficulty}\n")



        from screens.feeling_feedback import FeelingFeedbackScreen
        FeelingFeedbackScreen(self.root, self.gs).render()


    def clear(self):
        self.main_frame.pack_forget()
        for btn in self.buttons:
            btn.destroy()
        self.buttons.clear()