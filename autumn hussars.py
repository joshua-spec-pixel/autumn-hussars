import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import time
import threading
import os

# --- Vibes and Chess Graphics ---
BISHOP = "\u265D"  # Black Bishop
KNIGHT = "\u265E"  # Black Knight
KING = "\u265A"    # Black King
QUEEN = "\u265B"   # Black Queen

# --- Note Window ---
class NoteWindow(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Autumn Journal - Notes")
        self.configure(bg="#f7f6ed")
        self.geometry("600x600")
        self.resizable(False, False)

        # Main horizontal frame
        main_frame = tk.Frame(self, bg="#f7f6ed")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Left frame (notes, 75%)
        left_frame = tk.Frame(main_frame, bg="#f7f6ed")
        left_frame.place(relx=0, rely=0, relwidth=0.75, relheight=1)

        tk.Label(left_frame, text="The Winged Hussar Hall of Fame\nand Campaign Journal",
                 font=("Times New Roman", 16, "bold"), fg="#1c2d3a", bg="#f7f6ed").pack(pady=(10,2))
        tk.Label(left_frame, text="We remember in September\nThat's the night Vienna was freed", font=("Times New Roman", 12), fg="#735f35", bg="#f7f6ed").pack()

        self.textbox = scrolledtext.ScrolledText(left_frame, wrap=tk.WORD, font=("Georgia", 12), bg="#fff8e1")
        self.textbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=20)

        btn_frame = tk.Frame(left_frame, bg="#f7f6ed")
        btn_frame.pack(pady=5)
        tk.Button(btn_frame, text="Save Note", command=self.save_note, bg="#b4a078").pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Load Note", command=self.load_note, bg="#b4a078").pack(side=tk.LEFT, padx=5)

        # Right frame (bishop icon, 25%)
        right_frame = tk.Frame(main_frame, bg="#f7f6ed")
        right_frame.place(relx=0.75, rely=0, relwidth=0.25, relheight=1)

        # Center knight vertically, and half the height of notes box
        icon_container = tk.Frame(right_frame, bg="#f7f6ed")
        icon_container.place(relx=0, rely=0.25, relwidth=1, relheight=0.5)  # vertically centered, half height

        bishop_label = tk.Label(icon_container, text=BISHOP, font=("Segoe UI Symbol", 110), fg="#2b2b2b", bg="#f7f6ed")
        bishop_label.pack(expand=True)

        quote_label = tk.Label(icon_container, text="Guard your heart\n above all else,\nfor it is\nthe source of life.",
                               font=("Monotype Corsiva", 14, "italic"), fg="#6d4c31", bg="#f7f6ed", justify="center")
        quote_label.pack(pady=(10, 0))
        
        btn_frame = tk.Frame(right_frame, bg="#f7f6ed")
        btn_frame.place(relx=0, rely=0.8, relwidth=1, relheight=0.12) # 12% height, below the quote
        tk.Button(btn_frame, text="Save Note", command=self.save_note, bg="#b4a078", font=("Georgia", 10)).pack(fill=tk.X, padx=8, pady=(0,4))
        tk.Button(btn_frame, text="Load Note", command=self.load_note, bg="#b4a078", font=("Georgia", 10)).pack(fill=tk.X, padx=8)

    def save_note(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Documents", "*.txt")])
        if file_path:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(self.textbox.get(1.0, tk.END))
            messagebox.showinfo("Saved!", f"Note saved to {os.path.basename(file_path)}.")

    def load_note(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Documents", "*.txt")])
        if file_path:
            with open(file_path, "r", encoding="utf-8") as f:
                self.textbox.delete(1.0, tk.END)
                self.textbox.insert(tk.END, f.read())
            messagebox.showinfo("Loaded!", f"Note loaded from {os.path.basename(file_path)}.")

# --- Pomodoro Window ---
class PomodoroWindow(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("The Hussar-Chess Timer")
        self.configure(bg="#f7f6ed")
        self.geometry("500x420")
        self.resizable(False, False)

        # Main horizontal frame
        main_frame = tk.Frame(self, bg="#f7f6ed")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Knight icon frame (35%)
        icon_frame = tk.Frame(main_frame, bg="#f7f6ed")
        icon_frame.place(relx=0, rely=0, relwidth=0.35, relheight=1)

        knight_label = tk.Label(icon_frame, text=KNIGHT, font=("Segoe UI Symbol", 140), fg="#393939", bg="#f7f6ed")
        knight_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Timer/configs frame (65%)
        timer_frame = tk.Frame(main_frame, bg="#f7f6ed")
        timer_frame.place(relx=0.35, rely=0, relwidth=0.65, relheight=0.8)

        tk.Label(timer_frame, text="Autumn Grind Timer", font=("Times New Roman", 20, "bold"), fg="#1c2d3a", bg="#f7f6ed").pack(pady=(12,2))
        tk.Label(timer_frame, text="The chivalric wings of a hussar\nbring the tranquility of autumn.", font=("Times New Roman", 14), fg="#735f35", bg="#f7f6ed").pack()

        self.time_var = tk.StringVar(value="25:00")
        tk.Label(timer_frame, textvariable=self.time_var, font=("Consolas", 36, "bold"), bg="#f7f6ed").pack(pady=14)

        self.running = False
        self.pomodoro_minutes = tk.IntVar(value=25)
        self.break_minutes = tk.IntVar(value=5)

        frame = tk.Frame(timer_frame, bg="#f7f6ed")
        frame.pack(pady=5)
        tk.Label(frame, text="Pomodoro (min):", bg="#f7f6ed").pack(side=tk.LEFT)
        tk.Entry(frame, textvariable=self.pomodoro_minutes, width=3).pack(side=tk.LEFT, padx=3)
        tk.Label(frame, text="Break (min):", bg="#f7f6ed").pack(side=tk.LEFT)
        tk.Entry(frame, textvariable=self.break_minutes, width=3).pack(side=tk.LEFT, padx=3)

        btn_frame = tk.Frame(timer_frame, bg="#f7f6ed")
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Start", command=self.start_timer, bg="#b4a078").pack(side=tk.LEFT, padx=4)
        tk.Button(btn_frame, text="Pause", command=self.pause_timer, bg="#b4a078").pack(side=tk.LEFT, padx=4)
        tk.Button(btn_frame, text="Reset", command=self.reset_timer, bg="#b4a078").pack(side=tk.LEFT, padx=4)

        # Bottom quote in Monotype Corsiva
        quote_frame = tk.Frame(main_frame, bg="#f7f6ed")
        quote_frame.place(relx=0, rely=0.8, relwidth=1, relheight=0.2)
        quote_label = tk.Label(quote_frame, text="The brave are those who act, not merely those who dream.",
                               font=("Monotype Corsiva", 20, "italic"), fg="#6d4c31", bg="#f7f6ed", wraplength=480, justify="center")
        quote_label.pack(expand=True, pady=(5, 0))

    def start_timer(self):
        if not self.running:
            self.running = True
            threading.Thread(target=self.run_timer, daemon=True).start()

    def run_timer(self):
        total_seconds = self.pomodoro_minutes.get() * 60
        while total_seconds > 0 and self.running:
            mins, secs = divmod(total_seconds, 60)
            self.time_var.set(f"{mins:02d}:{secs:02d}")
            time.sleep(1)
            total_seconds -= 1
        if total_seconds == 0 and self.running:
            self.time_var.set("Break!")
            self.running = False
            self.after(1000, self.start_break)

    def start_break(self):
        self.running = True
        total_seconds = self.break_minutes.get() * 60
        while total_seconds > 0 and self.running:
            mins, secs = divmod(total_seconds, 60)
            self.time_var.set(f"Break: {mins:02d}:{secs:02d}")
            time.sleep(1)
            total_seconds -= 1
        self.time_var.set("Session done!")
        self.running = False

    def pause_timer(self):
        self.running = False

    def reset_timer(self):
        self.running = False
        self.time_var.set(f"{self.pomodoro_minutes.get():02d}:00")

# --- Main Window ---
class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Hall Of Hussars - Autumn Chess")
        self.geometry("500x280")
        self.configure(bg="#d5cfc5")
        self.resizable(False, False)

        main_frame = tk.Frame(self, bg="#d5cfc5")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # King piece on left, leaf icon on right
        top_frame = tk.Frame(main_frame, bg="#d5cfc5")
        top_frame.pack(fill=tk.X, padx=10, pady=(10, 0))

        left_icon = tk.Label(top_frame, text=KING, font=("Segoe UI Symbol", 40), fg="#2d1c0a", bg="#d5cfc5")
        left_icon.pack(side=tk.LEFT, padx=(5, 0))

        tk.Label(top_frame, text="Autumn Hussars", font=("Bookman Old Style", 22, "bold"), fg="#2d1c0a", bg="#d5cfc5").pack(side=tk.LEFT, expand=True, padx=15)
        right_icon = tk.Label(top_frame, text=QUEEN, font=("Segoe UI Symbol", 35), fg="#735f35", bg="#d5cfc5")
        right_icon.pack(side=tk.RIGHT, padx=(0, 7))

        tk.Label(main_frame, text="September for Polish Hussars", font=("Courier New", 18), fg="#735f35", bg="#d5cfc5").pack(pady=(0, 8))

        btn_frame = tk.Frame(main_frame, bg="#d5cfc5")
        btn_frame.pack(pady=25)
        tk.Button(btn_frame, text="Campaign Journal", command=self.open_notes, font=("Georgia", 12), bg="#b4a078").pack(pady=10, fill=tk.X)
        tk.Button(btn_frame, text="Sieze The Day", command=self.open_pomodoro, font=("Georgia", 12), bg="#b4a078").pack(pady=10, fill=tk.X)


        # After you set up your main window (for example, in MainApp.__init__):
        
        footer_label = tk.Label(self, text="A Tribute to:\nCharlie Kirk\nand the victims\nof hate", font=("Lucida Handwriting", 9), fg="#735f35", bg="#d5cfc5")
        footer_label.place(relx=1.0, rely=1.0, anchor='se', x=-10, y=-10)  # 10px margin from bottom/right

    def open_notes(self):
        NoteWindow(self)

    def open_pomodoro(self):
        PomodoroWindow(self)

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()



