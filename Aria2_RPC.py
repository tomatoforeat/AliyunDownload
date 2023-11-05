import requests
import json
import time

class Aria2Download:
    def __init__(self, api):
        # aria2 API地址
        self.api = api
        # 消息id，aria2会原样返回这个id，可以自动生成也可以用其他唯一标识
        self.id = "QXJpYU5nXzE2NzUxMzUwMDFfMC42Mzc0MDA5MTc2NjAzNDM="
 
    def addUri(self, url, path, file=None, proxy=None):
        """
        添加任务
        :param url: 文件下载地址
        :param path: 文件保存路径
        :param file: 文件保存名称
        :param proxy: 代{过}{滤}理地址
        :return:
        """
        data = {
            "id": self.id,
            "jsonrpc": "2.0",
            "method": "aria2.addUri",
            "params": [[url], {"dir": path, "out": file, "all-proxy": proxy, "header": ["User-Agent: pan.baidu.com"]}]
        }
        req = requests.post(url=self.api, data=json.dumps(data))
        return_json = req.json()
        req.close()
        return return_json
 
    def getGlobalStat(self):
        """
        获取全部下载信息
        :return:
        """
        data = {
            "jsonrpc": "2.0",
            "method": "aria2.getGlobalStat",
            "id": self.id
        }
        req = requests.post(url=self.api, data=json.dumps(data))
        return_json = req.json()
        req.close()
        return return_json
 
    def tellActive(self):
        """
        正在下载
        :return:
        """
        data = {
            "jsonrpc": "2.0",
            "method": "aria2.tellActive",
            "id": self.id, "params": [
                ["gid", "totalLength", "completedLength", "uploadSpeed", "downloadSpeed", "connections", "numSeeders",
                 "seeder", "status", "errorCode", "verifiedLength", "verifyIntegrityPending", "files", "bittorrent",
                 "infoHash"]]
        }
 
        req = requests.post(url=self.api, data=json.dumps(data))
        return_json = req.json()
        req.close()
        return return_json
 
    def tellWaiting(self):
        """
        正在等待
        :return:
        """
        data = {"jsonrpc": "2.0", "method": "aria2.tellWaiting",
                "id": self.id,
                "params": [0, 1000, ["gid", "totalLength",
                                     "completedLength",
                                     "uploadSpeed",
                                     "downloadSpeed",
                                     "connections",
                                     "numSeeders",
                                     "seeder", "status",
                                     "errorCode",
                                     "verifiedLength",
                                     "verifyIntegrityPending"]
                           ]
                }
        req = requests.post(url=self.api, data=json.dumps(data))
        return_json = req.json()
        req.close()
        return return_json
 
    def tellStopped(self):
        """
        已完成/已停止
        :return:
        """
        data = {"jsonrpc": "2.0",
                "method": "aria2.tellStopped",
                "id": self.id,
                "params": [-1, 1000, ["gid", "totalLength",
                                      "completedLength",
                                      "uploadSpeed",
                                      "downloadSpeed",
                                      "connections",
                                      "numSeeders", "seeder",
                                      "status", "errorCode",
                                      "verifiedLength",
                                      "verifyIntegrityPending"]]
                }
        req = requests.post(url=self.api, data=json.dumps(data))
        return_json = req.json()
        req.close()
        return return_json
 
    def tellStatus(self, gid):
        """
        任务状态
        :param gid: 任务ID
        :return:
        """
        data = {"jsonrpc": "2.0", "method": "aria2.tellStatus", "id": self.id, "params": [gid, ['status', 'downloadSpeed']]}
        req = requests.post(url=self.api, data=json.dumps(data))
        return_json = req.json()
        req.close()
        return return_json

    def tellPause(self, gid):
        """
        任务状态
        :param gid: 任务ID
        :return:
        """
        data = {"jsonrpc": "2.0", "method": "aria2.pause", "id": self.id, "params": [gid]}
        req = requests.post(url=self.api, data=json.dumps(data))
        return_json = req.json()
        req.close()
        return return_json
 
    def removeDownloadResult(self, gid):
        """
        删除下载结束的任务
        :param gid: 任务ID
        :return:
        """
        data = {"jsonrpc": "2.0", "method": "aria2.removeDownloadResult", "id": self.id, "params": [gid]}
        req = requests.post(url=self.api, data=json.dumps(data))
        return_json = req.json()
        req.close()
        return return_json

if __name__ == '__main__':
    aria2 = Aria2Download("http://192.168.0.201:6800/jsonrpc")
    while True:
        global_status = aria2.getGlobalStat()['result']
        print(global_status)
        # 当等待的任务为0是，程序结束
        if global_status['numWaiting'] == '0':
            break
        else:
            # 当下载速度为0时，暂停当前下载任务
            if global_status['downloadSpeed'] == '0':
                if aria2.tellActive()['result'] != []:
                    gid = aria2.tellActive()['result'][0]['gid']
                    aria2.tellPause(gid)
        time.sleep(180)