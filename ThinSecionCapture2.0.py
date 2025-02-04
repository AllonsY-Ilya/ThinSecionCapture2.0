import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import math

class ImageApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Viewer")

        # Устанавливаем фиксированные размеры окна (60% от экрана)
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = int(screen_width * 0.6)
        window_height = int(screen_height * 0.6)
        self.root.geometry(f"{window_width}x{window_height}")
        self.root.minsize(1980, 1200)

        # Создаем фреймы
        self.left_frame = tk.Frame(self.root, width=window_width // 2)
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.right_frame = tk.Frame(self.root)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Холст для изображения
        self.canvas = tk.Canvas(self.left_frame, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Блок 1: Загрузка изображения, размер пикселя и обрезка
        self.block1_frame = tk.LabelFrame(self.right_frame, text="Управление изображением", padx=10, pady=10)
        self.block1_frame.pack(fill=tk.X, pady=5)

        # Ползунки для обрезки справа и снизу
        self.right_crop_scale_entry = tk.Label(self.block1_frame, text="Длина шлифа мм:")
        self.right_crop_scale_entry.pack()

        self.right_crop_scale = tk.Entry(self.block1_frame)
        self.right_crop_scale.pack()
        self.right_crop_scale.insert(0, "30")  # Установка значения по умолчанию
        self.right_crop_scale.bind("<KeyRelease>", self.update_crop)

        self.bottom_crop_scale_entry = tk.Label(self.block1_frame, text="Ширина шлифа мм:")
        self.bottom_crop_scale_entry.pack()

        self.bottom_crop_scale = tk.Entry(self.block1_frame)
        self.bottom_crop_scale.pack()
        self.bottom_crop_scale.insert(0, "35")  # Установка значения по умолчанию
        self.bottom_crop_scale.bind("<KeyRelease>", self.update_crop)

        # Кнопка загрузки
        self.load_button = tk.Button(self.block1_frame, text="Загрузить изображение", command=self.load_image)
        self.load_button.pack()

        # Блок 2: Рисование прямоугольника
        self.block2_frame = tk.LabelFrame(self.right_frame, text="Управление прямоугольником", padx=10, pady=10)
        self.block2_frame.pack(fill=tk.X, pady=5)

        # Ползунки для управления размерами прямоугольника
        self.rect_width_scale_entry = tk.Label(self.block2_frame, text="Ширина прямоугольника мм:")
        self.rect_width_scale_entry.pack()

        self.rect_width_scale = tk.Entry(self.block2_frame)
        self.rect_width_scale.pack()
        self.rect_width_scale.insert(0, "5")  # Установка значения по умолчанию
        self.rect_width_scale.bind("<KeyRelease>", self.update_rectangle)

        self.rect_height_scale_entry = tk.Label(self.block2_frame, text="Высота прямоугольника мм:")
        self.rect_height_scale_entry.pack()

        self.rect_height_scale = tk.Entry(self.block2_frame)
        self.rect_height_scale.pack()
        self.rect_height_scale.insert(0, "5")  # Установка значения по умолчанию
        self.rect_height_scale.bind("<KeyRelease>", self.update_rectangle)


        self.rect_rotation_scale = tk.Scale(self.block2_frame, from_=0, to=180, orient="horizontal",
                                            label="Поворот прямоугольника (°)", command=self.update_rotation)
        self.rect_rotation_scale.set(0)  # Устанавливаем начальный угол 0 градусов
        self.rect_rotation_scale.pack()



        # Кнопка для запоминания текущего размера прямоугольника и радиуса окружности
        self.save_shape_button = tk.Button(self.block2_frame, text="Запомнить размер прямоугольника и радиус",
                                           command=self.save_shape)
        self.save_shape_button.pack()

        # Чекбокс для рисования прямоугольника вокруг окружности
        self.draw_rect_around_circle_var = tk.BooleanVar()
        self.draw_rect_around_circle_checkbox = tk.Checkbutton(self.block2_frame,
                                                               text="Рисовать прямоугольник вокруг окружности",
                                                               variable=self.draw_rect_around_circle_var,
                                                               command=self.redraw_shapes)
        self.draw_rect_around_circle_checkbox.pack()

        # Ползунок для расстояния между центрами окружностей
        self.distance_scale = tk.Scale(self.block2_frame, from_=1, to=3, resolution = 0.02,
                                       orient="horizontal", label="Расстояние между центрами окружностей (мм)",
                                       command=self.update_distance)
        self.distance_scale.set(2)  # Устанавливаем начальное значение
        self.distance_scale.pack()

        self.kolichestvo = tk.Label(self.block2_frame, text="Количество съемок = ")
        self.kolichestvo.pack()

        self.cadr_amount_entry = tk.Label(self.block2_frame, text="Минимальный угол поворота столика (градусы)")
        self.cadr_amount_entry.pack()

        self.cadr_amount = tk.Entry(self.block2_frame)
        self.cadr_amount.pack()
        self.cadr_amount.insert(0, "1")  # Установка значения по умолчанию
        self.cadr_amount.bind("<KeyRelease>", self.update_time)

        self.time = tk.Label(self.block2_frame, text="Общее время съемки (мин) = :")
        self.time.pack()

        # Инициализация переменных
        self.image_path = None
        self.image = None
        self.img_tk = None
        self.image_resized = None
        self.image_width_mm = 0
        self.image_height_mm = 0
        self.rect_width = 0
        self.rect_height = 0
        self.rect_width_mm = 0
        self.rect_height_mm = 0
        self.saved_radius = None
        self.saved_rect_width = None
        self.saved_rect_height = None
        self.pixel_size = 1
        self.time_for720 = 12
        self.kolichestvo_video = None
        # Привязка событий
        self.root.bind("<Configure>", self.on_resize)

    def load_image(self):
        try:
            self.image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.png;*.jpeg;*.bmp;*.tiff")])
            if self.image_path:
                self.image = Image.open(self.image_path)
                self.image_width, self.image_height = self.image.size  # Устанавливаем размеры
                self.resize_image()  # Вызов метода для изменения размеров изображения
                self.calculate_sizes()  # Перерасчет размеров с учётом пикселя
        except Exception as e:
            print(f"Ошибка при загрузке изображения: {e}")

    def update_rotation(self, event=None):
        self.rect_rotation = self.rect_rotation_scale.get()  # Сохраняем угол из ползунка
        self.calculate_sizes()  # Обновляем размеры прямоугольника с новым углом

    def resize_image(self):
        if not self.image:
            return

        canvas_width = max(1, self.canvas.winfo_width())
        canvas_height = max(1, self.canvas.winfo_height())

        available_width = max(1, canvas_width - 80)
        available_height = max(1, canvas_height - 80)

        width_ratio = available_width / self.image_width
        height_ratio = available_height / self.image_height
        scale_ratio = max(min(width_ratio, height_ratio), 0.01)

        new_width = max(1, int(self.image_width * scale_ratio))
        new_height = max(1, int(self.image_height * scale_ratio))

        #right_crop = int((int(self.right_crop_scale.get()) / 100) * new_width)
        #bottom_crop = int((int(self.bottom_crop_scale.get()) / 100) * new_height)

        cropped_width = float(self.right_crop_scale.get())*33.3333
        cropped_height = float(self.bottom_crop_scale.get())*33.3333

        try:
            self.image_resized = self.image.resize((new_width, new_height), Image.Resampling.LANCZOS).crop(
                (0, 0, cropped_width, cropped_height))
            self.img_tk = ImageTk.PhotoImage(self.image_resized)
        except Exception as e:
            print(f"Ошибка при масштабировании: {e}")
            return

        self.canvas.delete("all")
        self.canvas.create_image(80, 40, anchor=tk.NW, image=self.img_tk)
        self.draw_arrows_and_sizes()
        self.draw_rectangle_and_circle()

    def draw_arrows_and_sizes(self):
        if not self.image_resized:
            return

        image_x = 80
        image_y = 40

        self.canvas.delete("arrow_top", "arrow_left", "text_top", "text_left")

        # Рисуем стрелку для ширины
        self.canvas.create_line(
            image_x, image_y - 20,
                     image_x + self.image_resized.width, image_y - 20,
            arrow=tk.BOTH, width=2, tags="arrow_top"
        )

        # Размеры изображения с учётом обрезки
        right_crop_percent = float(self.right_crop_scale.get()) / 100
        cropped_width = float(self.right_crop_scale.get())

        # Переводим размеры в миллиметры
        width_mm = cropped_width * float(self.pixel_size)

        self.canvas.create_text(
            image_x + self.image_resized.width // 2, image_y - 30,
            text=f"{width_mm:.2f} mm", font=("Arial", 12), tags="text_top"
        )

        # Рисуем стрелку для высоты
        self.canvas.create_line(
            image_x - 40, image_y,
            image_x - 40, image_y + self.image_resized.height,
            arrow=tk.BOTH, width=2, tags="arrow_left"
        )

        # Размеры изображения с учётом обрезки
        bottom_crop_percent = float(self.bottom_crop_scale.get()) / 100
        cropped_height = float(self.bottom_crop_scale.get())

        # Переводим размеры в миллиметры
        height_mm = cropped_height * float(self.pixel_size)

        self.canvas.create_text(
            image_x - 50, image_y + self.image_resized.height // 2,
            text=f"{height_mm:.2f} mm", font=("Arial", 12), tags="text_left", angle=90
        )

    def draw_rectangle_and_circle(self):
        if not self.image_resized:
            return

        image_x = 80
        image_y = 40

        # Удаляем старые элементы (прямоугольник и окружность)
        self.canvas.delete("rectangle", "circle")

        # Рисуем прямоугольник
        self.canvas.create_rectangle(
            image_x, image_y,
            image_x + self.rect_width, image_y + self.rect_height,
            outline="red", width=2, tags="rectangle"
        )

        # Находим центр прямоугольника
        rect_center_x = image_x + self.rect_width / 2
        rect_center_y = image_y + self.rect_height / 2

        # Диаметр окружности, выбираем минимальную сторону прямоугольника для диаметра
        circle_diameter = min(self.rect_width, self.rect_height)

        # Рисуем окружность в центре прямоугольника
        self.canvas.create_oval(
            rect_center_x - circle_diameter / 2,
            rect_center_y - circle_diameter / 2,
            rect_center_x + circle_diameter / 2,
            rect_center_y + circle_diameter / 2,
            outline="blue", width=2, tags="circle"
        )



    def calculate_sizes(self, event=None):
        try:
            # Получаем размер пикселя в миллиметрах
            pixel_size_mm = float(self.pixel_size)

            # Размеры изображения с учётом обрезки
            right_crop_percent = float(self.right_crop_scale.get()) / 100
            bottom_crop_percent = float(self.bottom_crop_scale.get()) / 100
            cropped_width = float(self.right_crop_scale.get())
            cropped_height = float(self.bottom_crop_scale.get())

            # Переводим размеры изображения в миллиметры
            self.image_width_mm = cropped_width * pixel_size_mm
            self.image_height_mm = cropped_height * pixel_size_mm

            # Рисуем стрелки для получения размеров
            self.draw_arrows_and_sizes()

            # Получаем размеры стрелок как ориентиры (они соответствуют доступным размерам изображения)
            arrow_width = self.image_resized.width  # ширина изображения после масштабирования
            arrow_height = self.image_resized.height  # высота изображения после масштабирования

            # Размеры прямоугольника в процентах от размеров изображения
            rect_width_percent = float(self.rect_width_scale.get()) / 100
            rect_height_percent = float(self.rect_height_scale.get()) / 100

            # Минимальный прямоугольник
            self.rect_width = max(5, 33.333 * float(self.rect_width_scale.get()))
            self.rect_height = max(5, 33.333 * float(self.rect_height_scale.get()))

            # Переводим размеры в миллиметры
            self.rect_width_mm = self.rect_width * pixel_size_mm
            self.rect_height_mm = self.rect_height * pixel_size_mm

            # Обновляем метки с размерами


            # Рисуем прямоугольник и окружность
            self.draw_rectangle_and_circle()

        except ValueError:
            pass

    def update_crop(self, event=None):
        self.resize_image()

    def update_rectangle(self, event=None):
        self.calculate_sizes()

    def save_shape(self):
        # Удаляем старые элементы (окружности и прямоугольники)
        self.canvas.delete("circle", "rectangle")

        # Сохраняем текущие размеры прямоугольника
        self.saved_rect_width = self.rect_width  # Ширина прямоугольника
        self.saved_rect_height = self.rect_height  # Высота прямоугольника

        # Определяем радиус окружности
        self.saved_radius = min(self.saved_rect_width, self.saved_rect_height) / 2

        # Координаты для рисования окружностей
        image_x = 80 + self.saved_radius # Координата X верхнего левого угла изображения
        image_y = 40 + self.saved_radius  # Координата Y верхнего левого угла изображения

        # Расчет актуальных размеров изображения
        right_crop_percent = float(self.right_crop_scale.get()) / 100
        cropped_width = float(self.right_crop_scale.get())*33.333

        bottom_crop_percent = float(self.bottom_crop_scale.get()) / 100
        cropped_height = float(self.bottom_crop_scale.get())*33.333

        # Максимальная координата для центра последней окружности
        max_center_x = cropped_width + self.saved_radius*1.25
        max_center_y = cropped_height + self.saved_radius*1.1



        distance_between_centers = self.distance_scale.get()

        # Общее количество окружностей, которые можно нарисовать
        max_circles_wigth = int(max_center_x / (distance_between_centers * self.saved_radius))
        max_circles_height = int(max_center_y / (distance_between_centers * self.saved_radius))


        self.kolichestvo_video = max_circles_height * max_circles_wigth
        self.update_time()

        # Координаты для рисования окружностей
        for i in range(max_circles_wigth):
            center_x = image_x + i * distance_between_centers * self.saved_radius

            if center_x > max_center_x:
                break

            # Рисуем окружность
            self.canvas.create_oval(
                center_x - self.saved_radius,
                image_y - self.saved_radius,
                center_x + self.saved_radius,
                image_y + self.saved_radius,
                outline="blue", width=2, tags="circle"
            )

        for i in range(max_circles_height):
            center_y = image_y + i * distance_between_centers * self.saved_radius

            if center_y > max_center_y:
                break

            # Рисуем окружность
            self.canvas.create_oval(
                image_x - self.saved_radius,
                center_y - self.saved_radius,
                image_x + self.saved_radius,
                center_y + self.saved_radius,
                outline="blue", width=2, tags="circle"
            )



        # Если галочка активирована, рисуем все прямоугольники вокруг окружностей
        if self.draw_rect_around_circle_var.get() and max_circles_wigth > 0:  # Если галочка активна
            self.draw_all_rectangles(image_x, image_y, max_circles_wigth, max_circles_height, max_center_x, max_center_y)



    def update_time(self, event=None):

        self.kolichestvo.config(text=f"Количество съемок = : {self.kolichestvo_video:.2f}")

        time =self.kolichestvo_video * self.time_for720 / int(self.cadr_amount.get())

        self.time.config(text=f"Общее время съемки (мин) = :{time:.2f}")


    def update_distance(self, event=None):
        # Вызываем метод save_shape для перерисовки с новыми параметрами
        self.save_shape()

    def draw_all_rectangles(self, image_x, image_y, max_circles_wigth, max_circles_height, max_center_x, max_center_y):
        self.canvas.delete("rectangle")
        distance_between_centers = self.distance_scale.get()

        #Прямоугольники для ширины
        angle_rad = math.radians(self.rect_rotation_scale.get())  # Преобразуем угол в радианы
        for i in range(max_circles_wigth):

            center_x = image_x + i * distance_between_centers * self.saved_radius  # Координаты центра окружности
            if center_x > max_center_x:
                break


            # Рассчитываем координаты углов прямоугольника
            rect_points = [
                (center_x - self.saved_rect_width / 2, image_y - self.saved_rect_height / 2),  # Верхний левый угол
                (center_x + self.saved_rect_width / 2, image_y - self.saved_rect_height / 2),  # Верхний правый угол
                (center_x + self.saved_rect_width / 2, image_y + self.saved_rect_height / 2),  # Нижний правый угол
                (center_x - self.saved_rect_width / 2, image_y + self.saved_rect_height / 2),  # Нижний левый угол
            ]

            # Функция для поворота точки относительно центра
            def rotate_point(x, y, angle):
                new_x = center_x + (x - center_x) * math.cos(angle) - (y - image_y) * math.sin(angle)
                new_y = image_y + (x - center_x) * math.sin(angle) + (y - image_y) * math.cos(angle)
                return new_x, new_y

            # Получаем новые координаты углов после поворота
            rotated_points = [rotate_point(x, y, angle_rad) for x, y in rect_points]

            # Рисуем прямоугольник
            self.canvas.create_polygon(
                rotated_points[0][0], rotated_points[0][1],
                rotated_points[1][0], rotated_points[1][1],
                rotated_points[2][0], rotated_points[2][1],
                rotated_points[3][0], rotated_points[3][1],
                outline="green", fill="", width=2, tags="rectangle"
            )

            # Прямоугольники для длины
            for j in range(max_circles_height):

                center_y = image_y + j * distance_between_centers * self.saved_radius  # Координаты центра окружности

                if center_y > max_center_y:
                    break
                # Рассчитываем координаты углов прямоугольника
                rect_points = [
                    (image_x - self.saved_rect_width / 2, center_y - self.saved_rect_height / 2),  # Верхний левый угол
                    (image_x + self.saved_rect_width / 2, center_y - self.saved_rect_height / 2),  # Верхний правый угол
                    (image_x + self.saved_rect_width / 2, center_y + self.saved_rect_height / 2),  # Нижний правый угол
                    (image_x - self.saved_rect_width / 2, center_y + self.saved_rect_height / 2),  # Нижний левый угол
                ]

                # Функция для поворота точки относительно центра
                def rotate_point(x, y, angle):
                    new_x = image_x + (x - image_x) * math.cos(angle) - (y - center_y) * math.sin(angle)
                    new_y = center_y + (x - image_x) * math.sin(angle) + (y - center_y) * math.cos(angle)
                    return new_x, new_y

                # Получаем новые координаты углов после поворота
                rotated_points = [rotate_point(x, y, angle_rad) for x, y in rect_points]

                # Рисуем прямоугольник
                self.canvas.create_polygon(
                    rotated_points[0][0], rotated_points[0][1],
                    rotated_points[1][0], rotated_points[1][1],
                    rotated_points[2][0], rotated_points[2][1],
                    rotated_points[3][0], rotated_points[3][1],
                    outline="green", fill="", width=2, tags="rectangle"
                )



    def update_rotation(self, event=None):
        # Обновляем все прямоугольники на основе текущего угла
        if self.draw_rect_around_circle_var.get():
            self.save_shape()

    def redraw_shapes(self):
        # Перерисовываем прямоугольник вокруг окружности, если галочка установлена
        self.save_shape()

    def on_resize(self, event):
        # Перерасчет размеров при изменении размера окна
        self.resize_image()


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageApp(root)
    root.mainloop()