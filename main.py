import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import datetime

DATA_PATH = "habits.json"

class HabitTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Habit Tracker")
        self.root.geometry("550x500")
        self.habits = []
        self.history = {}
        self.completed_today = set()
        self.completed_habits = []
        self.load_data()

        self.top_frame = ttk.Frame(root)
        self.top_frame.pack(fill="x", pady=(10, 0))
        self.display_top_habits()

        control_frame = ttk.Frame(root)
        control_frame.pack(fill="x", padx=10, pady=(5, 10))
        self.entry = ttk.Entry(control_frame, width=30)
        self.entry.grid(row=0, column=0, padx=(0, 5))
        self.entry.bind("<Return>", lambda e: self.add_habit())
        self.add_button = ttk.Button(control_frame, text="Add Habit", command=self.add_habit)
        self.add_button.grid(row=0, column=1)

        self.notebook = ttk.Notebook(root)
        self.today_frame = ttk.Frame(self.notebook)
        self.stats_frame = ttk.Frame(self.notebook)
        self.completed_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.today_frame, text="Сегодня")
        self.notebook.add(self.stats_frame, text="Статистика")
        self.notebook.add(self.completed_frame, text="Завершено")
        self.notebook.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self.vars = {}
        self.today_list_frame = ttk.Frame(self.today_frame)
        self.today_list_frame.pack(fill="both", expand=True, pady=(0, 10))
        self.stats_list_frame = ttk.Frame(self.stats_frame)
        self.stats_list_frame.pack(fill="both", expand=True, pady=(0, 10))
        self.completed_list_frame = ttk.Frame(self.completed_frame)
        self.completed_list_frame.pack(fill="both", expand=True, pady=(0, 10))

        self.display_today_tab()
        self.display_stats_tab()
        self.display_completed_tab()

    def load_data(self):
        if os.path.exists(DATA_PATH):
            try:
                with open(DATA_PATH, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except (json.JSONDecodeError, ValueError):
                data = None
        else:
            data = None
        if data is None:
            self.habits = []
            self.history = {}
            self.completed_today = set()
            self.completed_habits = []
            self.save_data()
            return
        if isinstance(data, dict):
            self.habits = data.get("habits", [])
            self.history = data.get("history", {})
            ct = data.get("completed_today", [])
            self.completed_today = set(ct if isinstance(ct, list) else [])
            self.completed_habits = data.get("completed_habits", [])
        else:
            self.habits = data if isinstance(data, list) else []
            self.history = {}
            self.completed_today = set()
            self.completed_habits = []
            self.save_data()

    def save_data(self):
        data = {
            "habits": self.habits,
            "history": self.history,
            "completed_today": list(self.completed_today),
            "completed_habits": self.completed_habits
        }
        with open(DATA_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def add_habit(self):
        name = self.entry.get().strip()
        if not name:
            return
        if name in self.habits:
            messagebox.showinfo("Info", f"Привычка «{name}» уже есть.")
            return
        self.habits.append(name)
        self.history[name] = []
        self.entry.delete(0, tk.END)
        self.save_data()
        self.display_top_habits()
        self.display_today_tab()
        self.display_stats_tab()

    def remove_habit(self, name):
        confirm = messagebox.askyesno("Удалить", f"Удалить привычку «{name}»?")
        if not confirm:
            return
        if name in self.habits:
            self.habits.remove(name)
        self.history.pop(name, None)
        self.completed_today.discard(name)
        self.save_data()
        self.display_top_habits()
        self.display_today_tab()
        self.display_stats_tab()

    def toggle_complete(self, name):
        today = datetime.date.today().isoformat()
        if self.vars[name].get():
            if name not in self.completed_today:
                self.completed_today.add(name)
                if today not in self.history.get(name, []):
                    self.history.setdefault(name, []).append(today)
        else:
            self.completed_today.discard(name)
            if today in self.history.get(name, []):
                self.history[name].remove(today)
        self.save_data()
        if len(self.history.get(name, [])) >= 7:
            self.complete_habit(name)
        self.display_stats_tab()

    def complete_habit(self, name):
        today = datetime.date.today().isoformat()
        entry = {"name": name, "completed_date": today, "history": self.history.get(name, [])}
        self.completed_habits.append(entry)
        if name in self.habits:
            self.habits.remove(name)
        self.history.pop(name, None)
        self.completed_today.discard(name)
        self.save_data()
        self.display_top_habits()
        self.display_today_tab()
        self.display_completed_tab()

    def display_top_habits(self):
        for w in self.top_frame.winfo_children():
            w.destroy()
        if not self.habits:
            return
        for habit in self.habits:
            lbl = ttk.Label(self.top_frame, text=habit, padding=(5, 2))
            lbl.pack(side="left", padx=2)

    def display_today_tab(self):
        for w in self.today_list_frame.winfo_children():
            w.destroy()
        self.vars.clear()
        if not self.habits:
            ttk.Label(self.today_list_frame, text="Нет привычек").pack(pady=10)
            return
        for habit in self.habits:
            row = ttk.Frame(self.today_list_frame)
            row.pack(fill="x", pady=2, padx=5)
            var = tk.BooleanVar(value=(habit in self.completed_today))
            self.vars[habit] = var
            cb = ttk.Checkbutton(row, text=habit, variable=var, command=lambda h=habit: self.toggle_complete(h))
            cb.pack(side="left", anchor="w")
            btn = ttk.Button(row, text="Delete", width=6, command=lambda h=habit: self.remove_habit(h))
            btn.pack(side="right")

    def display_stats_tab(self):
        for w in self.stats_list_frame.winfo_children():
            w.destroy()
        if not self.habits:
            ttk.Label(self.stats_list_frame, text="Нет привычек").pack(pady=10)
            return
        for habit in self.habits:
            frame = ttk.Frame(self.stats_list_frame)
            frame.pack(fill="x", pady=5, padx=5)
            ttk.Label(frame, text=f"{habit}").pack(anchor="w")
            today = datetime.date.today()
            circles = ""
            for i in range(6, -1, -1):
                day = (today - datetime.timedelta(days=i)).isoformat()
                if day in self.history.get(habit, []):
                    circles += "● "
                else:
                    circles += "○ "
            ttk.Label(frame, text=circles.strip()).pack(anchor="w", pady=(2, 0))

    def display_completed_tab(self):
        for w in self.completed_list_frame.winfo_children():
            w.destroy()
        if not self.completed_habits:
            ttk.Label(self.completed_list_frame, text="Нет завершённых привычек").pack(pady=10)
            return
        for entry in self.completed_habits:
            frame = ttk.Frame(self.completed_list_frame)
            frame.pack(fill="x", pady=5, padx=5)
            name = entry.get("name", "")
            date = entry.get("completed_date", "")
            ttk.Label(frame, text=f"{name} (завершено: {date})").pack(anchor="w")

def main():
    root = tk.Tk()
    app = HabitTracker(root)
    root.mainloop()

if __name__ == "__main__":
    main()
