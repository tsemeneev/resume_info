# table.py

import pandas as pd
import datetime
import re


def update_table(updates_dict):
    file_path = 'data.csv'
    today = datetime.datetime.now().strftime("%d.%m.").strip('.')

    # Загружаем CSV
    try:
        df = pd.read_csv(file_path, on_bad_lines='skip')
    except FileNotFoundError:
        print(f"[Ошибка] Файл {file_path} не найден.")
        return

    base_columns = ['Ссылка', 'БЕ', 'Должность', 'ФИО', 'Телефон 1', 'Телефон 2']

    # Функция: определяет, является ли колонка датой
    def is_date_col(col):
        return bool(re.match(r'^\d{2}\.\d{2}\.?$', col.strip()))

    # Группируем существующие колонки по типам
    was_cols = [c for c in df.columns if 'Когда был_' in c or (c == 'Когда был' and not any('_' in x for x in df.columns))]
    updated_cols = [c for c in df.columns if 'Когда обновил_' in c or (c == 'Когда обновил' and not any('_' in x for x in df.columns))]
    status_cols = [c for c in df.columns if 'Текущий статус_' in c or (c == 'Текущий статус' and not any('_' in x for x in df.columns))]

    # Извлечение дат
    def extract_date(col):
        return col.split('_')[-1].strip('. ')

    existing_was_dates = [extract_date(c) for c in was_cols if '_' in c]
    existing_updated_dates = [extract_date(c) for c in updated_cols if '_' in c]
    existing_status_dates = [extract_date(c) for c in status_cols if '_' in c]

    # Добавляем сегодняшнюю дату, если её нет
    if today not in existing_was_dates:
        df[f'Когда был_{today}'] = ''
    if today not in existing_updated_dates:
        df[f'Когда обновил_{today}'] = ''
    if today not in existing_status_dates:
        df[f'Текущий статус_{today}'] = ''

    # Все уникальные даты (сортируем)
    all_dates = sorted(
        set(existing_was_dates + existing_updated_dates + existing_status_dates + [today]),
        key=lambda x: datetime.datetime.strptime(x + '.2025', '%d.%m.%Y')
    )

    # Формируем порядок колонок
    new_columns = base_columns.copy()
    for d in all_dates:
        new_columns.append(f'Когда был_{d}')
        new_columns.append(f'Когда обновил_{d}')
        new_columns.append(f'Текущий статус_{d}')

    # Переставляем
    df = df.reindex(columns=[col for col in new_columns if col in df.columns] +
                           [col for col in df.columns if col not in new_columns])

    # Заполняем данные по каждому кандидату
    for idx, row in df.iterrows():
        url = row['Ссылка']
        if not isinstance(url, str) or 'hh.ru/resume/' not in url:
            continue

        resume_id = url.split('/')[-1].split('?')[0]

        if resume_id in updates_dict:
            data = updates_dict[resume_id]
            df.at[idx, f'Когда был_{today}'] = data['was']
            df.at[idx, f'Когда обновил_{today}'] = data['updated']
            df.at[idx, f'Текущий статус_{today}'] = data['status']

    # Сохраняем
    df.to_csv(file_path, index=False)
    print(f"[OK] Таблица обновлена за {today}.")


df= pd.read_csv('data.csv', on_bad_lines='skip')
df.to_excel('data.xlsx', index=False)