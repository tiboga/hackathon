import matplotlib.pyplot as plt
import numpy as np

def generate_progress_charts(user_data, correct_color='green', incorrect_color='red', filename='user_progress_bar.png'):
    """
    Функция для генерации столбчатых графиков на основе данных о прогрессе пользователя и сохранения его в формате PNG.

    :param user_data: Словарь с данными о прогрессе пользователя.
                      Пример: {
                          'dates': ['2024-05-01', '2024-05-02', ...],
                          'correct': [10, 15, ...],
                          'incorrect': [2, 1, ...]
                      }
    :param correct_color: Цвет для правильных ответов.
    :param incorrect_color: Цвет для неправильных ответов.
    :param filename: Имя файла для сохранения графика.
    """
    dates = user_data['dates']
    correct = user_data['correct']
    incorrect = user_data['incorrect']

    # Преобразуем даты в формат numpy для оси X
    x = np.arange(len(dates))

    # Создаем фигуру и оси
    fig, ax = plt.subplots(figsize=(10, 5))

    # Устанавливаем черный фон для фигуры и осей
    fig.patch.set_facecolor('black')
    ax.set_facecolor('black')

    # Установка цвета для текста и линий
    ax.spines['bottom'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.title.set_color('white')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    ax.yaxis.label.set_color('white')
    ax.xaxis.label.set_color('white')

    # Ширина столбцов
    bar_width = 0.4

    # Построение столбчатого графика
    ax.bar(x - bar_width/2, correct, width=bar_width, color=correct_color, label='Правильные решения')
    ax.bar(x + bar_width/2, incorrect, width=bar_width, color=incorrect_color, label='Неправильные решения')

    # Добавляем заголовок и метки осей
    ax.set_title('Прогресс пользователя за период')
    ax.set_xlabel('Дата')
    ax.set_ylabel('Количество решений')

    # Устанавливаем метки на оси X
    ax.set_xticks(x)
    ax.set_xticklabels(dates, rotation=45, ha='right', color='white')

    # Отключаем сетку
    ax.grid(False)

    # Добавляем легенду с белым текстом
    legend = ax.legend()
    for text in legend.get_texts():
        text.set_color('white')

    # Сохраняем график в файл
    plt.tight_layout()
    plt.savefig(f'static/{filename}', facecolor=fig.get_facecolor())

    # Закрываем график чтобы избежать его отображения
    plt.close(fig)

    return filename

# # Пример данных
# user_data = {
#     'dates': ['2024-05-01', '2024-05-02', '2024-05-03', '2024-05-04', '2024-05-05'],
#     'correct': [10, 15, 20, 25, 30],
#     'incorrect': [2, 1, 3, 2, 1]
# }

# # Вызов функции для генерации графиков
# filename = generate_progress_charts(user_data, correct_color='green', incorrect_color='orange')
# print(f"График сохранен как {filename}")
