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
        self.root.geometry("450x400")

        self.habits = []
        self.completed_today = set()
        self.load_data()

        self.notebook = ttk.Notebook(root)
        self.today_frame = ttk.Frame(self.notebook)
        self.history_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.today_frame, text="Сегодня")
        self.notebook.add(self.history_frame, text="Статистика")
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        control_frame = ttk.Frame(root)
        control_frame.pack(fill="x", padx=10)

        self.entry = ttk.Entry(control_frame, width=25)
        self.entry.grid(row=0, column=0, padx=(0, 5), pady=(0, 10))

        self.add_button = ttk.Button(control_frame, text="Add Habit", command=self.add_habit)
        self.add_button.grid(row=0, column=1, pady=(0, 10))

        self.vars = {}

        self.today_list_frame = ttk.Frame(self.today_frame)
        self.today_list_frame.pack(fill="both", expand=True, pady=(0, 10))

        self.history_list_frame = ttk.Frame(self.history_frame)
        self.history_list_frame.pack(fill="both", expand=True, pady=(0, 10))

        self.display_today_tab()
        self.display_history_tab()

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
            self.completed_today = set()
            self.save_data()
            return

        if isinstance(data, list):
            self.habits = data
            self.completed_today = set()
            self.save_data()
            return

        if isinstance(data, dict):
            self.habits = data.get("habits", [])
            ct = data.get("completed_today", [])
            self.completed_today = set(ct if isinstance(ct, list) else [])
        else:
            self.habits = []
            self.completed_today = set()
            self.save_data()

    def save_data(self):
        data = {
            "habits": self.habits,
            "completed_today": list(self.completed_today)
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
        self.entry.delete(0, tk.END)
        self.save_data()
        self.display_today_tab()
        self.display_history_tab()

    def remove_habit(self, name):
        confirm = messagebox.askyesno("Удалить", f"Удалить привычку «{name}»?")
        if not confirm:
            return
        if name in self.habits:
            self.habits.remove(name)
        if name in self.completed_today:
            self.completed_today.remove(name)
        self.save_data()
        self.display_today_tab()
        self.display_history_tab()

    def toggle_complete(self, name):
        if self.vars[name].get():
            self.completed_today.add(name)
        else:
            self.completed_today.discard(name)
        self.save_data()
        self.display_history_tab()

    def display_today_tab(self):
        for w in self.today_list_frame.winfo_children():
            w.destroy()
        self.vars.clear()

        if not self.habits:
            ttk.Label(self.today_list_frame, text="Нет привычек").pack(pady=10)
            return

        for idx, habit in enumerate(self.habits):
            row = ttk.Frame(self.today_list_frame)
            row.pack(fill="x", pady=2, padx=5)
            var = tk.BooleanVar(value=(habit in self.completed_today))
            self.vars[habit] = var

            cb = ttk.Checkbutton(
                row,
                text=habit,
                variable=var,
                command=lambda h=habit: self.toggle_complete(h)
            )
            cb.pack(side="left", anchor="w")

            btn = ttk.Button(
                row,
                text="Delete",
                width=6,
                command=lambda h=habit: self.remove_habit(h)
            )
            btn.pack(side="right")

    def display_history_tab(self):
        for w in self.history_list_frame.winfo_children():
            w.destroy()

        if not self.habits:
            ttk.Label(self.history_list_frame, text="Нет привычек").pack(pady=10)
            return

        completed = [h for h in self.habits if h in self.completed_today]
        not_completed = [h for h in self.habits if h not in self.completed_today]

        ttk.Label(
            self.history_list_frame,
            text=f"Выполненных сегодня: {len(completed)} из {len(self.habits)}"
        ).pack(pady=(5, 10))

        ttk.Label(self.history_list_frame, text="✅ Выполнено:").pack(anchor="w", padx=5)
        for h in completed:
            ttk.Label(self.history_list_frame, text=f"  - {h}").pack(anchor="w", padx=15)

        ttk.Label(self.history_list_frame, text="❌ Не выполнено:").pack(anchor="w", pady=(10, 0), padx=5)
        for h in not_completed:
            ttk.Label(self.history_list_frame, text=f"  - {h}").pack(anchor="w", padx=15)

def main():
    root = tk.Tk()
    app = HabitTracker(root)
    root.mainloop()

if __name__ == "__main__":
    main()
