from PIL import Image, ImageDraw, ImageFont
import io
import random
from typing import List, Tuple, Optional

# Made by SunriseCat_Dev
# Ver 0.1
# Link: 


class CryptoChartGenerator:
    """
    Класс для генерации свечных графиков криптовалют поверх изображений

    Attributes:
        background_color (tuple): Цвет фона графика (RGBA)
        bull_color (tuple): Цвет бычьих свечей (RGB)
        bear_color (tuple): Цвет медвежьих свечей (RGB)
        padding (int): Отступы от краев изображения
        candle_width_ratio (float): Ширина свечи относительно доступного пространства
        label_font (str): Путь к файлу шрифта
        label_size (int): Размер текста
        label_color (tuple): Цвет текста (RGBA)
    """

    def __init__(self,
                 bull_color: Tuple[int, int, int] = (76, 175, 80),
                 bear_color: Tuple[int, int, int] = (239, 83, 80),
                 padding: int = 60,
                 candle_width_ratio: float = 0.7,
                 label_text: str = 'MCAP',
                 label_font: str = 'arial.ttf',
                 label_size: int = 60,
                 label_color: Tuple[int, int, int, int] = (255, 255, 255, 200)):

        self.bull_color = bull_color
        self.bear_color = bear_color
        self.padding = padding
        self.candle_width_ratio = candle_width_ratio
        self.chart_background = (25, 25, 50, 125)
        self.grid_color = (255, 255, 255, 64)
        self.wick_width = 5

        # Параметры текста
        self.label_text = label_text
        self.label_font = label_font
        self.label_size = label_size
        self.label_color = label_color

    @staticmethod
    def generate_candle_data(data_points: int = 20) -> List[Tuple[float, float, float, float]]:
        """
        Генерирует случайные свечные данные

        Args:
            data_points: Количество свечей

        Returns:
            Список кортежей (Open, High, Low, Close)
        """
        data = []
        last_close = random.uniform(80, 120)

        for _ in range(data_points):
            open_price = last_close
            close = open_price + random.uniform(-20, 20)
            high = max(open_price, close) + random.uniform(5, 15)
            low = min(open_price, close) - random.uniform(5, 15)
            data.append((open_price, high, low, close))
            last_close = close

        return data

    def _calculate_metrics(self, data: List[Tuple[float, float, float, float]],
                           img_width: int,
                           img_height: int) -> tuple:
        """Вычисляет масштабы и границы графика"""
        min_val = min(d[2] for d in data)
        max_val = max(d[1] for d in data)

        if max_val <= min_val:
            max_val = min_val + 1e-5

        chart_width = img_width - 2 * self.padding
        chart_height = img_height - 2 * self.padding
        y_scale = chart_height / (max_val - min_val)

        return min_val, max_val, chart_width, chart_height, y_scale

    def generate_chart(self,
                       base_image_path: str,
                       data: Optional[List[Tuple[float, float, float, float]]] = None,
                       data_points: int = 20,
                       output_format: str = 'PNG') -> io.BytesIO:
        """
        Генерирует изображение с графиком

        Args:
            base_image_path: Путь к фоновому изображению
            data: Пользовательские свечные данные
            data_points: Количество свечей если данные не предоставлены
            output_format: Формат выходного изображения

        Returns:
            BytesIO объект с результатом
        """
        # Загрузка изображения
        img = Image.open(base_image_path).convert('RGBA')
        width, height = img.size

        # Генерация или использование готовых данных
        data = data or self.generate_candle_data(data_points)
        min_val, max_val, chart_width, chart_height, y_scale = self._calculate_metrics(data, width, height)

        # Создание слоев
        overlay = Image.new('RGBA', img.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(overlay)

        # Отрисовка элементов
        self._draw_chart_background(draw, width, height)
        self._draw_grid(draw, width, height, chart_height)
        self._draw_candles(draw, data, min_val, chart_width, height, y_scale)
        self._draw_labels(draw)  # Добавлен вызов отрисовки текста

        # Финализация
        img = Image.alpha_composite(img, overlay).convert('RGB')
        return self._save_to_bytesio(img, output_format)

    def _draw_chart_background(self, draw: ImageDraw.Draw, width: int, height: int):
        """Рисует фон графика"""
        draw.rounded_rectangle(
            [(self.padding-10, self.padding-10),
             (width-self.padding+10, height-self.padding+10)],
            radius=20,
            fill=self.chart_background,
            outline=self.grid_color,
            width=3
        )

    def _draw_grid(self, draw: ImageDraw.Draw, width: int, height: int, chart_height: int):
        """Рисует сетку"""
        for i in range(5):
            y = height - self.padding - i * (chart_height / 4)
            opacity = 25 + i * 30
            draw.line(
                [(self.padding, y), (width - self.padding, y)],
                fill=(255, 255, 255, opacity),
                width=1 + i // 3
            )

    def _draw_candles(self,
                      draw: ImageDraw.Draw,
                      data: List[Tuple[float, float, float, float]],
                      min_val: float,
                      chart_width: int,
                      height: int,
                      y_scale: float):
        """Рисует свечи"""
        candle_width = chart_width / len(data) * self.candle_width_ratio

        for idx, (o, h, l, c) in enumerate(data):
            x_center = self.padding + (idx + 0.5) * (chart_width / len(data))
            color = self.bull_color if c >= o else self.bear_color

            # Фитиль
            y_high = height - self.padding - (h - min_val) * y_scale
            y_low = height - self.padding - (l - min_val) * y_scale
            draw.line([(x_center, y_high), (x_center, y_low)], fill=color, width=self.wick_width)

            # Тело свечи
            y_open = height - self.padding - (o - min_val) * y_scale
            y_close = height - self.padding - (c - min_val) * y_scale
            body_top = min(y_open, y_close)
            body_height = abs(y_open - y_close) or 1

            draw.rounded_rectangle(
                [
                    (x_center - candle_width/2, body_top),
                    (x_center + candle_width/2, body_top + body_height)
                ],
                radius=1,
                fill=color,
                outline=(255, 255, 255, 50),
                width=1
            )

    def _draw_labels(self, draw: ImageDraw.Draw):
        """Рисует текстовые метки на графике

        Args:
            draw: ImageDraw.Draw объект для рисования
            text: Текст метки
            font: Шрифт метки
            position: Позиция метки
        Returns:
            Текст на картинке
        """

        try:
            font = ImageFont.truetype(self.label_font, self.label_size)
        except:
            font = ImageFont.load_default()

        text = self.label_text
        position = (self.padding + 15, self.padding + 10)  # Позиция в левом верхнем углу

        # Рисуем текст с обводкой
        draw.text(
            position,
            text,
            fill=self.label_color,
            font=font,
            stroke_width=5,
            stroke_fill=(0, 0, 0, 128)
        )

    @staticmethod
    def _save_to_bytesio(img: Image.Image, output_format: str) -> io.BytesIO:
        """Сохранение в BytesIO"""
        img_io = io.BytesIO()
        img.save(img_io, format=output_format, quality=95, optimize=True)
        img_io.seek(0)
        return img_io


# Пример использования
if __name__ == "__main__":
    # Инициализация генератора
    chart_generator = CryptoChartGenerator(
        padding=70,
        candle_width_ratio=0.6,
        bull_color=(100, 200, 100),
        bear_color=(200, 100, 100),
        label_text='MCAP 1kkkk$',
        label_font='arial.ttf',
        label_size=60,
        label_color=(200, 220, 255, 255)
    )

    # Генерация данных и создание графика
    custom_data = CryptoChartGenerator.generate_candle_data(20)
    result = chart_generator.generate_chart(
        'result.jpg',
        data=custom_data,
        output_format='JPEG'
    )

    # Сохранение результата
    with open('crypto_chart.jpg', 'wb') as f:
        f.write(result.getvalue())
