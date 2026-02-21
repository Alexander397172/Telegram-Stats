import matplotlib.pyplot as plt
import pandas as pd
from calendar import month_abbr
from utils import load_stats, load_user_names

def aggregate_by_month(df: pd.DataFrame, year: int) -> pd.DataFrame:
    df_year = df[df['date'].dt.year == year]
    df_year['month'] = df_year['date'].dt.month
    monthly_stats = df_year.groupby(['month', 'user'])['count'].sum().unstack(fill_value=0)
    return monthly_stats

def plot_yearly_stats(monthly_stats: pd.DataFrame, year: int):
    if monthly_stats.empty:
        print(f"Нет данных за {year} год")
        return

    plt.figure(figsize=(12, 6))
    colors = plt.cm.tab20.colors
    for i, user in enumerate(monthly_stats.columns):
        plt.plot(monthly_stats.index, monthly_stats[user],
                 marker='o', linestyle='-', linewidth=2,
                 color=colors[i % len(colors)],
                 label=user)

    plt.xticks(monthly_stats.index, [month_abbr[m] for m in monthly_stats.index])
    plt.title(f'Активность пользователей по месяцам ({year} год)', pad=20)
    plt.xlabel('Месяц', labelpad=10)
    plt.ylabel('Количество сообщений', labelpad=10)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(title='Пользователи', bbox_to_anchor=(1.05, 1), loc='upper left')

    for month in monthly_stats.index:
        for user in monthly_stats.columns:
            count = monthly_stats.at[month, user]
            if count > 0:
                plt.text(month, count, str(count), ha='center', va='bottom', fontsize=9)

    plt.tight_layout()
    plt.show()

def choose_year(df: pd.DataFrame) -> int:
    available_years = sorted(df['date'].dt.year.unique())
    print("Доступные годы данных:", ', '.join(map(str, available_years)))
    while True:
        try:
            year = int(input("Введите год для анализа: "))
            if year not in available_years:
                print(f"Ошибка: нет данных за {year} год")
                continue
            return year
        except ValueError:
            print("Ошибка: введите корректный год")

try:
    df = load_stats()
    df['date'] = pd.to_datetime(df['date'])
    year = choose_year(df)
    monthly_stats = aggregate_by_month(df, year)
    plot_yearly_stats(monthly_stats, year)
except FileNotFoundError as e:
    print(e)
except Exception as e:
    print(f"Произошла ошибка: {e}")
