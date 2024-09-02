import tkinter as tk
from tkinter import messagebox

def validate_input(value):
    # Проверка, что введенное значение содержит только цифры или пустую строку
    return value.isdigit() or value == ""

def get_computer_and_server():
    def on_button_click():
        # Действие при нажатии на кнопку
        computer_number = entry_computer.get()
        server_name = entry_server.get()

        if computer_number and server_name:
            root.computer_number = int(computer_number)
            root.server_name = server_name
            root.quit()  # Завершаем главный цикл приложения
        else:
            messagebox.showwarning("Предупреждение", "Пожалуйста, введите номер компьютера и имя сервера.")

    def close_window():
        root.quit()  # Корректно завершаем главный цикл приложения
        root.destroy()  # Полностью закрываем окно

    def center_window(window):
        window.update_idletasks()  # Обновляем информацию о размере окна
        width = window.winfo_width()
        height = window.winfo_height()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry(f'{width}x{height}+{x}+{y}')

    # Создаем главное окно
    root = tk.Tk()
    root.title("Введите номер компьютера и сервер")
    root.computer_number = None  # Инициализация переменной для хранения числа
    root.server_name = None  # Инициализация переменной для хранения имени сервера

    # Удаляем рамки окна (если необходимо)
    root.overrideredirect(True)

    # Создаем надпись для номера компьютера
    label_computer = tk.Label(root, text="Введите номер компьютера:")
    label_computer.pack(pady=10)

    # Валидатор для ввода только чисел
    vcmd = (root.register(validate_input), '%P')

    # Создаем поле ввода для номера компьютера
    entry_computer = tk.Entry(root, validate='key', validatecommand=vcmd)
    entry_computer.pack(pady=10)

    # Создаем надпись для сервера
    label_server = tk.Label(root, text="Введите имя сервера:")
    label_server.pack(pady=10)

    # Создаем поле ввода для имени сервера
    entry_server = tk.Entry(root)
    entry_server.pack(pady=10)

    # Создаем кнопку
    button = tk.Button(root, text="Подтвердить", command=on_button_click)
    button.pack(pady=10)

    # Обработчик для закрытия окна
    root.protocol("WM_DELETE_WINDOW", close_window)

    # Центрируем окно на экране
    center_window(root)

    # Запуск главного цикла приложения
    root.mainloop()

    # После выхода из mainloop
    root.destroy()  # Полностью закрываем окно

    return root.computer_number, root.server_name  # Возвращаем введенные значения

# Пример использования функции
if __name__ == "__main__":
    computer_number, server_name = get_computer_and_server()
    print(f"Введённый номер компьютера: {computer_number}")
    print(f"Введённое имя сервера: {server_name}")
