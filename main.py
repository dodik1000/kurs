import customtkinter as ctk
from PIL import Image
from Equation import Equation
from Database import Database
from tkinter import filedialog
from CTkMessagebox import CTkMessagebox


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        '''------------------- НАСТРОЙКА ОКНА -------------------'''

        self.title("Калькулятор для вычисления интегралов методом Симпсона")
        self.geometry("900x700+450+100")
        self.resizable(width=False, height=False)

        # region: Конфигурация окна
        self.grid_columnconfigure(1,
                                  weight=1)  # Основная область контента расширяется
        self.grid_columnconfigure(0, weight=0)  # Боковая панель не расширяется
        self.grid_rowconfigure(0, weight=0)  # Меню не расширяется по вертикали
        self.grid_rowconfigure((1, 2, 3), weight=1)  # Расширение строк

        # endregion

        # Инициализация таймера бездействия
        self.idle_timer_id = self.after(60000, self.show_idle_warning)

        # Инициализация переменной для удаления окна
        self.new_window_deleter = None
        self.int_frame_deleter = None
        self.calculations_result = None
        self.precision = 4

        self.calculations_result = None

        # Установка обработчика события закрытия окна
        self.protocol("WM_DELETE_WINDOW", self.close_program)

        # region : Фреймы для различных частей приложения

        self.sidebar_frame = ctk.CTkFrame(self, width=140, corner_radius=0,
                                          fg_color="#202020")
        self.main_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="#202020")
        self.group_frame = ctk.CTkFrame(self.main_frame, fg_color="#202020")
        self.button_frame = ctk.CTkFrame(self.main_frame, fg_color="#202020")
        self.calculate_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="#202020")
        self.calculate_frame.grid_rowconfigure(7, weight=1)
        self.about_author_frame = ctk.CTkFrame(self, corner_radius=0,
                                               fg_color="#202020")
        self.about_program_frame = ctk.CTkFrame(self, corner_radius=0,
                                                fg_color="#202020")
        self.about_program_group = ctk.CTkFrame(self.about_program_frame,
                                                corner_radius=0,
                                                fg_color="#202020")
        self.menu_bar_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="#282828",
                                           height=40, width=900)
        self.show_help_frame = ctk.CTkScrollableFrame(self, corner_radius=0,
                                                      fg_color="#202020")
        # endregion

        # Текущий фрейм
        self.current_frame = self.main_frame

        '''------------------- MENU BAR FRAME -------------------'''


        self.menu_bar_frame.grid_propagate(False)
        self.menu_bar_frame.rowconfigure(0, weight=1)

        # region: Оформление меню
        self.image_save = Image.open("materials/saveicon.png")
        self.ctk_image_save = ctk.CTkImage(light_image=self.image_save, size=(18, 18))

        # Кнопка "Сохранить"
        self.save_me_button = ctk.CTkButton(self.menu_bar_frame,
                                            image=self.ctk_image_save,
                                            text="Сохранить", fg_color="#7d748e",
                                            hover_color="#545164", width=30,
                                            height=15, font=("Arial black", 12),
                                            command=self.save_file)
        self.save_me_button.grid(row=0, column=0, padx=(20, 5))

        self.image_open = Image.open("materials/openicon.png")
        self.ctk_image_save = ctk.CTkImage(light_image=self.image_open, size=(18, 18))

        # Кнопка "Открыть"
        self.open_me_button = ctk.CTkButton(self.menu_bar_frame,
                                            image=self.ctk_image_save,
                                            text="Открыть", fg_color="#7d748e",
                                            hover_color="#545164", width=30,
                                            height=15, font=("Arial black", 12),
                                            command=self.open_file)
        self.open_me_button.grid(row=0, column=1, padx=5)

        # Перегородка между кнопками
        self.separator1 = ctk.CTkLabel(self.menu_bar_frame, text="", width=2,
                                       height=20, fg_color="#7d748e")
        self.separator1.grid(row=0, column=2, padx=5)

        self.image_clear = Image.open("materials/clearicon.png")
        self.ctk_image_clear = ctk.CTkImage(light_image=self.image_clear,
                                            size=(18, 18))

        # Кнопка "Очистить поля"
        self.clear_me_button = ctk.CTkButton(self.menu_bar_frame,
                                             image=self.ctk_image_clear,
                                             text="Очистить поля", fg_color="#7d748e",
                                             hover_color="#545164", width=30,
                                             height=15, font=("Arial black", 12),
                                             command=self.clear_me)
        self.clear_me_button.grid(row=0, column=3, padx=5)

        # Перегородка между кнопками
        self.separator2 = ctk.CTkLabel(self.menu_bar_frame, text="", width=2,
                                       height=20, fg_color="#7d748e")
        self.separator2.grid(row=0, column=4, padx=5)

        self.slider_name = ctk.CTkLabel(self.menu_bar_frame, width=2,
                                        text="Количество знаков после запятой:",
                                        height=20, font=("Arial Black", 12))
        self.slider_name.grid(row=0, column=5, padx=5)

        # Слайдер для установки количества знаков после запятой в ответе
        self.slider_1 = ctk.CTkSlider(self.menu_bar_frame, from_=1, to=9, width=90,
                                      number_of_steps=8, button_color="#7d748e",
                                      command=lambda value: setattr(self, 'precision',
                                                                    int(float(
                                                                        value))),
                                      button_hover_color="#7d748e")
        self.slider_1.grid(row=0, column=6, padx=5)

        # Перегородка между кнопками
        self.separator3 = ctk.CTkLabel(self.menu_bar_frame, text="", width=2,
                                       height=20, fg_color="#7d748e")
        self.separator3.grid(row=0, column=7, padx=(10, 10))

        self.image_help = Image.open("materials/helpicon.png")
        self.ctk_image_help = ctk.CTkImage(light_image=self.image_help, size=(18, 18))

        # Кнопка "Помощь"
        self.help_me_button = ctk.CTkButton(self.menu_bar_frame,
                                            image=self.ctk_image_help,
                                            text="Помощь", fg_color="#7d748e",
                                            hover_color="#545164", width=30,
                                            height=15, font=("Arial Black", 12),
                                            command=lambda: self.switch_frame
                                            (self.show_help_frame))
        self.help_me_button.grid(row=0, column=8)

        # endregion

        '''------------------- SIDEBAR FRAME -------------------'''

        # Размещение фрейма
        self.sidebar_frame.grid(row=1, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        # region : Размещение кнопок и меток боковой панели
        # Кнопка "Главная"
        self.main_button = ctk.CTkButton(self.sidebar_frame, text="Главная",
                                         fg_color="#7d748e", hover_color="#545164",
                                         command=lambda:
                                         self.switch_frame(self.main_frame),
                                         width=147, height=30)
        self.main_button.grid(row=0, column=0, padx=20, pady=(10, 0))

        # Кнопка "Калькулятор"
        self.calculate_button = ctk.CTkButton(self.sidebar_frame, text="Калькулятор",
                                              fg_color="#7d748e",
                                              hover_color="#545164",
                                              command=lambda:
                                              self.switch_frame(self.calculate_frame),
                                              width=147, height=30)
        self.calculate_button.grid(row=1, column=0, padx=20, pady=(10, 0))

        # Кнопка "Об авторе"
        self.about_author_button = (ctk.CTkButton
                                    (self.sidebar_frame, text="Об авторе",
                                     fg_color="#7d748e", hover_color="#545164",
                                     command=lambda:
                                     self.switch_frame(self.about_author_frame),
                                     width=147, height=30))
        self.about_author_button.grid(row=2, column=0, padx=20, pady=(10, 0))

        # Кнопка "О программе"
        self.about_program_button = (ctk.CTkButton
                                     (self.sidebar_frame, text="О программе",
                                      fg_color="#7d748e", hover_color="#545164",
                                      command=lambda:
                                      self.switch_frame(self.about_program_frame),
                                      width=147, height=30))
        self.about_program_button.grid(row=3, column=0, padx=20, pady=(10, 0))

        # Кнопка "История вычислений"
        self.recent_button = ctk.CTkButton(self.sidebar_frame,
                                           text="История вычислений",
                                           fg_color="#7d748e", hover_color="#545164",
                                           command=self.show_calculation_history,
                                           state="enabled",
                                           width=147, height=30)
        self.recent_button.grid(row=4, column=0, padx=20, pady=(10, 0), sticky="n")

        # Отступ между кнопками и этикеткой темы
        self.padding_label = ctk.CTkLabel(self.sidebar_frame, text="", anchor="w")
        self.padding_label.grid(row=5, column=0)  # Пустой элемент для отступа

        # Выбор темы
        self.appearance_mode_label = ctk.CTkLabel(self.sidebar_frame,
                                                  text="Тема:", anchor="w")
        self.appearance_mode_label.grid(row=6, column=0, padx=20, pady=(10, 0))

        self.appearance_mode_option_menu = (
            ctk.CTkOptionMenu(self.sidebar_frame, values=["Светлая", "Темная"],
                              command=self.change_theme, fg_color="#7d748e",
                              button_color="#7d748e", button_hover_color="#545164"))
        self.appearance_mode_option_menu.grid(row=7, column=0, padx=20, pady=(10, 30))
        # endregion

        '''------------------- MAIN FRAME -------------------'''

        # Размещение главного фрейма
        self.main_frame.grid(row=1, column=1, rowspan=4, sticky="nsew")

        # Установка темной темы по умолчанию
        ctk.set_appearance_mode("Dark")
        self.appearance_mode_option_menu.set("Темная")

        # region: Оформление главного окна

        # Название университета, факультета, кафедры
        self.label_uni = (
            ctk.CTkLabel(self.main_frame,
                         text="Белорусский национальный технический университет"
                              "\n\n"
                              "Факультет информационных технологий и робототехники"
                              "\n\nПрограммное обеспечение информационных "
                              "систем и технологий",
                         font=("Arial Black", 16)))
        self.label_uni.grid(pady=(10, 60))

        # Название проекта
        self.label_course = ctk.CTkLabel(self.main_frame, text="Курсовой проект",
                                         font=("Arial Black", 24))
        self.label_course.grid()
        self.label_subject = ctk.CTkLabel(self.main_frame,
                                          text="по дисциплине Языки программирования",
                                          font=("Arial Black", 16))
        self.label_subject.grid()

        # Название темы курсового проекта
        self.label_theme = ctk.CTkLabel(self.main_frame,
                                        text="Вычисление определенных "
                                             "интегралов методом Симпсона",
                                        font=("Arial Black", 20))
        self.label_theme.grid(pady=(0, 30))

        # Загрузка изображения
        self.image = Image.open("materials/integral_calculator.png")
        self.ctk_image = ctk.CTkImage(light_image=self.image, size=(150, 150))

        self.group_frame.grid()

        self.label_student = ctk.CTkLabel(self.group_frame,
                                          text="Выполнил: Студент группы 10701123",
                                          font=("Arial Black", 16))
        self.label_student.grid(row=0, column=1, sticky="w")

        self.label_student_name = ctk.CTkLabel(self.group_frame,
                                               text="Макаров Артём Сергеевич",
                                               font=("Arial Black", 16))
        self.label_student_name.grid(row=1, column=1, sticky="w")

        self.teach = ctk.CTkLabel(self.group_frame,
                                  text="Преподователь: к.ф.-м.н., доц.",
                                  font=("Arial Black", 16))
        self.teach.grid(row=2, column=1, sticky="w")

        self.teach_name = ctk.CTkLabel(self.group_frame,
                                       text="Сидорик Валерий Владимирович",
                                       font=("Arial Black", 16))
        self.teach_name.grid(row=3, column=1, sticky="w")

        self.label_image = ctk.CTkLabel(self.group_frame, image=self.ctk_image,
                                        text="")
        self.label_image.grid(row=0, column=0, rowspan=4, padx=100)

        self.label_year = ctk.CTkLabel(self.main_frame, text="Минск, 2024",
                                       font=("Arial Black", 16))
        self.label_year.grid(pady=(120, 0))

        self.button_frame.grid(sticky="s", pady=(20, 30))

        self.button_continue = ctk.CTkButton(self.button_frame,
                                             text="Далее", fg_color="#7d748e",
                                             hover_color="#545164", width=300,
                                             height=50, font=("Arial Black", 16),
                                             command=lambda:
                                             self.switch_frame(self.calculate_frame))
        self.button_continue.grid(row=0, column=0, padx=10)

        self.button_exit = ctk.CTkButton(self.button_frame, text="Выход",
                                         fg_color="#7d748e", hover_color="#545164",
                                         width=300, height=50,
                                         font=("Arial Black", 16),
                                         command=self.close_program)
        self.button_exit.grid(row=0, column=1, padx=10)
        # endregion

        '''------------------- CALCULATE FRAME -------------------'''

        # region: оформление calculate frame
        # Функция
        self.func_label = (
            ctk.CTkLabel(self.calculate_frame,
                         text="Функция (используйте 'x' как переменную):",
                         font=('Arial Black', 14)))
        self.func_label.grid(row=0, column=0, padx=20, pady=10, sticky="w")

        self.entry_func = ctk.CTkEntry(self.calculate_frame, width=300,
                                       font=('Arial Black', 14))
        self.entry_func.grid(row=0, column=1, columnspan=2, padx=10, pady=10,
                             sticky="nsew")

        # Нижний предел (a):
        self.label_a = ctk.CTkLabel(self.calculate_frame, text="Нижний предел (a):",
                                    font=('Arial Black', 14))
        self.label_a.grid(row=1, column=0, padx=20, pady=10, sticky="w")

        self.entry_a = ctk.CTkEntry(self.calculate_frame, width=100,
                                    font=('Arial Black', 14))
        self.entry_a.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        self.entry_a.insert(0, "-1")

        # Верхний предел (b):
        self.label_b = ctk.CTkLabel(self.calculate_frame, text="Верхний предел (b):",
                                    font=('Arial Black', 14))
        self.label_b.grid(row=2, column=0, padx=20, pady=10, sticky="w")

        self.entry_b = ctk.CTkEntry(self.calculate_frame, width=100,
                                    font=('Arial Black', 14))
        self.entry_b.grid(row=2, column=1, padx=10, pady=10, sticky="w")
        self.entry_b.insert(0, "1")

        # Количество точек (n):
        self.label_dots = ctk.CTkLabel(self.calculate_frame,
                                       text="Количество точек (n):",
                                       font=('Arial Black', 14))
        self.label_dots.grid(row=3, column=0, padx=20, pady=10, sticky="w")

        self.entry_n = ctk.CTkEntry(self.calculate_frame, width=100,
                                    font=('Arial Black', 14))
        self.entry_n.grid(row=3, column=1, padx=10, pady=10, sticky="w")
        self.entry_n.insert(0, "1000")

        # Кнопка для вычисления интеграла
        self.but = ctk.CTkButton(self.calculate_frame, text="Вычислить",
                                 font=('Arial Black', 14),
                                 fg_color="#7d748e", hover_color="#545164",
                                 command=self.calculate_answer)
        self.but.grid(row=4, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

        # endregion

        '''------------------- ABOUT AUTHOR FRAME -------------------'''

        # region: оформление about author frame

        self.ab_author_label = ctk.CTkLabel(self.about_author_frame,
                                            text="Автор",
                                            font=("Arial Black", 20))
        self.ab_author_label.grid(row=0, column=1, padx=200,
                                  pady=(15, 15), sticky="nsew")

        self.image_author = Image.open("materials/author.jpg")
        self.ctk_image3 = ctk.CTkImage(light_image=self.image_author, size=(280, 280))
        self.label_image3 = ctk.CTkLabel(self.about_author_frame,
                                         image=self.ctk_image3, text="")
        self.label_image3.grid(row=1, column=1, padx=10, sticky="nsew")

        self.auth_label1 = ctk.CTkLabel(self.about_author_frame,
                                        text="Студент группы 10701123"
                                        "\n\nМакаров Артём Сергеевич"
                                        "\n\nartemmakarovv05@gmail.com",
                                        font=("Arial Black", 18))
        self.auth_label1.grid(row=2, column=1, padx=200, pady=(30, 5), sticky="nsew")

        self.image2 = Image.open("materials/bntu.png")
        self.ctk_image2 = ctk.CTkImage(light_image=self.image2, size=(180, 180))
        self.label_image2 = ctk.CTkLabel(self.about_author_frame,
                                         image=self.ctk_image2, text="")
        self.label_image2.grid(row=3, column=1, padx=10,  sticky="nsew")

        # endregion

        '''------------------- ABOUT PROGRAM FRAME -------------------'''

        # region: оформление about program frame
        self.auth_label1 = ctk.CTkLabel(self.about_program_frame,
                                        text="О программе\n\n"
                                             "Вычисление определенных интегралов\n"
                                             "методом Симпсона",
                                        font=("Arial Black", 18))
        self.auth_label1.grid(row=0, column=0, pady=(10, 30))
        self.about_program_group.grid(row=1, column=0, padx=10, sticky="nsew")
        self.image3 = Image.open("materials/about.png")
        self.ctk_image3 = ctk.CTkImage(light_image=self.image3, size=(180, 160))
        self.label_image3 = ctk.CTkLabel(self.about_program_group,
                                         image=self.ctk_image3, text="")
        self.label_image3.grid(row=1, column=0, padx=10)

        self.description_label = (
            ctk.CTkLabel(self.about_program_group,
                         text="Данная программа предназначена для вычисления "
                              "определенных интегралов с помощью метода Симпсона. "
                              "Метод Симпсона является одним из наиболее "
                              "распространенных численных методов интегрирования, "
                              "который аппроксимирует область под кривой "
                              "интеграла с помощью парабол.",
                         font=("Arial Black", 14), wraplength=500, justify="left"))
        self.description_label.grid(row=1, column=1, pady=15)

        # Возможности
        self.features_label = ctk.CTkLabel(self.about_program_frame,
                                           text="Основные возможности:",
                                           font=("Arial Black", 14))
        self.features_label.grid(pady=10)

        self.features_text = (
            ctk.CTkLabel(self.about_program_frame,
                         text="• Ввод функции: Пользователь может ввести функцию, "
                              "для которой необходимо вычислить интеграл. "
                              "В качестве переменной используется \"x\".\n"
                              "• Установка пределов интегрирования: "
                              "Пользователь задает нижний (a) и верхний "
                              "(b) пределы интегрирования.\n• "
                              "Указание количества точек: "
                              "Пользователь выбирает количество точек (n) "
                              "для разбиения "
                              "области интегрирования, что влияет на точность "
                              "вычислений.\n• Вычисление интеграла: "
                              "Программа вычисляет интеграл методом Симпсона "
                              "на основе введенных данных.\n"
                              "• Отображение результата: "
                              "Результат вычисления отображается на экране.",
                         font=("Arial Black", 12), padx=10,
                         wraplength=700, justify="left"))
        self.features_text.grid()

        # Преимущества метода Симпсона
        self.advantages_label = ctk.CTkLabel(self.about_program_frame,
                                             text="Преимущество метода Симпсона:",
                                             font=("Arial Black", 14))
        self.advantages_label.grid(pady=10)

        self.advantages_text = ctk.CTkLabel(self.about_program_frame,
                                            text="Относительная точность: "
                                                 "Метод Симпсона обычно обеспечивает "
                                                 "более высокую точность, чем методы "
                                                 "трапеций или прямоугольников.",
                                            font=("Arial Black", 12), wraplength=500,
                                            justify="left")
        self.advantages_text.grid()

        # endregion

        '''------------------- SHOW HELP FRAME -------------------'''

        # region: оформление show help frame
        self.auth_label1 = ctk.CTkLabel(self.show_help_frame,
                                        text="Помощь\n",
                                        font=("Arial Black", 18))
        self.auth_label1.grid(row=0, column=0, pady=(30, 5))

        # Помощь в использовании
        self.feature_text = (
            ctk.CTkLabel(self.show_help_frame,
                         text="Ввод функций:\n\n1. Степень:\n- Чтобы возвести число в"
                              " степень, используйте двойную звездочку (**).\n"
                              "Например, для возведения x в квадрат напишите `x**2`."
                              "\n\n2. Корень: \n- Для вычисления квадратного корня "
                              "используйте функцию `sqrt()`. Например, квадратный "
                              "корень из x: `sqrt(x)`.\n\n3. Математические "
                              "функции: \n- Вы можете использовать различные "
                              "математические функции, такие как `sin()`, `cos()`, "
                              "`tan()`, `log()`, и т.д.\nНапример, синус x: `sin(x)`."
                              "\n\nВвод пределов интегрирования:\n\n1. "
                              "Нижний предел: \n- Введите значение нижнего "
                              "предела интегрирования в соответствующее поле.\n\n"
                              "2. Верхний предел: \n- Введите значение верхнего "
                              "предела интегрирования в соответствующее поле. "
                              "\n\n! Обратите внимание: \n- В функциях, содержащих "
                              "логарифмы `log(x)`, значения x должны быть "
                              "положительными, чтобы избежать ошибок. \n- В функциях,"
                              " содержащих квадратные корни `sqrt(x)`, значения x "
                              "должны быть неотрицательными. \n- В функциях, "
                              "содержащих обратные тригонометрические функции "
                              "`arcsin(x)`, `arccos(x)`, значения x должны быть "
                              "в диапазоне [-1, 1]."
                              "\n\nПримеры ввода функций: "
                              "\n- Полиномиальная функция: `x**3 + 2*x**2 - 5*x + 1` "
                              "\n- Тригонометрическая функция: `sin(x) + cos(x)`"
                              "\n- Логарифмическая функция: `log(x)`\n\n\n\n\n",
                         font=("Arial Black", 14), padx=10,
                         wraplength=705, justify="left"))
        self.feature_text.grid()

        # endregion

    def change_theme(self, theme):
        """ Метод для смены темы приложения"""
        if theme == "Темная":
            ctk.set_appearance_mode("Dark")
            self.main_frame.configure(fg_color="#202020")
            self.sidebar_frame.configure(fg_color="#202020")
            self.group_frame.configure(fg_color="#202020")
            self.button_frame.configure(fg_color="#202020")
            self.calculate_frame.configure(fg_color="#202020")
            self.about_author_frame.configure(fg_color="#202020")
            self.about_program_frame.configure(fg_color="#202020")
            self.about_program_group.configure(fg_color="#202020")
            self.menu_bar_frame.configure(fg_color="#282828")
            self.show_help_frame.configure(fg_color="#202020")
        elif theme == "Светлая":
            ctk.set_appearance_mode("Light")
            self.main_frame.configure(fg_color="#f3f3f3")
            self.sidebar_frame.configure(fg_color="#f3f3f3")
            self.group_frame.configure(fg_color="#f3f3f3")
            self.button_frame.configure(fg_color="#f3f3f3")
            self.calculate_frame.configure(fg_color="#f3f3f3")
            self.about_author_frame.configure(fg_color="#f3f3f3")
            self.about_program_frame.configure(fg_color="#f3f3f3")
            self.about_program_group.configure(fg_color="#f3f3f3")
            self.menu_bar_frame.configure(fg_color="#E8E8E8")
            self.show_help_frame.configure(fg_color="#f3f3f3")

    def switch_frame(self, new_frame):
        """ Метод для смены фреймов """
        self.after_cancel(self.idle_timer_id)
        self.current_frame.grid_forget()
        if new_frame == self.calculate_frame:
            self.menu_bar_frame.grid(row=0, column=0, columnspan=2, sticky="ew")
            new_frame.grid(row=1, column=1, rowspan=4, sticky="nsew")
        else:
            self.menu_bar_frame.grid_forget()
            new_frame.grid(row=1, column=1, rowspan=4, sticky="nsew")
        self.current_frame = new_frame

    def close_program(self):
        """ Метод для закрытия приложения """
        if self.new_window_deleter is not None:
            self.new_window_deleter.destroy()
        if hasattr(self, 'idle_timer_id'):
            self.after_cancel(self.idle_timer_id)
        if hasattr(self, 'close_timer_id'):
            self.after_cancel(self.close_timer_id)
        if hasattr(self, 'update_countdown_id'):
            self.after_cancel(self.update_countdown_id)
        self.destroy()

    def calculate_answer(self):
        """ Вызывает вычисление ответа и обновляет историю """

        # Удаление предыдущего фрейма с результатами, если он существует
        if self.int_frame_deleter is not None:
            self.int_frame_deleter.grid_forget()

        self.eq = Equation(self.calculate_frame, self, self.entry_func.get(),
                           self.entry_a.get(), self.entry_b.get(), self.entry_n.get(),
                           ctk.get_appearance_mode(), self.precision)
        self.calculations_result, self.int_frame_deleter = self.eq.simpson()

        self.db = Database(self, self.entry_func.get(), self.entry_a.get(),
                           self.entry_b.get(), self.entry_n.get())
        self.db.update_history()
        self.db = None

    def show_calculation_history(self):
        self.recent_button.configure(state="disabled")
        # Включаем кнопку обратно через 2 секунды
        self.after(350, lambda: self.recent_button.configure(state="enabled"))

        if self.new_window_deleter is not None:
            self.new_window_deleter.destroy()
        self.switch_frame(self.calculate_frame)
        self.db = Database(self, self.entry_func.get(), self.entry_a.get(),
                           self.entry_b.get(), self.entry_n.get())
        self.new_window_deleter = self.db.history_window()
        self.db = None

    def continue_session(self):
        """ Метод для продолжения работы при бездействии пользователя"""
        self.warning_window.destroy()
        if hasattr(self, 'close_timer_id'):
            self.after_cancel(self.close_timer_id)
        if hasattr(self, 'update_countdown_id'):
            self.after_cancel(self.update_countdown_id)
        self.idle_timer_id = self.after(60000, self.show_idle_warning)

    def show_idle_warning(self):
        """Показывает окно с предупреждением о бездействии."""
        self.warning_window = ctk.CTkToplevel(self)
        self.warning_window.title("Предупреждение")
        self.warning_window.geometry("300x200")
        self.warning_window.resizable(width=False, height=False)
        self.seconds_left = 10
        # Таймер для автоматического закрытия
        self.close_timer_id = self.after(11000, self.close_program)

        self.label_warn = ctk.CTkLabel(self.warning_window,
                                       text='Вы были неактивны в течение 60 секунд. '
                                            'Продолжить? '
                                            'Нажмите "Да!" или программа '
                                            'автоматически закроется через',
                                       font=("Arial Black", 14), wraplength=285)
        self.label_warn.grid(pady=10, padx=(11, 10))

        # Лейбл для обратного отсчета
        self.countdown_label = ctk.CTkLabel(self.warning_window,
                                            text=f"{self.seconds_left}",
                                            font=("Arial Black", 20))
        self.countdown_label.grid(pady=(10, 0), padx=(11, 0))

        self.answer_warn_button = ctk.CTkButton(self.warning_window, text="Да!",
                                                command=self.continue_session,
                                                fg_color="#7d748e",
                                                hover_color="#545164", height=30)
        self.answer_warn_button.grid(pady=(30, 20), padx=(11, 0), sticky='nsew')
        # Запускаем таймер для обновления обратного отсчета
        self.update_countdown()

    def update_countdown(self):
        """Обновляет лейбл обратного отсчета."""
        if self.seconds_left > 0:
            self.seconds_left -= 1
            self.countdown_label.configure(text=f"{self.seconds_left}")
            # 1000 мс = 1 секунда
            self.update_countdown_id = self.after(1000, self.update_countdown)
        else:
            if hasattr(self, 'update_countdown_id'):
                self.after_cancel(self.update_countdown_id)
            self.close_program()

    def clear_me(self):
        """ Метод для очистки полей (кнопка "Очистить поля") """
        self.after_cancel(self.idle_timer_id)
        self.entry_func.delete(0, 'end')
        self.entry_func.insert(0, "")
        self.entry_a.delete(0, 'end')
        self.entry_a.insert(0, "")
        self.entry_b.delete(0, 'end')
        self.entry_b.insert(0, "")
        self.entry_n.delete(0, 'end')
        self.entry_n.insert(0, "")

    def save_file(self):
        """ Метод для сохранения полей и ответа (кнопка "Сохранить") """
        # Открытие диалогового окно сохранения файла
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text files", "*.txt")])
        if file_path:
            # Словарь для хранения значений полей и их названий
            fields = {
                'Функция': self.entry_func.get(),
                'Нижний предел': self.entry_a.get(),
                'Верхний предел': self.entry_b.get(),
                'Количество точек': self.entry_n.get(),
                'Результат': self.calculations_result
            }

            # Проверка, что все поля заполнены
            for name, value in fields.items():
                if not value:
                    CTkMessagebox(title="Ошибка",
                                  message=f"Поле '{name}' не должно быть пустым",
                                  width=300, height=200, icon="cancel")
                    return

            # Запись данных в файл
            with open(file_path, 'w', encoding='utf-8') as file:
                for name, value in fields.items():
                    file.write(f'{name}: {value}\n')
                CTkMessagebox(title="Сохранено",
                              message="Файл успешно сохранен",
                              width=300, height=200, icon="check")

    def open_file(self):
        """ Метод для открытия файла (кнопка "Открыть") """
        # Открытие диалогового окно открытия файла
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()

                # Очищение текущих значений полей ввода
                self.entry_func.delete(0, ctk.END)
                self.entry_a.delete(0, ctk.END)
                self.entry_b.delete(0, ctk.END)
                self.entry_n.delete(0, ctk.END)

                # Запись значений в соответствующие поля
                for line in lines:
                    if line.startswith('Функция:'):
                        self.entry_func.insert(0, line.split(':',
                                                             1)[1].strip())
                    elif line.startswith('Нижний предел:'):
                        self.entry_a.insert(0, line.split(':',
                                                          1)[1].strip())
                    elif line.startswith('Верхний предел:'):
                        self.entry_b.insert(0, line.split(':',
                                                          1)[1].strip())
                    elif line.startswith('Количество точек:'):
                        self.entry_n.insert(0, line.split(':',
                                                          1)[1].strip())

                # Проверка значений полей и вывод сообщения об успешной загрузке
                if (self.entry_func.get() and self.entry_a.get() and
                        self.entry_b.get() and self.entry_n.get()):
                    self.switch_frame(self.calculate_frame)
                    CTkMessagebox(title="Открыто",
                                  message="Файл успешно импортирован",
                                  width=300, height=200, icon="check")
                else:
                    CTkMessagebox(title="Ошибка",
                                  message="Некоторые поля были заполнены некорректно",
                                  width=300, height=200, icon="cancel")


if __name__ == "__main__":
    app = App()
    app.mainloop()
