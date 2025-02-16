# Crypto Chart Generator 🚀

Генератор свечных графиков криптовалют для наложения на изображения. Проект позволяет создавать стильные графики с кастомизацией цветов, текста и сетки. Идеально подходит для визуализации финансовых данных в социальных сетях или аналитических материалах.



## Особенности ✨

- Генерация случайных или пользовательских свечных данных.
- Настройка цветов (бычьи/медвежьи свечи, фон, сетка).
- Добавление текстовых меток с обводкой.
- Поддержка форматов PNG/JPEG.
- Гибкие параметры: отступы, ширина свечей, шрифты.

## Установка ⚙️

1. Клонируйте репозиторий:
   
   git clone https://github.com/SunriseCat-Dev/crypto-chart-generator.git

2. Установите зависимости:
   pip install -r requirements.txt

## Использование 🛠️
    Минимальный пример:

        from Graph import CryptoChartGenerator

        chart = CryptoChartGenerator()
        result = chart.generate_chart("background.jpg")
        with open("chart.png", "wb") as f:
            f.write(result.getvalue())

    Расширенная настройка:

        chart = CryptoChartGenerator(
            padding=80,
            bull_color=(76, 175, 80),    # Зеленый для роста
            bear_color=(239, 83, 80),    # Красный для падения
            label_text="BTC/USDT",
            label_size=45,
            candle_width_ratio=0.7
        )

        custom_data = [
            (100, 120, 90, 110),  # Open, High, Low, Close
            (110, 130, 105, 125),
            # ... другие данные
        ]

        result = chart.generate_chart(
            base_image_path="background.jpg",
            data=custom_data,
            output_format="JPEG"
        )

Разработано с ❤️ SunriseCat_Dev |