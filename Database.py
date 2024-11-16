import customtkinter as ctk
from openpyxl import load_workbook


class Database:
    def __init__(self, parent, fx, a, b, n):
        self.fn = 'materials/database.xlsx'
        self.wb = load_workbook(self.fn)
        self.ws = self.wb['Sheet1']
        self.new_window = None  # Окно истории
        self.parent = parent
        self.fx = fx
        self.a = a
        self.b = b
        self.n = n

    def load_history_data(self):

        # Чтение данных из Excel
        for i, row in enumerate(self.ws.iter_rows(min_row=2, max_row=self.ws.max_row)):
            if i < len(self.history_frames):  # Проверка, есть ли достаточно фреймов
                fx = row[0].value
                a = row[1].value
                b = row[2].value
                n = row[3].value

                # Обновление текста лейбла
                history_label, _ = self.history_frames[i]
                history_label.configure(text=f"f(x) = {fx}\na = {a}\nb = {b}\nn = {n}\n")

        self.wb.close()

    def history_window(self):
        if self.new_window:
            self.new_window.destroy()  # Закрываем предыдущее окно истории
        self.new_window = ctk.CTk()
        self.new_window.title("История вычислений")
        self.new_window.geometry("300x600")
        self.new_window.resizable(width=False, height=False)
        self.new_window.deiconify()

        self.history_frames = []

        # Создаем 5 фреймов
        for i in range(5):
            self.history_frame = ctk.CTkFrame(self.new_window, corner_radius=10, height=100, width=290)
            self.history_frame.grid(row=i, column=0, padx=5, pady=5)
            self.history_frame.grid_propagate(False)

            # Установим конфигурацию столбцов и строк внутри фрейма
            self.history_frame.grid_columnconfigure(0, weight=1)
            self.history_frame.grid_columnconfigure(1, weight=0)
            self.history_frame.grid_rowconfigure(0, weight=1)

            self.history_label = ctk.CTkLabel(self.history_frame, text="", font=("Arial Black", 12), wraplength=220,
                                              justify="left")
            self.history_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

            self.history_button = ctk.CTkButton(self.history_frame, text="Выбрать", font=("Arial Black", 12),
                                                command=lambda idx=i: self.fill_input_fields(idx),
                                                fg_color="#7d748e", hover_color="#545164", width=80)
            self.history_button.grid(row=0, column=1, padx=10, pady=10, sticky="e")

            self.history_frames.append((self.history_label, self.history_button))

        self.clear_history_button = ctk.CTkButton(self.new_window, text="Очистить историю", command=self.clear_history,
                                                  fg_color="#7d748e", hover_color="#545164", width=150)
        self.clear_history_button.grid(row=6, column=0, padx=10, pady=10, sticky="nsew")

        # Загружаем данные истории
        self.load_history_data()

    def clear_history(self):

        # Очищаем ячейки с данными истории
        for row in range(2, self.ws.max_row + 1):
            for col in range(1, 5):  # Очищаем столбцы A-D
                self.ws.cell(row=row, column=col).value = None

        # Сбрасываем счетчик
        self.ws['F2'].value = 2  # Сбрасываем счетчик на 2

        self.wb.save(self.fn)
        self.wb.close()

        # Обновляем отображение истории в окне
        self.load_history_data()  # Обновляем данные в фреймах

        # Сбрасываем текст лейбла в окне истории
        for history_label, _ in self.history_frames:
            history_label.configure(text="")

    def fill_input_fields(self, button_index):
        """Заполняет поля в calculate_frame данными из истории."""
        if button_index < len(self.history_frames):

            row = list(self.ws.iter_rows(min_row=button_index + 2, max_row=button_index + 2))

            if row:
                r = row[0]
                self.fx = r[0].value
                self.a = r[1].value
                self.b = r[2].value
                self.n = r[3].value

                # Заполняем поля в calculate_frame
                self.parent.entry_func.delete(0, 'end')
                self.parent.entry_func.insert(0, self.fx)
                self.parent.entry_a.delete(0, 'end')
                self.parent.entry_a.insert(0, self.a)
                self.parent.entry_b.delete(0, 'end')
                self.parent.entry_b.insert(0, self.b)
                self.parent.entry_n.delete(0, 'end')
                self.parent.entry_n.insert(0, self.n)

            self.wb.close()

    def update_history(self):
        # Добавляем счетчик строки
        row_counter_cell = self.ws['F2']  # Используем ячейку F2 для хранения текущего значения строки
        self.row_counter = row_counter_cell.value if row_counter_cell.value else 2

        # Устанавливаем значения в новую строку
        self.ws[f'A{self.row_counter}'] = self.fx
        self.ws[f'B{self.row_counter}'] = self.a
        self.ws[f'C{self.row_counter}'] = self.b
        self.ws[f'D{self.row_counter}'] = self.n

        # Увеличиваем счетчик
        self.row_counter += 1

        # Проверяем, не превышает ли счетчик 5
        if self.row_counter > 6:
            self.row_counter = 2

        # Сохраняем текущее значение row_counter в ячейке
        self.ws['F2'] = self.row_counter

        self.wb.save(self.fn)
        self.wb.close()
