import requests

def get_token_from_baiduocr(client_id:str, client_secret:str) -> str:
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={}&client_secret={}'.format(client_id, client_secret)
    response = requests.get(host)
    if response:
        return response.json()['access_token']
    else:
        return None

def get_tag_from_baiduocr(image:bytes, access_token:str) -> map:
    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic"
    params = {"image":image}
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        return response.json()['words_result']
    else:
        return None