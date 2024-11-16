"""В этом файле находится код для класса Equation, который
используется для работы с функцией и её параметрами"""

import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Equation:
    def __init__(self, frame, parent, fx, a, b, n):
        self.parent = parent
        self.frame = frame

        self.fx = fx
        self.a = float(a)
        self.b = float(b)
        self.n = int(n)

        self.h = (self.b - self.a) / self.n
        self.x = np.linspace(self.a, self.b, self.n + 1)
        self.y = []  # Создаем пустой список для y

        # Создаем новое пространство имен
        self.local_namespace = {}

        # Импортируем функции из math в новое пространство имен
        exec("from math import *", self.local_namespace)

        # Вычисляем значения функции для каждого x
        for i in range(len(self.x)):
            # Исправляем замену x
            self.y_value = eval(self.fx, {"x": self.x[i]}, self.local_namespace)
            self.y.append(self.y_value)

    def simpson(self):
        """Вызывает функцию подсчета определенного интеграла методом Симпсона и отображает результат."""
        try:
            # Вычисление интеграла по методу Симпсона
            result = self.calculate_simpson()

            if result is not None:
                self.answer_done = ctk.CTkLabel(self.frame, text=f"Ответ: {result:.5f}",
                                                font=('Arial Black', 18))
                self.answer_done.grid(row=5, column=0, columnspan=3, padx=10, pady=(5, 20), sticky="ew")

        except ValueError:
            CTkMessagebox(title="Ошибка", message="Некорректный формат введенных данных!", width=300, height=200,
                          icon="cancel")

    def calculate_simpson(self):
        """Вычисляет определенный интеграл методом Симпсона"""
        # Создаем новое пространство имен
        try:
            y0 = self.y[0]
            yn = self.y[-1]
            sum_even = 0
            sum_odd = 0

            for i in range(1, self.n, 2):
                sum_odd += self.y[i]
            for i in range(2, self.n, 2):
                sum_even += self.y[i]

            integral = self.h / 3 * (y0 + yn + 2 * sum_even + 4 * sum_odd)
            return integral
        except NameError:
            CTkMessagebox(title="Ошибка", message="Некорректный формат введенных данных!", width=300, height=200,
                          icon="cancel")
            return None  # Возвращаем None при ошибке

    def plot_function(self):
        try:
            # Создаем фигуру и график
            fig, ax = plt.subplots(figsize=(4, 3.7))
            ax.plot(self.x, self.y, label=self.fx)
            ax.set_xlabel("x")
            ax.set_ylabel("y")
            ax.set_title("График функции")
            ax.legend()
            ax.grid(True)

            # Удаляем предыдущий график (если он был)
            if hasattr(self, "canvas"):
                self.canvas.get_tk_widget().destroy()

            # Создаем CanvasTkAgg
            self.canvas = FigureCanvasTkAgg(fig, master=self.frame)
            self.canvas.draw()
            self.canvas.get_tk_widget().grid(row=6, column=0, columnspan=2, sticky='nsew', pady=(0, 10))

            # Настройка размеров фрейма
            self.frame.grid_rowconfigure(6, weight=1)
            self.frame.columnconfigure(0, weight=1)
            self.frame.columnconfigure(1, weight=1)

        except Exception as e:
            CTkMessagebox(title="Ошибка", message=f"Ошибка при построении графика: {e}",
                          width=300, height=200, icon="cancel")
