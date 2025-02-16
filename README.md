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
