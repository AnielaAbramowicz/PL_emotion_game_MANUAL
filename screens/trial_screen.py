import tkinter as tk
import time
from PIL import Image, ImageTk
from screens.emotion_question import EmotionQuestionScreen
from utils.image_loader import load_image

# === Color Theme ===
frame_color = "#9090EE"     #purple
bg_color = "#D3EAA6"        # soft pastel green
text_color = "#0E314A"      # dark blue
error_color = "#EFA355"     # soft red
success_color = "#93C47D"       # soft green

class TrialScreen:
    def __init__(self, root, game_state):
        self.root = root
        self.gs = game_state
        self.emotions = ["Złość", "Wstręt", "Strach", "Radość", "Smutek", "Zaskoczenie"]
        self.time_beg = None

        self.main_frame = tk.Frame(root, bg=bg_color)
        self.button_frame = tk.Frame(self.main_frame, bg=bg_color)
        self.buttons = []

        button_yellow_raw = Image.open("/Users/anielamac/Desktop/thesis/visualization/buttom_yellow.png").resize((380, 120))
        self.button_yellow = ImageTk.PhotoImage(button_yellow_raw)

        flower_left_raw = Image.open("/Users/anielamac/Desktop/thesis/visualization/flower_left.png").resize((200,370))
        self.flower_left = ImageTk.PhotoImage(flower_left_raw)

        flower_right_raw = Image.open("/Users/anielamac/Desktop/thesis/visualization/flower_right.png").resize((200,370))
        self.flower_right = ImageTk.PhotoImage(flower_right_raw)

        self.correct_answer = "Radość"
        self.image_path = "/Users/anielamac/Desktop/thesis/visualization/trail_image.jpg"

        self.score_count = tk.Label(self.main_frame,image=self.button_yellow,  text=f"Punkty: {self.gs.score}", font=("Monocraft", 50), fg=text_color,bg=bg_color, compound="center")

        button_red = ImageTk.PhotoImage(Image.open("/Users/anielamac/Desktop/thesis/visualization/buttom_red.png").resize((200, 60)))

        end_button = tk.Label(
            self.main_frame,
            image=button_red,
            text="ZAKOŃCZ",
            compound="center",
            font=("Monocraft", 20, "bold"),
            fg=text_color,
            bg=bg_color
        )
        end_button.image = button_red
        end_button.place(relx=1.0, x=-10, y=10, anchor="ne")
        end_button.bind("<Button-1>", lambda e: self.root.quit())  # or link to summary screen if you prefer


        self.button_blue = ImageTk.PhotoImage(Image.open("/Users/anielamac/Desktop/thesis/visualization/buttom_blue.png").resize((330, 70)))
        self.button_purple = ImageTk.PhotoImage(Image.open("/Users/anielamac/Desktop/thesis/visualization/button_purple.png").resize((200, 60)))

    def render(self):
        self.time_beg = time.time()
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.score_count.pack(pady=0)

        question_label = tk.Label(self.main_frame, text="Jaką emocję widzisz?", font=("Monocraft", 65), fg=text_color, bg=bg_color)
        question_label.pack(pady=0)

        image = load_image(self.image_path, size=(600, 400))
        img_frame = tk.Frame(self.main_frame, bd=10, relief=tk.RAISED, bg=frame_color)
        img_frame.pack(pady=0)
        self.image_label = tk.Label(img_frame, image=image)
        self.image_label.image = image
        self.image_label.pack(padx=4, pady=0)

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        round_label = tk.Label(
            self.main_frame,
            text=f"Runda 1 / {self.gs.num_questions}",
            font=("Monocraft", 30, "bold"),
            fg=text_color,
            bg=bg_color,

        )
        round_label.place(x=10,y=10)

        
        flower_label = tk.Label(self.main_frame, image=self.flower_left, bg=bg_color)
        flower_label.image = self.flower_left
        flower_label.place(x=30, rely=0.5, anchor="w")  

        flower_label2 = tk.Label(self.main_frame, image=self.flower_right, bg=bg_color)
        flower_label2.image = self.flower_right
        flower_label2.place(x=screen_width-30-200, rely=0.5, anchor="w") 




        self.button_frame.pack(pady=20)
        row1 = tk.Frame(self.button_frame, bg=bg_color)
        row2 = tk.Frame(self.button_frame, bg=bg_color)
        row1.pack(pady=10)
        row2.pack(pady=10)

        for idx, emo in enumerate(self.emotions):
            btn = tk.Label(
                row1 if idx < 3 else row2,
                image=self.button_blue,
                text=emo,
                #justify=tk.CENTER,
                compound="center",
                #anchor=tk.CENTER,
                font=("Monocraft", 35),
                fg=text_color,
                bg=bg_color,
                padx=0,
                pady=0
            )
            btn.image = self.button_blue
            btn.pack(side=tk.LEFT, padx=4)
            btn.bind("<Button-1>", lambda e, emotion=emo: self.check_answer(emotion))
            self.buttons.append(btn)

        # for idx, emo in enumerate(self.emotions):
        #     btn = tk.Label(
        #         row1 if idx < 3 else row2,
                
        #         text=emo,
        #         compound="center",
        #         # anchor="center",
        #         font=("Monocraft", 28),
        #         fg=text_color,
        #         bg=bg_color,
        #         padx=0,
        #         pady=-10
        #     )


    def check_answer(self, selected):
        print(f"selected  {selected}")
        print(f"cerrecet answer  {self.correct_answer}")
        is_correct = selected.lower() == self.correct_answer.lower()
        self.show_feedback(is_correct)

    def show_feedback(self, is_correct):
        self.button_frame.pack_forget()
        color = success_color if is_correct else error_color

        container = tk.Frame(self.main_frame, bg=bg_color)
        container.pack(pady=10)

        self.feedback_frame = tk.Frame(container, width=600, padx=40, pady=20, bd=10, relief=tk.GROOVE, bg=color)
        self.feedback_frame.pack()

        msg = (
            "Poprawnie! Świetna robota!\nJesteś gotów, by zacząć grę!"
            if is_correct else
            f"Ups, to była zła odpowiedź.\nPoprawna odpowiedź to: {self.correct_answer.capitalize()}."
        )
        label = tk.Label(self.feedback_frame, text=msg, font=("Monocraft", 19), bg=color, fg=text_color, justify="center", wraplength=590)
        label.pack(pady=0)

        btn = tk.Label(
            self.feedback_frame,
            image=self.button_purple,
            text="Zakończ rundę",
            compound="center",
            font=("Monocraft", 16, "bold"),
            fg=text_color,
            bg=color
        )
        btn.image = self.button_purple
        btn.bind("<Button-1>", lambda e: self.proceed_to_game())
        btn.pack(pady=5)

    def proceed_to_game(self):
        self.main_frame.pack_forget()
        from screens.start_game import StartGame
        StartGame(self.root, self.gs).render()
