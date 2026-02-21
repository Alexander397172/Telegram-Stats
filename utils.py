import os
from typing import Dict
from datetime import datetime
import pandas as pd

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
        for line in f:
            parts = line.strip().rstrip(';').split(';')
            date = datetime.strptime(parts[0], '%Y-%m-%d').date()

            for item in parts[1:]:
                user_id, count = map(int, item.split(':'))
                username = user_names.get(user_id, f'User_{user_id}')
                records.append((date, username, count))

    return pd.DataFrame(records, columns=['date', 'user', 'count'])
