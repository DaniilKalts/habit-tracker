import tkinter as tk

class HabitTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Habit Tracker")
        self.root.geometry("400x300")

        self.habits = []

        self.entry = tk.Entry(root, width=30)
        self.entry.pack(pady=10)

        self.add_button = tk.Button(root, text="Add Habit", command=self.add_habit)
        self.add_button.pack(pady=5)

        self.habits_frame = tk.Frame(root)
        self.habits_frame.pack(pady=10)

    def add_habit(self):
        habit_name = self.entry.get()
        if habit_name and habit_name not in self.habits:
            self.habits.append(habit_name)
            self.entry.delete(0, tk.END)
            self.display_habits()

    def display_habits(self):
        for widget in self.habits_frame.winfo_children():
            widget.destroy()

        for habit in self.habits:
            tk.Label(self.habits_frame, text=habit).pack()

def main():
    root = tk.Tk()
    app = HabitTracker(root)
    root.mainloop()

if __name__ == "__main__":
    main()
