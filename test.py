# main.py

import requests
import json
from datetime import datetime
import csv
import os
import time
from itertools import cycle
import random

# Импортируем только обновление таблицы (без пересоздания)
from table import update_table


tokens = [
    {"ua": "ru.hh.employer.android/3.155.1.367, Device: V2218A, Android OS: 9 (UUID: db268c3e-5dec-41b8-8743-fa1969c2ae72", 
            "token": "USERN5MDO4P5CN46K6HJ9GOBEVD7KT79L4RM3537A8G3M418KQK1JK304UCEQN0O"}, 
    {"ua": "ru.hh.employer.android/3.155.1.367, Device: PHB110, Android OS: 9 (UUID: 46b6adaf-5b7a-4454-b2fb-3ffd174afafc)", 
    "token": "USERSGHMVJMOBQVSLEQQH3IKQFFCOD9NJJ2UF9C6DE3V1V7C1D4CTNH6D25K41TT"},
    {"ua": "ru.hh.employer.android/3.155.1.367, Device: SM-S9260, Android OS: 9 (UUID: 360b9a8f-4761-4d4d-b6ce-1c1e205e4025)", 
    "token": "USERQ53OI5LHHUGN2DE5H8BLCP42KN9P2G65JTO78EMPR7J463JKR2AF16HGIUS2"},
    {"ua": "ru.hh.employer.android/3.155.1.367, Device: G576D, Android OS: 9 (UUID: 5d833372-930b-454d-b133-257c56096247)", 
    "token": "USERQHFMCB0ENPF22U9NCKG64SU375DM5BFD3PR4AM03V564NEBEKQLPOA1954Q8"},
    {"ua": "ru.hh.employer.android/3.155.1.367, Device: 2211133C, Android OS: 9 (UUID: 25b410c9-922f-4182-a3d4-c6f3887c8af6)", 
    "token": "USERSQG0TB1469F0A2IGG6KJE6HGT84OS6H88EE92G6LUTS1VA1F8D34EVLOIMOV"},
    {"ua": "ru.hh.employer.android/3.155.1.367, Device: 2203121C, Android OS: 9 (UUID: 785f0d65-bf5a-42e8-8a1b-9f43d08380af)", 
    "token": "USERV913ULCDF5EVTH3AGB5DF739HSCBLD1O5O8RNLDEROFC6BDBL51N5VDQVHRI"},
    {"ua": "ru.hh.employer.android/3.155.1.367, Device: 22127RK46C, Android OS: 9 (UUID: c331fc13-c9bf-4109-b551-10de24f60625)", 
    "token": "USERHNQ7595VIJE6CT5S43R484M01TQIRT2P4BJRU360NN24U7N0T2I3ICG0QTCF"},]
    


tokens_pool = cycle(tokens)
proxies = requests.get('https://api.npoint.io/0da6a4daf4342150a85b').json()['proxy'] # https://www.npoint.io/docs/0da6a4daf4342150a85b

proxy_pool = cycle(proxies)

def get_resume_info(resume_id):

    url = f"https://api.hh.ru/resumes/{resume_id.strip()}"
    data = next(tokens_pool)
    ua = data['ua']
    token = data['token']
    headers = {
        "Accept-Encoding": "gzip",
        "Connection": "Keep-Alive",
        "Authorization": f"Bearer {token}",
        "Host": "api.hh.ru",
        "User-Agent": ua,
        "x-hh-app-active": "true"
    }
    params = {
        "locale": "RU",
        "host": "hh.ru",
        "with_chat_info": "true",
        "with_job_search_status": "true",
        "with_creds": "true"
    }

    try:
        proxy = next(proxy_pool)
        response = requests.get(url, headers=headers, params=params, proxies={'http': proxy, 'https': proxy}, timeout=10)
        if response.status_code != 200:
            print(f"[Ошибка] Не удалось получить данные для {resume_id}: {response.status_code}")
            return resume_id, None, None, None

        data = response.json()
        # with open(f"resume_{resume_id}.json", "w", encoding="utf-8") as f:
        #     json.dump(data, f, ensure_ascii=False, indent=4)

        # Преобразуем даты
        last_seen = data['user_activity']['last_activity_at']
        updated_at_str = data['updated_at']
        status = data['job_search_status']['name']

        today_date = datetime.now().strftime("%d.%m.")  # Только дата, например 23.09

        # Проверяем, был ли сегодня (по last_activity_at)
        last_dt = datetime.strptime(last_seen, "%Y-%m-%dT%H:%M:%S%z")
        was_today =  last_dt.strftime("%d.%m.%Y")

        # Проверяем, обновлял ли резюме сегодня
        updated_dt = datetime.strptime(updated_at_str, "%Y-%m-%dT%H:%M:%S%z")
        updated_today = updated_dt.strftime("%d.%m.%Y")

        # Статус поиска работы
        current_status = status

        print(f"[OK] {resume_id} — был: {was_today}, обновил: {updated_today}, статус: {current_status}")
        return resume_id, was_today, updated_today, current_status

    except Exception as e:
        print(f"[Ошибка при обработке {resume_id}] {str(e)}")
        return resume_id, "нет", "нет", "Ошибка"


def read_resume_ids_from_csv(csv_file='data.csv'):
    """Читает ссылки и извлекает ID резюме"""
    resume_ids = []
    try:
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader, None)  # Пропускаем заголовок
            for row in reader:
                if len(row) > 0 and 'hh.ru/resume/' in row[0]:
                    url = row[0]
                    resume_id = url.split('/')[-1].split('?')[0]
                    resume_ids.append(resume_id)
    except Exception as e:
        print(f"[Ошибка чтения CSV] {e}")
    return resume_ids


def main():
    # ⚠️ Не конвертируем xlsx -> csv каждый раз!
    # Это перезапишет историю. Делай это ТОЛЬКО один раз вручную.
    
    ids = read_resume_ids_from_csv('data.csv')
    updates = {}
    with requests.Session() as session:
        for resume_id in ids:
            _, was, updated, status = get_resume_info(resume_id, session)
            updates[resume_id] = {
                'was': was,
                'updated': updated,
                'status': status
            }
            time.sleep(random.randint(7,12))  # Пауза между запросами


    # Теперь вызываем update_table с правильными данными
    update_table(updates)


if __name__ == "__main__":
    main()