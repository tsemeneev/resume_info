import json
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


client_id = 'QPTJSE7VM7L9GHB820SLU89GH9N335S5PUJBM91PA0K0NA57M9OHNM5BQV46P3U9'
client_secret = 'IUKG8MK8R8UMAMH4I026EE78PH5TR3R9CQBMSBLF9SETBNQJV8N1D97OE55R4SCI'
code = 'L1R58DL1BUIEEFV792I5ICSR03I4O52NSAIKNTU3PBLR27OUIL7KI6S6614H38RV'
redirect_uri = 'https://example.com/page'
# https://hh.ru/oauth/authorize?response_type=code&client_id=QPTJSE7VM7L9GHB820SLU89GH9N335S5PUJBM91PA0K0NA57M9OHNM5BQV46P3U9&redirect_uri=https://t.me/jobb_hunter_bot

resumes = ['5ed2327d0008efb9ed00bb7f2c423242323847', 'e9be711c0005b9c6d800bb7f2c50556d6b6849', '14f7ee30000853320300bb7f2c704743727a47',
'7b668c7f0002690a7c00bb7f2c335546764f49', '64aee1360007f0e63d00bb7f2c4f4e7a514165', '9a63188700045e2afc00bb7f2c6c715a773430',
'c419c8370004fa92a400bb7f2c657a52683163', 'a6623ca20004cd508100bb7f2c336e48627844', 'b94fa46c00071d691e00bb7f2c457958356267',
'c875454c0006e35fdc00bb7f2c47366d4e6c6a', '4c1a7a5e0005449d4000bb7f2c514159506751', '5c2461de00082cacc200bb7f2c4c304e674454',
'00e2e6af000083f48200bb7f2c736563726574', '27989f400003c6f73900bb7f2c5576557a5763', '5e19a85a000405079e00bb7f2c7a574b4c4767']


def get_hh_access_token():
    params = {
        'grant_type': 'authorization_code',
        'client_id': client_id,
        'client_secret': client_secret,
        'code': code, 
        'redirect_uri': redirect_uri
    }
    token = requests.post(url='https://hh.ru/oauth/token', data=params)
    with open('hh_token.json', 'w') as f:
        json.dump(token.json(), f, indent=2, ensure_ascii=False)




def get_hh_refresh_token():
        
    with open('hh_token.json', 'r') as token:
        refresh_token = json.load(token).get('refresh_token')
        
    params  = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        }
    res = requests.post('https://hh.ru/oauth/token', params=params, verify=False)
    if res.status_code == 200:
        with open('hh_token.json', 'w') as token:
            json.dump(res.json(), token, indent=2, ensure_ascii=False)
    
def post_token():
    url = 'https://api.npoint.io/fcb68f95136cb59c5d6b'
    with open('hh_token.json', 'r') as token:
        requests.post(url, json=json.load(token))
            

def get_resume(id):
    with open('hh_token.json', 'r') as token:
        headers = {'Authorization': f'Bearer {json.load(token).get("access_token")}'}
    url = f'https://api.hh.ru/resumes/{id}?with_job_search_status=true'
    web_url = f'https://togliatti.hh.ru/resume/{id}'
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        with open(f'resumes.json', 'w') as f:
            json.dump(res.json(), f, indent=2, ensure_ascii=False)
        print(res.json()['updated_at'])
        if res.json().get('job_search_status'):
            print(res.json().get('job_search_status').get('name'))
        else:
            print('Статус скрыт')
    else:
        print(res.text)
    

    # Открытие ссылки
    driver.get(web_url)
    intime = driver.find_element(By.CLASS_NAME, 'resume-online-status')
    print(intime.text)


chrome_options = Options()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--headless")

# Запуск браузера в режиме инкогнито
driver = webdriver.Chrome(options=chrome_options)

for id in resumes:
    get_resume(id)
    print('-----------------')
    time.sleep(1)