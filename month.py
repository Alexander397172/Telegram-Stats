import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
from calendar import month_abbr
import os
from typing import Dict

def load_user_names(filename: str = 'names.txt') -> Dict[int, str]:
    user_names = {}
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                if ':' in line:
                    user_id, name = line.strip().split(':', 1)
                    user_names[int(user_id)] = name
    return user_names

def load_stats(filename: str = 'message_stats.txt') -> pd.DataFrame:
    if not os.path.exists(filename):
        raise FileNotFoundError(f"Файл '{filename}' не найден.")

    user_names = load_user_names()
    records = []

    with open(filename, 'r', encoding='utf-8') as f:
        current_date = None
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith('Дата:'):
                date_str = line.split(': ')[1]
                try:
                    current_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                except ValueError:
                    current_date = None
            elif current_date and ':' in line:
                try:
                    user_id_str, count_str = line.split(':', 1)
                    user_id = int(user_id_str.strip())
                    count = int(count_str.strip())
                    username = user_names.get(user_id, f'User_{user_id}')
                    records.append((current_date, username, count))
                except ValueError:
                    continue

    df = pd.DataFrame(records, columns=['date', 'user', 'count'])
    return df

def filter_by_month(df: pd.DataFrame, year: int, month: int) -> pd.DataFrame:
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    return df[(df['year'] == year) & (df['month'] == month)].copy()

def plot_monthly_stats(df: pd.DataFrame, year: int, month: int):
    if df.empty:
        print(f"Нет данных за {month_abbr[month]} {year} года")
        return

    daily_stats = df.pivot_table(index='date', columns='user', values='count', aggfunc='sum', fill_value=0)
    daily_stats = daily_stats.sort_index()

    plt.figure(figsize=(12, 6))
    colors = plt.cm.tab20.colors

    for i, user in enumerate(daily_stats.columns):
        plt.plot(daily_stats.index, daily_stats[user],
                 marker='o', linestyle='-', linewidth=2,
                 color=colors[i % len(colors)],
                 label=user)

    plt.title(f'Активность пользователей по дням ({month_abbr[month]} {year})', pad=20)
    plt.xlabel('Дата', labelpad=10)
    plt.ylabel('Количество сообщений', labelpad=10)
    plt.xticks(rotation=45)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(title='Пользователи', bbox_to_anchor=(1.05, 1), loc='upper left')

    for date in daily_stats.index:
        for user in daily_stats.columns:
            count = daily_stats.at[date, user]
            if count > 0:
                plt.text(date, count, str(count), ha='center', va='bottom', fontsize=9)

    plt.tight_layout()
    plt.show()

def choose_month(df: pd.DataFrame) -> (int, int):
    available_years_months = df['date'].dt.to_period('M').drop_duplicates().sort_values()
    available_periods = [f"{p.year}-{p.month:02}" for p in available_years_months]
    print("Доступные периоды данных:", ', '.join(available_periods))

    while True:
        try:
            year = int(input("Введите год для анализа: "))
            month = int(input("Введите номер месяца (1-12): "))
            if f"{year}-{month:02}" not in available_periods:
                print(f"Ошибка: нет данных за {month}/{year}")
                continue
            return year, month
        except ValueError:
            print("Ошибка: введите корректные числа")



try:
    df = load_stats()
    df['date'] = pd.to_datetime(df['date'])
    year, month = choose_month(df)
    month_df = filter_by_month(df, year, month)
    plot_monthly_stats(month_df, year, month)
except FileNotFoundError as e:
    print(e)
except Exception as e:
    print(f"Произошла ошибка: {e}")
