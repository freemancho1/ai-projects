import os
import requests

_KEY_FILE_PATH = os.path.join(os.path.expanduser('~'), 'projects', 'naver_application_key.txt')
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


if __name__ == '__main__':
    address = '전남 나주시 중야1길 15'
    print(get_geocoding(address))