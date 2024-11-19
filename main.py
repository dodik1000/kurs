import customtkinter as ctk
from PIL import Image
from Equation import Equation
from Database import Database


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        '''------------------- НАСТРОЙКА ОКНА -------------------'''

        self.title("Калькулятор")
        self.geometry("900x700")
        self.resizable(width=False, height=False)

        # region: Конфигурация окна
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # endregion

        # Инициализация таймера бездействия
        self.idle_timer = None

        # Инициализация переменной для удаления окна
        self.new_window_deleter = None

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
        # endregion

        # Текущий фрейм
        self.current_frame = self.main_frame

        '''------------------- SIDEBAR FRAME -------------------'''

        # Размещение фрейма
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
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
        self.about_programm_button = (ctk.CTkButton
                                      (self.sidebar_frame, text="О программе",
                                       fg_color="#7d748e", hover_color="#545164",
                                       command=lambda:
                                       self.switch_frame(self.about_program_frame),
                                       width=147, height=30))
        self.about_programm_button.grid(row=3, column=0, padx=20, pady=(10, 0))

        # Кнопка "История вычислений"
        self.recent_button = ctk.CTkButton(self.sidebar_frame,
                                           text="История вычислений",
                                           fg_color="#7d748e", hover_color="#545164",
                                           command=self.execute_funcs_history,
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

        self.appearance_mode_optionemenu = (
            ctk.CTkOptionMenu(self.sidebar_frame, values=["Светлая", "Темная"],
                              command=self.change_theme, fg_color="#7d748e",
                              button_color="#7d748e", button_hover_color="#545164"))
        self.appearance_mode_optionemenu.grid(row=7, column=0, padx=20, pady=(10, 30))
        # endregion

        '''------------------- MAIN FRAME -------------------'''

        # Размещение главного фрейма
        self.main_frame.grid(row=0, column=1, rowspan=4, sticky="nsew")

        # Установка темной темы по умолчанию
        ctk.set_appearance_mode("Dark")
        self.appearance_mode_optionemenu.set("Темная")

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
        self.label_kurs = ctk.CTkLabel(self.main_frame, text="Курсовой проект",
                                       font=("Arial Black", 24))
        self.label_kurs.grid()
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
        self.image = Image.open("materials/integralcalculator.png")
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

        #################################################################
        # region: CALCULATE FRAME

        self.func_label = (
            ctk.CTkLabel(self.calculate_frame,
                         text="Функция (используйте 'x' как переменную):",
                         font=('Arial Black', 14)))
        self.func_label.grid(row=0, column=0, padx=20, pady=20, sticky="w")

        self.entry_func = ctk.CTkEntry(self.calculate_frame, width=300,
                                       font=('Arial Black', 14))
        self.entry_func.grid(row=0, column=1, columnspan=2, padx=10, pady=20,
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
                                 command=self.execute_functions)
        self.but.grid(row=4, column=0, columnspan=3, padx=10, pady=20, sticky="ew")

        # endregion

        #################################################################
        # region: ABOUT AUTHOR FRAME

        self.auth_label1 = ctk.CTkLabel(self.about_author_frame,
                                        text="Автор\n\nСтудент группы 10701123"
                                        "\n\nМакаров Артём Сергеевич"
                                        "\n\nartemmakarovv05@gmail.com",
                                        font=("Arial Black", 20))
        self.auth_label1.grid(row=0, column=1, padx=200, pady=(70, 15), sticky="nsew")

        self.image2 = Image.open("materials/bntu.png")
        self.ctk_image2 = ctk.CTkImage(light_image=self.image2, size=(200, 200))
        self.label_image2 = ctk.CTkLabel(self.about_author_frame,
                                         image=self.ctk_image2, text="")
        self.label_image2.grid(row=1, column=1, padx=10,  sticky="nsew")

        # endregion

        #################################################################
        # region: ABOUT PROGRAM FRAME

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
                         font=("Arial Black", 12), wraplength=700, justify="left"))
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

    def change_theme(self, theme):
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

    def switch_frame(self, new_frame):
        self.current_frame.grid_forget()
        new_frame.grid(row=0, column=1, rowspan=4, sticky="nsew")
        self.current_frame = new_frame

    def close_program(self):
        if self.new_window_deleter is not None:
            self.new_window_deleter.destroy()
        if hasattr(self, 'idle_timer_id'):
            self.after_cancel(self.idle_timer_id)
        if hasattr(self, 'close_timer_id'):
            self.after_cancel(self.close_timer_id)
        if hasattr(self, 'update_countdown_id'):
            self.after_cancel(self.update_countdown_id)
        self.destroy()

    def execute_functions(self):  # Функция-обертка
        self.eq = Equation(self.calculate_frame, self, self.entry_func.get(),
                           self.entry_a.get(), self.entry_b.get(), self.entry_n.get())
        self.eq.simpson()

        self.db = Database(self, self.entry_func.get(), self.entry_a.get(),
                           self.entry_b.get(), self.entry_n.get())
        self.reset_idle_timer()
        self.db.update_history()
        self.db = None

    def execute_funcs_history(self):
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

    def reset_idle_timer(self):
        """Сбрасывает таймер бездействия."""
        if hasattr(self, 'idle_timer_id'):
            self.after_cancel(self.idle_timer_id)
        self.idle_timer_id = self.after(60000, self.show_idle_warning)

    def continue_session(self):
        self.warning_window.destroy()
        self.reset_idle_timer()
        if hasattr(self, 'close_timer_id'):
            self.after_cancel(self.close_timer_id)
        if hasattr(self, 'update_countdown_id'):
            self.after_cancel(self.update_countdown_id)

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


if __name__ == "__main__":
    app = App()
    app.mainloop()
