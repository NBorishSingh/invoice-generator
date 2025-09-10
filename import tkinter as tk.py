import tkinter as tk
from tkinter import messagebox
import threading
import time

questions = [
    {"question": "What is the capital of France?", "options": ["Paris", "Rome", "Berlin", "London"], "answer": "Paris"},
    {"question": "What is 2 + 2?", "options": ["3", "4", "5", "6"], "answer": "4"},
    {"question": "Which planet is known as the Red Planet?", "options": ["Earth", "Mars", "Jupiter", "Venus"], "answer": "Mars"},
    {"question": "What color is the sky on a clear day?", "options": ["Blue", "Green", "Red", "Yellow"], "answer": "Blue"},
    {"question": "How many legs does a spider have?", "options": ["6", "8", "4", "2"], "answer": "8"},
    {"question": "Which fruit is yellow and long?", "options": ["Apple", "Banana", "Grapes", "Orange"], "answer": "Banana"},
    {"question": "What do we drink that comes from cows?", "options": ["Juice", "Milk", "Water", "Tea"], "answer": "Milk"},
    {"question": "What sound does a dog make?", "options": ["Meow", "Moo", "Bark", "Roar"], "answer": "Bark"},
    {"question": "What shape has three sides?", "options": ["Square", "Triangle", "Circle", "Rectangle"], "answer": "Triangle"},
    {"question": "What do you use to write on a blackboard?", "options": ["Pen", "Pencil", "Chalk", "Marker"], "answer": "Chalk"}
]

class QuizApp:
    def _init_(self, root):
        self.root = root
        self.root.title("Quiz App with Timer")
        self.root.geometry("400x350")
        self.score = 0
        self.qn_index = 0
        self.timer_seconds = 10
        self.timer_thread = None
        self.timer_running = False
        self.create_start_screen()

    def create_start_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Welcome to Quiz App", font=('Arial', 16)).pack(pady=30)
        tk.Button(self.root, text="Start Quiz", command=self.start_quiz, font=('Arial', 12)).pack(pady=10)

    def start_quiz(self):
        self.score = 0
        self.qn_index = 0
        self.show_question()

    def show_question(self):
        self.clear_screen()
        self.timer_running = True

        self.question_label = tk.Label(self.root, text="", font=('Arial', 14), wraplength=350)
        self.question_label.pack(pady=20)

        self.option_buttons = []
        for i in range(4):
            btn = tk.Button(self.root, text="", font=('Arial', 12), command=lambda i=i: self.check_answer(i))
            btn.pack(fill="x", padx=50, pady=2)
            self.option_buttons.append(btn)

        self.timer_label = tk.Label(self.root, text="", font=('Arial', 12), fg="red")
        self.timer_label.pack(pady=10)

        self.load_question()
        self.start_timer()

    def load_question(self):
        question_data = questions[self.qn_index]
        self.question_label.config(text=f"Q{self.qn_index + 1}: {question_data['question']}")
        for i, option in enumerate(question_data["options"]):
            self.option_buttons[i].config(text=option, state="normal")

    def check_answer(self, selected_index):
        if not self.timer_running:
            return
        self.timer_running = False

        for btn in self.option_buttons:
            btn.config(state="disabled")

        correct_answer = questions[self.qn_index]["answer"]
        if questions[self.qn_index]["options"][selected_index] == correct_answer:
            self.score += 1

        self.root.after(500, self.next_question)

    def start_timer(self):
        def countdown():
            remaining = self.timer_seconds
            while remaining > 0 and self.timer_running:
                self.timer_label.config(text=f"Time left: {remaining} sec")
                time.sleep(1)
                remaining -= 1
            if remaining == 0 and self.timer_running:
                self.timer_running = False
                self.timer_label.config(text="Time's up!")
                for btn in self.option_buttons:
                    btn.config(state="disabled")
                self.root.after(1000, self.next_question)

        self.timer_thread = threading.Thread(target=countdown)
        self.timer_thread.start()

    def next_question(self):
        self.qn_index += 1
        if self.qn_index < len(questions):
            self.show_question()
        else:
            self.show_result()

    def show_result(self):
        self.clear_screen()
        messagebox.showinfo("Quiz Completed", f"You scored {self.score} out of {len(questions)}!")
        tk.Label(self.root, text=f"Your Score: {self.score}/{len(questions)}", font=('Arial', 16)).pack(pady=30)
        tk.Button(self.root, text="Restart", command=self.create_start_screen, font=('Arial', 12)).pack(pady=5)
        tk.Button(self.root, text="Exit", command=self.root.quit, font=('Arial', 12)).pack(pady=5)

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()


root = tk.Tk()
app = QuizApp(root)
root.mainloop()