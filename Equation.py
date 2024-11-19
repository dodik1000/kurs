import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import ast

""" Класс для работы с уравнениями и их
 приближенным интегрированием методом Симпсона """


class Equation:
    def __init__(self, frame, parent, fx, a, b, n):
        """ Инициализация уравнения """
        self.parent = parent
        self.frame = frame
        self.fx = fx
        self.y = []

        try:
            self.a = float(a)
            self.b = float(b)
            self.n = int(n)
            self.h = (self.b - self.a) / self.n
            self.x = np.linspace(self.a, self.b, self.n + 1)

            try:
                ast.parse(fx)  # Вызовет SyntaxError, если fx недействителен
            except SyntaxError:
                raise ValueError("Синтаксическая ошибка.")

            # Создаем новое пространство имен
            self.local_namespace = {}

            # Импорт функции из модуля math в это пространство имен.
            # Это необходимо для того, чтобы были доступны
            # математические функции (sin, cos, exp),
            # которые могут использоваться в функции, введенной пользователем.
            exec("from math import *", self.local_namespace)

            # Вычисляем значения функции для каждого x
            for x_val in self.x:
                self.y_value = eval(self.fx, {"x": x_val}, self.local_namespace)
                self.y.append(self.y_value)
        except (NameError, ValueError, SyntaxError, TypeError) as e:
            CTkMessagebox(title="Ошибка",
                          message=f"Неверный формат введенных данных: {e}",
                          width=400, height=200, icon="warning")

    def simpson(self):
        """ Вызов функции подсчета и построения графика, вывод результата """
        result = self.calculate_simpson()
        if result is not None:
            self.answer_done = ctk.CTkLabel(self.frame, text=f"Ответ: {result:.5f}",
                                            font=('Arial Black', 18))
            self.answer_done.grid(row=5, column=0, columnspan=3,
                                  padx=10, pady=(5, 20), sticky="ew")
            self.plot_function()

    def calculate_simpson(self):
        """ Расчет интеграла методом Симпсона """
        try:
            if not self.y or len(self.y) < 2 or self.n < 1:
                raise ValueError("Неверный формат введенных данных!")

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

        except ValueError:
            CTkMessagebox(title="Ошибка ввода",
                          message="Неверный формат введенных данных",
                          width=400, height=200, icon="cancel")
            return None

    def plot_function(self):
        """ Построение графика функции """
        try:
            # Создаем фигуру и график
            self.fig, self.ax = plt.subplots(figsize=(4, 3.7))
            self.ax.plot(self.x, self.y, label=self.fx)
            self.ax.set_xlabel("x")
            self.ax.set_ylabel("y")
            self.ax.set_title("График функции")
            self.ax.legend()
            self.ax.grid(True)

            # Удаление предыдущего графика (если он был)
            if hasattr(self, "canvas"):
                self.canvas.grid_forget()
                self.canvas.figure.clf()  # Очистка фигуры
                plt.close(self.canvas.figure)  # Закрытие фигуры

            # Создание CanvasTkAgg
            self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
            self.canvas.draw()
            self.canvas.get_tk_widget().grid(row=6, column=0, columnspan=2,
                                             sticky='nsew', pady=(0, 10))

            # Настройка размеров фрейма
            self.frame.grid_rowconfigure(6, weight=1)
            self.frame.columnconfigure(0, weight=1)
            self.frame.columnconfigure(1, weight=1)
            plt.close()

        except Exception as e:
            CTkMessagebox(title="Ошибка",
                          message=f"Ошибка при построении графика: {e}",
                          width=300, height=200, icon="cancel")
