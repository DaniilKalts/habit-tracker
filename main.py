import tkinter as tk

class HabitTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Habit Tracker")
        self.root.geometry("400x300")

def main():
    root = tk.Tk()
    app = HabitTracker(root)
    root.mainloop()

if __name__ == "__main__":
    main()
