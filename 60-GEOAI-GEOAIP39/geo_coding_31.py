import os
import requests

_KEY_FILE_PATH = os.path.join(
    os.path.expanduser('~'), 
    'projects' if os.name == 'posix' else 'python_projects', 
    'naver_application_key.txt'
)
_API_URL = 'https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode'

def _get_request_header():
    with open(_KEY_FILE_PATH, 'r') as key_file:
        lines = key_file.readlines()
    api_id = lines[0].replace('\n', '')
    api_secret = lines[1].replace('\n', '')
    
    return {
        "X-NCP-APIGW-API-KEY-ID": api_id,
        "X-NCP-APIGW-API-KEY": api_secret,
    }
    
REQUEST_HEADER = _get_request_header()
    
def get_geocoding(address_name):
    req_uri = f'{_API_URL}?query={address_name}'
    response = requests.get(req_uri, headers=REQUEST_HEADER)
    return response.json() if response.status_code == 200 else {'status': 'error'}

def get_optimal_path(start, end):
    optimal_api_url = \
        f'https://naveropenapi.apigw.ntruss.com/map-direction/v1/driving?' \
        f'start={start[1]},{start[0]}&goal={end[1]},{end[0]}' \
        f'&option=trafast:tracomfort:traoptimal&format=json'
        #  실시간  빠른길  편한길      최적
    print(f'{optimal_api_url}')
    response = requests.get(optimal_api_url, headers=REQUEST_HEADER)
    return response.json() if response.status_code == 200 else {'status': 'error'}


if __name__ == '__main__':
    address = '전남 나주시 중야1길 15'
    print(get_geocoding(address))