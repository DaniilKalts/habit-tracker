import tkinter as tk

class HabitTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Habit Tracker")
        self.root.geometry("400x300")

        self.entry = tk.Entry(root, width=30)
        self.entry.pack(pady=10)

        self.add_button = tk.Button(root, text="Add Habit", command=self.add_habit)
        self.add_button.pack(pady=5)

    def add_habit(self):
        habit_name = self.entry.get()
        if habit_name:
            print(f"Adding: {habit_name}")
            self.entry.delete(0, tk.END)

def main():
    root = tk.Tk()
    app = HabitTracker(root)
    root.mainloop()

if __name__ == "__main__":
    main()
