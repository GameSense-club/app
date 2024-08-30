import tkinter as tk

def create_popup():
    # Создаем основное окно
    popup = tk.Tk()
    
    # Устанавливаем стиль окна
    popup.overrideredirect(True)  # Убираем границы и заголовок окна
    popup.wm_attributes("-topmost", True)  # Делаем окно всегда сверху

    # Получаем размеры экрана
    screen_width = popup.winfo_screenwidth()
    screen_height = popup.winfo_screenheight()

    # Устанавливаем размер окна (например, 200x100)
    popup.geometry("260x150+{}+{}".format(screen_width - 260, 0))

    # Добавляем текст в окно
    label = tk.Label(popup, text="У вас осталось 5 минут!", font=("Poppins", 16), fg="white", bg="#2a1557")
    label.pack(expand=True, fill=tk.BOTH)

    # Скрываем окно через 5 секунд
    popup.after(5000, popup.destroy)

    # Запускаем основной цикл
    popup.mainloop()