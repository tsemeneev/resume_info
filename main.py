import json
import requests


client_id = 'QVH7QSCQNJBOFILTOT44JRE8QV6JOJFH9RLRUKQQA7SH6NUNCEEJ56G347JP7I0E'
client_secret = 'UGOHAUDCL4N66JQDKER1675EBJID3TJ0P4UCG7E0MC3ODL1CULA8KUHJM551K9QK'
code = 'OH5QUIPGAQTSAOAFN8MB2PQ4HML96I2MJRUSTVILS36215KQ2VPH930O0UNP200R'
redirect_uri = 'https://t.me/jobb_hunter_bot'
# https://hh.ru/oauth/authorize?response_type=code&client_id=QVH7QSCQNJBOFILTOT44JRE8QV6JOJFH9RLRUKQQA7SH6NUNCEEJ56G347JP7I0E&redirect_uri=https://t.me/jobb_hunter_bot

hh_employer_ids = [
        4986, 1140385, 92288, 1182859, 1413754, 9521594, 5717529, 3670351, 844660, 189053, 4987434, 3914672, 925811, 1788157, 
        1015533, 1031898, 4256239, 5526776, 240334, 218226, 3038085, 3402888, 2483069, 1436642, 4914451, 4845258,
        2886021, 5496195, 9886038, 6157984, 5420519, 1861895, 3315991, 5019303, 8882, 6166603, 4264826, 6036006, 5911909, 
        9934668, 3546356, 2898779, 4588196, 5363651, 5272164, 3218558, 4500860, 3334479, 3758678, 1822991, 989471, 6059022, 2758407, 
        1053183, 3915256, 4749449, 4601859, 3166005, 4206534, 1538921, 3932242, 699072, 2402339, 174, 97839,
        1690451, 2389464, 1738660, 1021597, 730482, 882293, 1967342
]


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
            

def get_resume():
    with open('hh_token.json', 'r') as token:
        token = json.load(token).get('access_token')

    
    headers = {
        "Authorization": f"Bearer {token}",
    }
    url = f'https://api.hh.ru/resumes/8f52aa5400043f8471000022b26c6b4867686f?with_job_search_status=true&with_creds=true'
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        with open(f'resumes.json', 'w') as f:
            json.dump(res.json(), f, indent=2, ensure_ascii=False)
    else:
        print(res.text)

get_resume()