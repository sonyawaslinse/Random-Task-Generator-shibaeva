import tkinter as tk
from tkinter import ttk, messagebox
import json
import random
import os

# Предопределённые задачи
tasks_list = [
    {"task": "Прочитать статью", "type": "учёба"},
    {"task": "Сделать зарядку", "type": "спорт"},
    {"task": "Написать отчет", "type": "работа"},
    {"task": "Учиться новой теме", "type": "учёба"},
    {"task": "Пробежка на улицы", "type": "спорт"},
    {"task": "Обсудить проект", "type": "работа"},
]

# Файл для сохранения истории
history_file = 'tasks.json'

def load_history():
    """Загружает историю из файла JSON."""
    if not os.path.exists(history_file):
        return []
    try:
        with open(history_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def save_history(history):
    """Сохраняет историю в файл JSON."""
    with open(history_file, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=4)

def generate_task():
    """Генерирует случайную задачу по фильтру."""
    selected_type = filter_var.get()
    if selected_type == "Все":
        filtered_tasks = tasks_list
    else:
        filtered_tasks = [t for t in tasks_list if t['type'] == selected_type]

    if not filtered_tasks:
        messagebox.showwarning("Нет задач", "Нет задач для выбранного фильтра.")
        return

    task = random.choice(filtered_tasks)
    current_task_var.set(task['task'])

    # Обновляем историю
    history = load_history()
    history.append(task)
    save_history(history)
    update_history_list()

def update_history_list():
    """Обновляет список истории в интерфейсе."""
    history = load_history()
    listbox.delete(0, tk.END)
    for t in history:
        listbox.insert(tk.END, f"{t['task']} ({t['type']})")

def add_task():
    """Добавляет новую задачу в список и сохраняет."""
    task_text = new_task_entry.get().strip()
    task_type = new_task_type_var.get()
    if task_text == "":
        messagebox.showerror("Ошибка", "Введите описание задачи.")
        return
    new_task = {"task": task_text, "type": task_type}
    tasks_list.append(new_task)

    # Добавляем сразу в историю, чтобы увидеть добавленную задачу
    history = load_history()
    history.append(new_task)
    save_history(history)

    update_history_list()
    new_task_entry.delete(0, tk.END)

# Инициализация главного окна
root = tk.Tk()
root.title("Random Task Generator")
root.geometry("500x600")

# Переменные
current_task_var = tk.StringVar()
filter_var = tk.StringVar(value="Все")
new_task_type_var = tk.StringVar(value="учёба")

# Создание интерфейса
ttk.Label(root, text="Текущая задача:", font=("Arial", 12)).pack(pady=5)
ttk.Label(root, textvariable=current_task_var, font=("Arial", 16, "bold")).pack(pady=5)

ttk.Button(root, text="Сгенерировать задачу", command=generate_task).pack(pady=10)

ttk.Label(root, text="Фильтр по типу:", font=("Arial", 10)).pack(pady=2)

filter_options = ["Все", "учёба", "спорт", "работа"]
filter_menu = ttk.OptionMenu(root, filter_var, *filter_options)
filter_menu.pack(pady=2)

ttk.Label(root, text="История:", font=("Arial", 10)).pack(pady=5)

# Список для отображения истории
listbox = tk.Listbox(root, height=12, width=50)
listbox.pack(pady=5)

# Раздел добавления новой задачи
ttk.Label(root, text="Добавить новую задачу:", font=("Arial", 10)).pack(pady=5)
new_task_entry = ttk.Entry(root, width=50)
new_task_entry.pack(pady=2)

ttk.Label(root, text="Тип задачи:", font=("Arial", 10)).pack(pady=2)
task_type_menu = ttk.OptionMenu(root, new_task_type_var, "учёба", "учёба", "спорт", "работа")
task_type_menu.pack(pady=2)

ttk.Button(root, text="Добавить задачу", command=add_task).pack(pady=10)

# Обновить историю при запуске
update_history_list()

# Запуск GUI
root.mainloop()