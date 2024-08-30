import tkinter as tk
from tkinter import messagebox

def validate_input(value):
    # Проверка, что введенное значение содержит только цифры
    return value.isdigit()

def get_computer_number():
    def on_button_click():
        # Действие при нажатии на кнопку
        computer_number = entry.get()
        if computer_number:
            root.computer_number = int(computer_number)
            root.quit()  # Завершаем главный цикл приложения
        else:
            messagebox.showwarning("Предупреждение", "Пожалуйста, введите номер компьютера.")
    
    def center_window(window):
        window.update_idletasks()  # Обновляем информацию о размере окна
        width = window.winfo_width()
        height = window.winfo_height()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry(f'{width}x{height}+{x}+{y}')

    # Создаем главное окно
    root = tk.Tk()
    root.title("Введите номер компьютера")
    root.computer_number = None  # Инициализация переменной для хранения числа

    # Удаляем рамки окна
    root.overrideredirect(True)

    # Создаем надпись
    label = tk.Label(root, text="Введите номер компьютера:")
    label.pack(pady=10)

    # Валидатор для ввода только чисел
    vcmd = (root.register(validate_input), '%P')

    # Создаем поле ввода
    entry = tk.Entry(root, validate='key', validatecommand=vcmd)
    entry.pack(pady=10)

    # Создаем кнопку
    button = tk.Button(root, text="Подтвердить", command=on_button_click)
    button.pack(pady=10)

    # Центрируем окно на экране
    center_window(root)

    # Запуск главного цикла приложения
    root.mainloop()

    return root.computer_number  # Возвращаем введенное число
