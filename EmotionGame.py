from tkinter import Tk, simpledialog
import tkinter
from game_state import GameState
from screens.emotion_question import EmotionQuestionScreen
from screens.summary import SummaryScreen
import tkinter as tk
from tkinter import font as tkFont
import sys
from tkinter import font as tkFont
from PIL import Image, ImageTk
from tkinter import Label
from screens.start_trail import StartTrail
import os
from datetime import datetime
import pathlib

MAIN_FOLDER_DEFAULT = pathlib.Path(__file__).parent.absolute()
VISUALIZATION_FOLDER = os.path.join(MAIN_FOLDER_DEFAULT, 'visualization')

frame_color = "#9090EE"  # purple
bg_color = "#D3EAA6"  # soft pastel green
text_color = "#0E314A"  # dark blue

if __name__ == "__main__":
    # Create timestamped session folder
    print(MAIN_FOLDER_DEFAULT)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    session_folder = os.path.join("sessions", timestamp)
    os.makedirs(session_folder, exist_ok=True)

    root = Tk()
    root.withdraw()
    # Collect basic user info
    age = simpledialog.askstring("Informacje o użytkowniku", "Podaj swój wiek:")
    if age is None:
        root.quit()
        root.destroy()
        sys.exit(0)

    gender = simpledialog.askstring(
        "Informacje o użytkowniku", "Podaj swoją płeć (Mężczyzna / Kobieta / Wolę nie podawać):"
    )
    if gender is None:
        root.quit()
        root.destroy()
        sys.exit(0)

    with open(os.path.join(session_folder, "user_info.txt"), "w") as f:
        f.write(f"Age: {age}\nGender: {gender}\n")

    # print(tkFont.families())
    image_path = os.path.join(VISUALIZATION_FOLDER, 'buttom_red.png')
    buttom_red = Image.open(image_path).resize((200, 80))
    buttom_red = ImageTk.PhotoImage(buttom_red)

    root.withdraw()
    # num_questions = simpledialog.askinteger(
    #     "Game Setup",
    #     "How many questions do you want to answer?",
    #     initialvalue=2,
    #     minvalue=1,
    #     maxvalue=100
    # )
    num_questions = 10

    if num_questions is None:
        root.quit()
        root.destroy()
        sys.exit(0)

    root.deiconify()
    root.title("Gra - rozpoznawanie emocji")

    root.attributes("-fullscreen", True)
    game_state = GameState(root, num_questions, session_folder=session_folder)

    end_button = tkinter.Label(
        root,
        image=buttom_red,
        text="ZAKOŃCZ",
        font=("Monocraft", 24
              , "bold"),
        bg=bg_color,
        fg=text_color,
        compound="center"

    )
    end_button.bind("<Button-1>", lambda e: end_game())

    end_button.place(relx=1.0, x=-10, y=10, anchor="ne")

    # clear txt files
    log_files = ["feeling_answers.txt", "reason_answers.txt", "score.txt", "difficulty.txt",
                 "emotion_probabilities.txt"]
    for filename in log_files:
        full_path = os.path.join(session_folder, filename)
        with open(full_path, "w") as f:
            f.write("")

    game_state.max_rounds = num_questions


    def end_game():
        SummaryScreen(root, game_state).render()
        root.protocol("WM_DELETE_WINDOW", root.quit)


    game_state.end_callback = end_game
    StartTrail(root, game_state).render()

    try:
        root.mainloop()
    except:
        sys.exit(0)
