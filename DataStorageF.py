import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from scipy.interpolate import CubicSpline
import random
import pandas as pd

def fetch_stock_data(ticker, start_date, end_date, n_points):
    # Завантаження даних акцій
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    
    # Вибір рівновіддалених точок
    total_days = len(stock_data)
    indices = np.linspace(0, total_days - 1, n_points, dtype=int)
    sampled_data = stock_data.iloc[indices]
    
    # Підготовка вузлів для інтерполяції
    x_nodes = pd.to_datetime(sampled_data.index)  # Інтерполяційні вузли як дати
    y_nodes = sampled_data['Close'].values  # Ціни акцій на ці дні
    
    return x_nodes, y_nodes

def cubic_B_spline_interpolation(x_nodes, y_nodes, num_extra_points=500):
    # Перетворюємо дати на числові значення для сплайну
    x_numeric = (x_nodes - x_nodes[0]).days  # Переводимо дати у кількість днів від першої дати
    spline = CubicSpline(x_numeric, y_nodes, bc_type='natural')
    
    # Створюємо точки для побудови гладкого графіка сплайну
    x_extra = np.linspace(x_numeric[0], x_numeric[-1], num_extra_points)
    S = spline(x_extra)
    
    return x_extra, S, spline, x_numeric

def plot_spline(x_nodes, y_nodes, x_extra, S, spline, x_numeric):
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Основний графік
    ax.plot(x_extra, S, 'r-', linewidth=2, label='B-сплайн інтерполяція')
    ax.plot(x_numeric, y_nodes, 'bo', markersize=6, label='Вузли')
    
    # Формат осі y в доларах
    ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'${x:.2f}'))
    
    # Форматування осі x для відображення дат
    date_labels = x_nodes.strftime('%Y-%m-%d')
    ax.set_xticks(x_numeric[::len(x_numeric)//10])  # Відображаємо 10 рівновіддалених дат на осі x
    ax.set_xticklabels(date_labels[::len(date_labels)//10], rotation=45, ha="right")
    
    # Підпис осей
    ax.set_title('B-сплайн інтерполяція для цін акцій Apple')
    ax.set_xlabel('Дата')
    ax.set_ylabel('Ціна акцій (в доларах)')
    ax.legend()
    ax.grid()
    plt.show()

def calculate_error(x_nodes, y_nodes, spline, x_numeric):
    # Обчислення значень сплайну у вузлових точках
    y_interpolated = spline(x_numeric)
    
    # Обчислення абсолютної похибки
    errors = np.abs(y_nodes - y_interpolated)
    max_error = np.max(errors)
    mean_error = np.mean(errors)
    
    print(f"Максимальна похибка у вузлових точках: ${max_error:.10f}")
    print(f"Середня похибка у вузлових точках: ${mean_error:.10f}")
    
    # Вибір випадкової точки між вузлами для обчислення похибки
    random_index = random.randint(0, len(x_numeric) - 2)  # Вибираємо індекс, щоб мати проміжок між вузлами
    random_point = (x_numeric[random_index] + x_numeric[random_index + 1]) / 2  # Точка між двома вузлами
    random_interpolated = float(spline(random_point))  # Інтерпольоване значення у цій точці
    
    # Вибір фактичного значення як середнього між двома сусідніми вузлами
    random_actual = float((y_nodes[random_index] + y_nodes[random_index + 1]) / 2)
    random_error = abs(random_actual - random_interpolated)
    
    print(f"\nОбчислення похибки для довільної точки між вузлами:")
    print(f"Точка між {x_nodes[random_index].strftime('%Y-%m-%d')} і {x_nodes[random_index + 1].strftime('%Y-%m-%d')}")
    print(f"Фактичне значення (середнє сусідніх точок): ${random_actual:.10f}")
    print(f"Інтерпольоване значення: ${random_interpolated:.10f}")
    print(f"Похибка: ${random_error:.10f}")



# Параметри для інтерполяції
ticker = "AAPL"
start_date = "2019-04-01"
end_date = "2024-10-21"
n_points = int(input("Введіть кількість рівновіддалених точок для інтерполяції (наприклад, 100): "))

# Отримання даних і побудова інтерполяції
x_nodes, y_nodes = fetch_stock_data(ticker, start_date, end_date, n_points)
x_extra, S, spline, x_numeric = cubic_B_spline_interpolation(x_nodes, y_nodes)

# Обчислення похибки, включаючи випадкову дату
calculate_error(x_nodes, y_nodes, spline, x_numeric)

# Побудова графіка з датами на осі x та позначками у доларах на осі y
plot_spline(x_nodes, y_nodes, x_extra, S, spline, x_numeric)
