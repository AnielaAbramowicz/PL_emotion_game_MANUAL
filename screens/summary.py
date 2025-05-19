import tkinter as tk
import sys
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
import pandas as pd
import os


frame_color = "#9090EE"     #purple
bg_color = "#D3EAA6"        # soft pastel green
text_color = "#0E314A"      # dark blue

class SummaryScreen:
    def __init__(self, root, game_state):
        self.root = root
        self.gs = game_state
        self.root.configure(bg=bg_color)

        self.main_frame = tk.Frame(root, bg=bg_color)

        flower_left_raw = Image.open("/Users/anielamac/Desktop/thesis/visualization/flower_left.png").resize((200,370))
        self.flower_left = ImageTk.PhotoImage(flower_left_raw)

        flower_right_raw = Image.open("/Users/anielamac/Desktop/thesis/visualization/flower_right.png").resize((200,370))
        self.flower_right = ImageTk.PhotoImage(flower_right_raw)

        button_red_raw = Image.open("/Users/anielamac/Desktop/thesis/visualization/buttom_red.png").resize((400,160))
        self.button_red = ImageTk.PhotoImage(button_red_raw)

        self.label = tk.Label(self.main_frame, font=("Monocraft", 16), fg=text_color, bg=bg_color)
        self.label2 = tk.Label(self.main_frame, font=("Monocraft", 16), fg=text_color, bg=bg_color)


    def render(self):
        self.clear()
        screen_height = self.root.winfo_screenheight()

        correct = self.gs.score
        total = self.gs.round


        used_rows = self.gs.full_df[self.gs.full_df["filename"].isin(self.gs.shown_filenames)]
        if not used_rows.empty:
            avg_diff = used_rows["difficulty"].mean()
        else:
            avg_diff = 0

        self.label2.config(
            text=f"KONIEC GRY!", font=("Monocraft", 130), justify="center", fg=text_color, bg=bg_color
        )
        self.label2.pack(pady=((screen_height/8),10))

        self.label.config(
            text=f"\nPoprawne odpowiedzi: {correct}/{total}\n\nŚredni poziom trudności: {avg_diff:.2f}", font=("Monocraft", 45), justify="center", fg=text_color, bg=bg_color
        )
        self.label.pack(pady=((50,10)))
        #self.exit_button = tk.Label(self.main_frame, image=self.buttom_red, text="Exit", compound="center")

        exit_button = tk.Label(self.main_frame,image=self.button_red, text="Zakończ", compound="center", bg=bg_color, fg=text_color, font=("Monocraft", 50), padx=0,pady=-80 )
        exit_button.image = self.button_red
        exit_button.bind("<Button-1>", lambda e: sys.exit())
        exit_button.pack(pady=(100,10))

        screen_width = self.root.winfo_screenwidth()

        flower_label = tk.Label(self.root, image=self.flower_left, bg=bg_color)
        flower_label.image = self.flower_left
        flower_label.place(x=30, rely=0.5, anchor="w")  

        flower_label2 = tk.Label(self.root, image=self.flower_right, bg=bg_color)
        flower_label2.image = self.flower_right
        flower_label2.place(x=screen_width-30-200, rely=0.5, anchor="w") 

        self.main_frame.pack(fill="both", expand=True)

    

        try:
            with open(os.path.join(self.gs.session_folder, "difficulty.txt"), "r") as f:
                lines = f.readlines()

            data = []
            for line in lines:
                if "Round" in line:
                    parts = line.strip().split(", ")
                    round_num = int(parts[0].split()[1])
                    perf = float(parts[1].split(": ")[1])
                    diff = float(parts[-1].split(": ")[1])
                    data.append((round_num, perf, diff))

            df = pd.DataFrame(data, columns=["Round", "Performance", "Difficulty"])
            plt.figure(figsize=(10, 5))
            plt.plot(df["Round"], df["Difficulty"], label="Selected Difficulty", marker="o")
            plt.plot(df["Round"], df["Performance"], label="Performance", marker="x")
            plt.xticks(df["Round"])

            plt.legend()
            plt.grid(True)
            plt.title("Performance vs. Difficulty")
            plt.savefig(os.path.join(self.gs.session_folder, "difficulty_plot.png"))
            plt.close() 


        except Exception as e:
            print("Could not plot difficulty graph:", e)






    def clear(self):
        self.main_frame.pack_forget()
        for widget in self.root.winfo_children():
            widget.pack_forget()
