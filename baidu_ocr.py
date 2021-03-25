# encoding:utf-8
import requests
import base64

import config

conf = config.get_config()
client_id = conf['api_key']
client_secret = conf['secret_key']
access_token = get_token_from_baiduocr(client_id, client_secret)

f = open('test.jpg', 'rb')
img = base64.b64encode(f.read())


def get_token_from_baiduocr(client_id:str, client_secret:str) -> str:
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={}&client_secret={}'.format(client_id, client_secret)
    response = requests.get(host)
    if response:
        return response.json()['access_token']
    else:
        return None

def get_tag_from_baiduocr(image:bytes, access_token:str) -> map:
    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic"
    params = {"image":img}
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        return response.json()
    else:
        return None

print(get_tag_from_baiduocr(img, access_token))