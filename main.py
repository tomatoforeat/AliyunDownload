import requests
import json
import time
from Aria2_RPC import Aria2Download

headers = {
    "Accept": "application/json, text/plain, */*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    "Content-Type": "application/json;charset=UTF-8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9"

}

def get_file_list(path):
    file_list = []
    data_list = {"path": path, "page": 1, "per_page": 0, "refresh": False}
    error_count = 0
    while True:
        req = requests.post(url=url_list, data=json.dumps(data_list), headers=headers, timeout=15)
        if req.status_code == 200:
            content = req.json()["data"]["content"]
            break
        else:
            error_count += 1
            time.sleep(1)
            if error_count >= 3:
                content = []
                break

    for item in content:
        if item["is_dir"]:
            sub_dir = path + "/" + item["name"]
            file_list.extend(get_file_list(sub_dir))
        else:
            file_info = {"name" : item["name"], "size" : item["size"], "path" : path, "sign" : item["sign"]}
            file_list.append(file_info)

    return file_list

url_login = 'http://192.168.0.201:5244/api/auth/login'
data = {"Username": 'admin', "Password": "123456"}
req = requests.post(url=url_login, data=json.dumps(data), headers=headers)
token = req.json()['data']['token']
headers["Authorization"] = token

url_list = 'http://192.168.0.201:5244/api/fs/list'

path = '/阿里云盘/超级宝贝JOJO'
file_list = get_file_list(path)
aria2 = Aria2Download("http://192.168.0.201:6800/jsonrpc")

for file in file_list:
    download_url = "http://192.168.0.201:5244" + "/d" + file["path"] + "/" + file["name"] + "?sign=" + file["sign"]
    save_path = "/downloads/aliyun/" + file["path"]
    print(aria2.addUri(download_url, save_path, file["name"]))

print("下载任务提交完成！")