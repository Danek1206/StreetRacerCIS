import tkinter as tk
from tkinter import filedialog, messagebox
import os
import shutil
import subprocess
import sys

class LauncherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Racer Dreams Launcher")
        self.root.geometry("400x300")
        self.install_path = None

        # Заголовок
        self.label = tk.Label(root, text="Racer Dreams: Пацанский Заезд", font=("Arial", 14))
        self.label.pack(pady=20)

        # Кнопка "Скачать"
        self.download_button = tk.Button(root, text="Скачать", command=self.download_game, font=("Arial", 12))
        self.download_button.pack(pady=10)

        # Кнопка "Играть" (изначально скрыта)
        self.play_button = tk.Button(root, text="Играть", command=self.play_game, font=("Arial", 12), state="disabled")
        self.play_button.pack(pady=10)

        # Статус
        self.status_label = tk.Label(root, text="Выбери папку для установки", font=("Arial", 10))
        self.status_label.pack(pady=20)

    def download_game(self):
        # Выбор папки
        self.install_path = filedialog.askdirectory(title="Выбери папку для установки")
        if not self.install_path:
            self.status_label.config(text="Установка отменена")
            return

        try:
            # Создаём папку игры
            game_folder = os.path.join(self.install_path, "RacerDreams")
            os.makedirs(game_folder, exist_ok=True)

            # Путь к текущему скрипту игры
            script_path = os.path.join(os.path.dirname(sys.argv[0]), "racer_dreams.py")
            if not os.path.exists(script_path):
                messagebox.showerror("Ошибка", "Файл racer_dreams.py не найден!")
                return

            # Копируем игру
            shutil.copy(script_path, game_folder)

            # Обновляем статус
            self.status_label.config(text=f"Игра установлена в {game_folder}")
            self.download_button.config(state="disabled")
            self.play_button.config(state="normal")
            messagebox.showinfo("Успех", "Игра установлена! Нажми 'Играть'.")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось установить: {str(e)}")
            self.status_label.config(text="Ошибка установки")

    def play_game(self):
        if not self.install_path:
            messagebox.showerror("Ошибка", "Игра не установлена!")
            return
        game_path = os.path.join(self.install_path, "RacerDreams", "racer_dreams.py")
        try:
            # Запускаем игру
            subprocess.run([sys.executable, game_path], check=True)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось запустить: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = LauncherApp(root)
    root.mainloop()