import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import ast

""" Класс для работы с уравнениями и их
 приближенным интегрированием методом Симпсона """


class Equation:
    def __init__(self, frame, parent, fx, a, b, n, theme, acc):
        """ Инициализация уравнения """
        self.parent = parent
        self.frame = frame
        self.fx = fx
        self.y = []
        self.theme = theme
        self.acc = acc

        if self.theme == "Dark":
            plt.rcParams.update({
                'axes.facecolor': '#282828',  # Цвет фона графика
                'axes.edgecolor': '#ffffff',  # Цвет рамки графика
                'axes.labelcolor': '#ffffff',  # Цвет меток осей
                'xtick.color': '#ffffff',  # Цвет меток по оси X
                'ytick.color': '#ffffff',  # Цвет меток по оси Y
                'figure.facecolor': '#202020',  # Цвет фона фигуры
                'grid.color': '#666666',  # Цвет сетки
                'text.color': '#ffffff'  # Цвет текста
            })
        elif theme == "Light":
            plt.rcParams.update({
                'axes.facecolor': '#f3f3f3',  # Цвет фона графика
                'axes.edgecolor': '#000000',  # Цвет рамки графика
                'axes.labelcolor': '#000000',  # Цвет меток осей
                'xtick.color': '#000000',  # Цвет меток по оси X
                'ytick.color': '#000000',  # Цвет меток по оси Y
                'figure.facecolor': '#f3f3f3',  # Цвет фона фигуры
                'grid.color': '#000000',  # Цвет сетки
                'text.color': '#000000'  # Цвет текста
            })

        try:
            self.n = int(n)
            try:
                ast.parse(fx)  # Вызовет SyntaxError, если fx недействителен
            except SyntaxError:
                raise ValueError("Синтаксическая ошибка.")

            # Пространство имен
            self.local_namespace = {}

            # Импорт функции из модуля numpy в это пространство имен.
            # Это необходимо для того, чтобы были доступны
            # математические функции (sin, cos, exp),
            # которые могут использоваться в функции, введенной пользователем.
            exec("from numpy import *", self.local_namespace)

            self.a = eval(a, self.local_namespace)
            self.b = eval(b, self.local_namespace)
            self.h = (self.b - self.a) / self.n
            self.x = np.linspace(self.a, self.b, self.n + 1)

            if 'sqrt' in self.fx:  # Проверка на наличие sqrt
                if self.a < 0 or self.b < 0:
                    raise ValueError(
                        "Пределы интегрирования должны быть неотрицательными, "
                        "если функция содержит sqrt.")
            if 'log' in self.fx:  # Проверка на наличие log
                if self.a <= 0 or self.b <= 0:
                    raise ValueError(
                        "Пределы интегрирования должны быть положительными, "
                        "если функция содержит log.")

            # Вычисление значения функции для каждого x
            with np.errstate(divide='ignore', invalid='ignore'):
                for x_val in self.x:
                    self.y_value = eval(self.fx, {"x": x_val}, self.local_namespace)
                    self.y.append(self.y_value)
        except (NameError, ValueError, SyntaxError, TypeError, ZeroDivisionError) as e:
            return

    def simpson(self):
        """ Вызов функции подсчета и построения графика, вывод результата """
        result = self.calculate_simpson()
        if result is not None:
            # Создание нового фрейма для размещения всех лейблов
            self.integral_frame = ctk.CTkFrame(self.frame,
                                               fg_color=self.frame.cget('fg_color'))
            self.integral_frame.grid(row=6, column=0, columnspan=4, padx=(0, 0))

            # Лейбл для верхнего предела интегрирования
            self.answer_b = ctk.CTkLabel(self.integral_frame, text=f"{self.b:.1f}",
                                         font=('Arial Black', 12))
            self.answer_b.grid(row=0, column=0, padx=(10, 0), sticky="ne")

            # Лейбл для символа интеграла
            self.answer_int = ctk.CTkLabel(self.integral_frame, text="∫",
                                           font=('Arial Black', 35))
            self.answer_int.grid(row=1, column=0, padx=(10, 0), sticky="e")

            # Лейбл для нижнего предела интегрирования
            self.answer_a = ctk.CTkLabel(self.integral_frame, text=f"{self.a:.1f}",
                                         font=('Arial Black', 12))
            self.answer_a.grid(row=2, column=0, padx=(10, 0), sticky="e")

            # Лейбл для функции и результата
            self.answer_done = ctk.CTkLabel(self.integral_frame,
                                            text=f"{self.fx} dx "
                                                 f"= {result:.{self.acc}f}\n",
                                            font=('Arial Black', 18))
            self.answer_done.grid(row=1, column=1, rowspan=2, sticky="w")

            self.plot_function()
            return f"{result:.{self.acc}f}", self.integral_frame
        else:
            return None, None

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
        try:
            self.fig, self.ax = plt.subplots(figsize=(7, 3))
            self.ax.plot(self.x, self.y, label=self.fx,
                         color="#8e84a1", linewidth=2.5)
            plt.title('График подынтегральной функции')
            plt.xlabel('x')
            plt.ylabel('f(x)')
            plt.grid()

            # Интерактивное изменение числа разбиений
            n_steps = [self.n + i * 2 for i in range(20)]
            bars = []
            for n in n_steps:

                y_step = [eval(self.fx, {"x": xi}, self.local_namespace) for xi in
                          self.x]
                bar = self.ax.fill_between(self.x, 0, y_step, color="#a9a0b7",
                                      alpha=0.05)
                bars.append(bar)

            if hasattr(self, "canvas"):
                self.canvas.get_tk_widget().destroy()

            self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
            self.canvas.draw()
            self.canvas.get_tk_widget().grid(row=7, column=0, columnspan=2,
                                             sticky='s', pady=(0, 10))

            self.frame.grid_rowconfigure(6, weight=1)
            self.frame.columnconfigure(0, weight=1)
            self.frame.columnconfigure(1, weight=1)
            plt.close()

        except Exception as e:
            CTkMessagebox(title="Ошибка",
                          message=f"Ошибка при построении графика: {e}", width=300,
                          height=200, icon="cancel")
