import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3


def add_task():
    task = task_entry.get()
    priority = priority_entry.get()

    if task.strip() == "":
        messagebox.showwarning("Warning", "Please enter a task")
        return

    conn = sqlite3.connect("todo.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO tasks(task_name, priority, status) VALUES(?,?,?)",
        (task, priority, "Pending")
    )

    conn.commit()
    conn.close()

    task_entry.delete(0, tk.END)
    load_tasks()

    messagebox.showinfo("Success", "Task added successfully!")


def load_tasks():
    listbox.delete(0, tk.END)

    conn = sqlite3.connect("todo.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tasks")
    rows = cursor.fetchall()

    for row in rows:
        listbox.insert(
            tk.END,
            f"{row[0]} | {row[1]} | {row[2]} | {row[3]}"
        )

    conn.close()
    update_dashboard()


def update_dashboard():
    conn = sqlite3.connect("todo.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM tasks")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM tasks WHERE status='Completed'")
    completed = cursor.fetchone()[0]

    pending = total - completed

    total_label.config(text=f"📋 Total Tasks: {total}")
    completed_label.config(text=f"✅ Completed: {completed}")
    pending_label.config(text=f"⏳ Pending: {pending}")

    conn.close()


def delete_task():
    selected = listbox.curselection()

    if not selected:
        messagebox.showwarning("Warning", "Please select a task to delete")
        return

    item = listbox.get(selected)
    task_id = item.split("|")[0].strip()

    conn = sqlite3.connect("todo.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM tasks WHERE id=?",
        (task_id,)
    )

    conn.commit()
    conn.close()

    load_tasks()
    messagebox.showinfo("Deleted", "Task deleted successfully!")


def complete_task():
    selected = listbox.curselection()

    if not selected:
        messagebox.showwarning("Warning", "Please select a task to complete")
        return

    item = listbox.get(selected)
    task_id = item.split("|")[0].strip()

    conn = sqlite3.connect("todo.db")
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE tasks SET status=? WHERE id=?",
        ("Completed", task_id)
    )

    conn.commit()
    conn.close()

    load_tasks()
    messagebox.showinfo("Completed", "Task marked as completed!")


def search_task():
    keyword = search_entry.get()

    listbox.delete(0, tk.END)

    conn = sqlite3.connect("todo.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM tasks WHERE task_name LIKE ?",
        ("%" + keyword + "%",)
    )

    rows = cursor.fetchall()

    for row in rows:
        listbox.insert(
            tk.END,
            f"{row[0]} | {row[1]} | {row[2]} | {row[3]}"
        )

    conn.close()


def update_task():
    selected = listbox.curselection()

    if not selected:
        messagebox.showwarning("Warning", "Please select a task to update")
        return

    task = task_entry.get()
    priority = priority_entry.get()

    if task.strip() == "":
        messagebox.showwarning("Warning", "Please enter updated task name")
        return

    item = listbox.get(selected)
    task_id = item.split("|")[0].strip()

    conn = sqlite3.connect("todo.db")
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE tasks SET task_name=?, priority=? WHERE id=?",
        (task, priority, task_id)
    )

    conn.commit()
    conn.close()

    task_entry.delete(0, tk.END)
    load_tasks()

    messagebox.showinfo("Updated", "Task updated successfully!")


root = tk.Tk()

root.title("🌸 Smart To-Do List Pro")
root.geometry("700x780")
root.configure(bg="#F6EAF8")

tk.Label(
    root,
    text="🌸 Smart To-Do List Pro 🌸",
    font=("Arial", 22, "bold"),
    bg="#F6EAF8",
    fg="#B5236E"
).pack(pady=15)

tk.Label(
    root,
    text="Organize your day beautifully ✨",
    font=("Arial", 10, "italic"),
    bg="#F6EAF8",
    fg="#866D9C"
).pack()

dashboard_frame = tk.Frame(
    root,
    bg="#EEDBF5",
    bd=2,
    relief="ridge"
)

dashboard_frame.pack(pady=10, padx=20)

total_label = tk.Label(
    dashboard_frame,
    text="📋 Total Tasks: 0",
    font=("Arial", 11, "bold"),
    bg="#EEDBF5"
)
total_label.pack()

completed_label = tk.Label(
    dashboard_frame,
    text="✅ Completed: 0",
    font=("Arial", 11, "bold"),
    bg="#EEDBF5"
)
completed_label.pack()

pending_label = tk.Label(
    dashboard_frame,
    text="⏳ Pending: 0",
    font=("Arial", 11, "bold"),
    bg="#EEDBF5"
)
pending_label.pack()

tk.Label(
    root,
    text="Task",
    bg="#F6EAF8",
    fg="#866D9C",
    font=("Arial", 13, "bold")
).pack(pady=5)

task_entry = tk.Entry(
    root,
    width=45,
    font=("Arial", 12)
)
task_entry.pack(pady=5)

tk.Label(
    root,
    text="Priority",
    bg="#F6EAF8",
    fg="#866D9C",
    font=("Arial", 13, "bold")
).pack(pady=5)

priority_entry = ttk.Combobox(
    root,
    width=42,
    state="readonly"
)

priority_entry["values"] = (
    "High",
    "Medium",
    "Low"
)

priority_entry.current(0)
priority_entry.pack(pady=5)

tk.Label(
    root,
    text="Search",
    bg="#F6EAF8",
    fg="#866D9C",
    font=("Arial", 13, "bold")
).pack(pady=5)

search_entry = tk.Entry(
    root,
    width=45,
    font=("Arial", 12)
)
search_entry.pack(pady=5)

button_frame = tk.Frame(
    root,
    bg="#F6EAF8"
)
button_frame.pack(pady=10)

tk.Button(
    button_frame,
    text="➕ Add Task",
    width=18,
    font=("Arial", 11, "bold"),
    bg="#E8CFF0",
    fg="#5A3D6B",
    command=add_task
).grid(row=0, column=0, padx=5, pady=5)

tk.Button(
    button_frame,
    text="✏️ Update Task",
    width=18,
    font=("Arial", 11, "bold"),
    bg="#E8CFF0",
    fg="#5A3D6B",
    command=update_task
).grid(row=0, column=1, padx=5, pady=5)

tk.Button(
    button_frame,
    text="🗑️ Delete Task",
    width=18,
    font=("Arial", 11, "bold"),
    bg="#E8CFF0",
    fg="#5A3D6B",
    command=delete_task
).grid(row=1, column=0, padx=5, pady=5)

tk.Button(
    button_frame,
    text="✅ Complete Task",
    width=18,
    font=("Arial", 11, "bold"),
    bg="#E8CFF0",
    fg="#5A3D6B",
    command=complete_task
).grid(row=1, column=1, padx=5, pady=5)

tk.Button(
    button_frame,
    text="🔍 Search Task",
    width=18,
    font=("Arial", 11, "bold"),
    bg="#E8CFF0",
    fg="#5A3D6B",
    command=search_task
).grid(row=2, column=0, columnspan=2, pady=8)

listbox = tk.Listbox(
    root,
    width=75,
    height=13,
    font=("Arial", 12),
    bd=3,
    relief="groove"
)
listbox.pack(pady=15)

load_tasks()

root.mainloop()