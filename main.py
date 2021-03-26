import base64
import prettytable
from prettytable import ALL as ALL

import devices
import baidu_ocr
import config
import db
import itertools

def get_raw_img() -> bytes:
    devices_no = devices.get_devices_no()
    current_device = devices.devices(devices_no)
    current_img = current_device.get_screenshot()
    f = open('./img/{}.png'.format(current_img), 'rb')
    img = base64.b64encode(f.read())
    return img

def tag_format(tags: tuple) -> str:
    res = ""
    for i in tags:
        res = res + i + " "
    return res.strip()

def role_sort(attr: tuple) -> int:
    return attr[1]

def result_format(res: map):
    for item in res:
        if(res[item][0][1] > 3):
            print("\033[1;35m {} \033[0m".format(item), end="\t")
        else:
            print("\033[1;38m {} \033[0m".format(item), end="\t")
        for role in res[item]:
            if role[1] == 0:
                print("\033[38m {} \033[0m".format(role[0]), end="")
            if role[1] == 1:
                print("\033[32m {} \033[0m".format(role[0]), end="")
            if role[1] == 2:
                print("\033[34m {} \033[0m".format(role[0]), end="")
            if role[1] == 3:
                print("\033[32m {} \033[0m".format(role[0]), end="")
            if role[1] == 4:
                print("\033[31m {} \033[0m".format(role[0]), end="")
            if role[1] == 5:
                print("\033[1;34;43m {} \033[0m".format(role[0]), end="")
        print()

def role_format(roles: list) -> str:
    current_len = 0
    res = ""
    for role in roles:
        res = res + role[0] + " "
        current_len = current_len + len(role[0]) + 1
        if current_len > 20:
            res = res + "\n"
            current_len = 0
    res = res.strip()
    if(res[1] == '\n'):
        res = res[0:-1]
    return res

def result_table(res: map):
    x = prettytable.PrettyTable(hrules=ALL)
    x.field_names = ["职业需求", "干员", "最低品质", "最高品质"]
    x.align["干员"] = 'l'
    x.align["职业需求"] = 'l'
    for item in res:
        x.add_row([item, role_format(res[item]), res[item][0][1] + 1, res[item][-1][1] + 1])
    print(x.get_string(sortby="最低品质"))

conf = config.get_config()
access_token = baidu_ocr.get_token_from_baiduocr(conf['api_key'], conf['secret_key'])
candidates = baidu_ocr.get_tag_from_baiduocr(get_raw_img(), access_token)

tags = []
for item in candidates:
    if item['words'] in db.tags:
        tags.append(item['words'])

high_level = False
if "高级资深" in tags:
    high_level = True
result = {}
for i in range(1, 4):
    for item in itertools.combinations(tags, i):
        for role in db.recruit_database:
            if set(item) <= set(role[2]):
                current_tag = tag_format(item)
                if current_tag not in result:
                    result[current_tag] = []
                if role[1] == 5 and not high_level:
                    continue
                result[current_tag].append(role)

for item in result:
    result[item] = sorted(result[item], key = role_sort)

result_table(result)