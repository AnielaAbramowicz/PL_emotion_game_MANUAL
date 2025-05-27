import tkinter as tk
from utils.image_loader import load_image
import time
import os
import sys

CORRECTNESS_RANGE = (0, 2)   
FEELING_RANGE = (-2, 2)  
TIME_RANGE = (-1, 1)      

frame_color = "#9090EE"     #purple
bg_color = "#D3EAA6"        # soft pastel green
text_color = "#0E314A"      # dark blue

def normalize(value, max, min):
    #maps [min,max] to [0,1]
    if max == min:
        return 0.5
    return (value-min)/(max-min)



class ReasonFeedbackScreen:
    def __init__(self, root, game_state):
        self.root = root
        self.gs = game_state
                
        self.label = tk.Label(root, text="Co sprawiło, że tak się poczułeś?", font=("Monocraft", 90), bg=bg_color, fg=text_color)
        self.frame = tk.Frame(root, bg=bg_color)
        self.time_beg = None

        base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))

        # Update these paths if you move images
        self.game_img_path = os.path.join(base_path, "visualization", "GAME.jpg")
        self.shared_image_path = self.gs.last_img_path 

    def render(self):
        self.clear()
        self.label.config(font=("Monocraft", 60))


        self.label.pack(pady=80)
        self.frame.pack(pady=0)

        self.time_beg = time.time()

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        img_width, img_height = int(screen_width*0.4), int(screen_height*0.3)
        game_img = load_image(self.game_img_path, size=(img_width,img_height))
        shared_image = load_image(self.shared_image_path, size=(img_width,img_height))

        self.note_label = tk.Label(self.root, text="Obraz / emocja", font=("Monocraft", 27, "bold"), bg=bg_color, fg=text_color)
        self.note_label.place(x=screen_width/2+310, y=screen_height/2 + 330)

        #Image 1 in frame
        frame1 = tk.Frame(self.frame, bd=10, relief=tk.RAISED, bg=frame_color)
        frame1.pack(pady=0)
        btn1 = tk.Button(frame1, image=game_img, command=lambda: self.log_and_continue(1), bg=bg_color, relief="flat")
        btn1.image = game_img
        btn1.pack()

        #Image 2 in frame
        frame2 = tk.Frame(self.frame, bd=10, relief=tk.RAISED, bg=frame_color)
        frame2.pack(pady=0)
        btn2 = tk.Button(frame2, image=shared_image, command=lambda: self.log_and_continue(2), bg=bg_color, relief="flat")
        btn2.image = shared_image
        btn2.pack()


        self.frame.tkraise()




    def next_image(self):
        from screens.emotion_question import EmotionQuestionScreen

        if self.gs.round >= self.gs.max_rounds:
            self.gs.end_callback()
            return

        # while self.gs.current_index < len(self.gs.df) and self.gs.df.iloc[self.gs.current_index]['shown']:
        #     self.gs.current_index += 1

        # if self.gs.current_index >= len(self.gs.df):
        #     self.root.destroy()
        #     return

        self.clear()
        EmotionQuestionScreen(self.root, self.gs).render()

    def clear(self):
        self.label.pack_forget()
        self.frame.pack_forget()
        for widget in self.frame.winfo_children():
            widget.destroy()
        if hasattr(self, "note_label"):
            self.note_label.destroy()


    def log_and_continue(self, answer_number):
        if len(self.gs.current_respond_time) >= 1:
            avg_time = sum(self.gs.current_respond_time)/ len(self.gs.current_respond_time)
        else:
            avg_time = 1.0

        #take into consideration last two times to deal with outliers more
        last_two_times = self.gs.current_respond_time[-2:]
        avg_last_two = sum(last_two_times) / len(last_two_times)


        if avg_last_two > avg_time*1.5:
            time_score = -1
        elif avg_last_two < avg_time*0.5:
            time_score = 1
        else:
            time_score = 0


        if answer_number == 1:
            text = "game"
        else:
            text = "question"

        total_time = time.time() - self.time_beg
        with open(os.path.join(self.gs.session_folder,"reason_answers.txt"), "a") as f:
            f.write(f"{total_time:.2f} seconds  - Answer: {text}\n")


        last_correctness = self.gs.currect_correctness[-1]
        last_feeling = self.gs.currect_feeliing[-1]

        #normalize it to [0;1]
        correctness_norm = normalize(last_correctness, *CORRECTNESS_RANGE)
        feeling_norm = normalize(last_feeling, *FEELING_RANGE)
        time_norm = normalize(time_score, *TIME_RANGE)
        #difficulty_norm = self.gs.difficulty
        difficulty_int = self.gs.df.loc[self.gs.current_index, "difficulty"]
        difficulty_norm = float(difficulty_int)


        # Progress scaling: later questions matter more
        question_progress = len(self.gs.currect_score)/ self.gs.num_questions 
        
        # Weighted score
        normalized_score = (
            0.4 * correctness_norm +
            0.2 * difficulty_int +
            0.1 * question_progress +
            0.2 * feeling_norm +
            0.1 * time_norm
        )

        self.gs.currect_score.append(normalized_score)

        with open(os.path.join(self.gs.session_folder, "score.txt"), "a") as f:
            f.write(f"Score: {normalized_score:.3f}, Difficulty: {difficulty_norm:.3f}, Correctness: {last_correctness}, Feeling: {last_feeling}, Time Score: {time_score}, Progress: {question_progress:.2f}\n")

        self.next_image()