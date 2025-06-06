import tkinter as tk
import json
import os
from tkinter import messagebox

class HabitTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Habit Tracker")
        self.root.geometry("400x300")

        self.habits = []
        self.load_data()

        self.entry = tk.Entry(root, width=30)
        self.entry.pack(pady=10)

        self.add_button = tk.Button(root, text="Add Habit", command=self.add_habit)
        self.add_button.pack(pady=5)

        self.habits_frame = tk.Frame(root)
        self.habits_frame.pack(pady=10, fill="both", expand=True)

        self.display_habits()

    def load_data(self):
        if os.path.exists("habits.json"):
            try:
                with open("habits.json", "r") as f:
                    self.habits = json.load(f)
            except (json.JSONDecodeError, ValueError):
                self.habits = []
        else:
            with open("habits.json", "w") as f:
                json.dump(self.habits, f)

    def save_data(self):
        with open("habits.json", "w") as f:
            json.dump(self.habits, f)

    def add_habit(self):
        habit_name = self.entry.get().strip()
        if habit_name and habit_name not in self.habits:
            self.habits.append(habit_name)
            self.entry.delete(0, tk.END)
            self.save_data()
            self.display_habits()

    def remove_habit(self, habit_name):
        confirm = messagebox.askyesno(
            "Удалить привычку",
            f"Вы уверены, что хотите удалить «{habit_name}»?"
        )
        if confirm and habit_name in self.habits:
            self.habits.remove(habit_name)
            self.save_data()
            self.display_habits()

    def display_habits(self):
        for widget in self.habits_frame.winfo_children():
            widget.destroy()

        if not self.habits:
            tk.Label(self.habits_frame, text="Нет привычек", fg="gray").pack()
            return

        for habit in self.habits:
            row = tk.Frame(self.habits_frame)
            row.pack(fill="x", pady=2)

            lbl = tk.Label(row, text=habit, anchor="w")
            lbl.pack(side="left", fill="x", expand=True)

            btn = tk.Button(
                row,
                text="Delete",
                command=lambda h=habit: self.remove_habit(h),
                width=6
            )
            btn.pack(side="right")

def main():
    root = tk.Tk()
    app = HabitTracker(root)
    root.mainloop()

if __name__ == "__main__":
    main()
