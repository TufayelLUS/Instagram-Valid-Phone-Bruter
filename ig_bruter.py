# Version: Python 3.7.x
# install additional module using command pip install missing_module_name
import requests
import json
import string
import random
import threading
from queue import Queue
import socket

threads_count = 40
socket.setdefaulttimeout(5)

class myThread(threading.Thread):
    def __init__(self, queue, *args):
        self.queue = queue
        self._args = args
        threading.Thread.__init__(self)

    def is_insta_acc(self, cred):
        s = requests.Session()
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36",
            }
        try:
            lp = s.get('https://www.instagram.com/accounts/login/?',headers=headers)
        except:
            return False
        token = s.cookies.get_dict().get('csrftoken')
        url = "https://www.instagram.com/accounts/login/ajax/"
        params = {
            "username": cred,
            "enc_password": "",
            "queryParams": "{\"source\":\"auth_switcher\"}",
            "optIntoOneTap": "false"
            }
        headers = {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9,bn;q=0.8",
            "content-length": "126",
            "content-type": "application/x-www-form-urlencoded",
            #"cookie": "mid=W5uoAwAEAAHQMrm9fx_BelLIVThw; mcd=3; ig_did=91ADCB76-A660-4BE2-8696-EA6C2C514EBB; csrftoken=ZXzr82urYV1fCvFdLvp83ecFs2QvuWqV; rur=FTW",
            "dnt": "1",
            "origin": "https://www.instagram.com",
            "referer": "https://www.instagram.com/accounts/login/?source=auth_switcher",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36",
            "x-csrftoken": token,
            "x-ig-app-id": "936619743392459",
            "x-ig-www-claim": "0",
            "x-instagram-ajax": "7ba5929a3456",
            "x-requested-with": "XMLHttpRequest"
            }
        try:
            rr = s.post(url, headers=headers, data=params).text
            return rr
        except:
            print("Site cannot be accessed! Increase timeout ...")
            return json.dumps({"user":"False"})

    def run(self):
        while True:
            acc = None
            try:
                acc = self.queue.get(timeout=1)
            except:
                return
            low_lim = int(acc.split(":")[0])
            high_lim = int(acc.split(":")[1])
            for x in range(low_lim, high_lim+1):
                print(x)
                try:
                    out = json.loads(self.is_insta_acc("+"+str(x)))
                    ans = out['user']
                except:
                    ans = "False"
                if str(ans) == "True":
                    with open("success.txt", "a+") as suc_file:
                        suc_file.write("+" + str(x) + "\n")
            self.queue.task_done()

if __name__ == "__main__":
    queue= Queue()
    threads = []
    for i in range(threads_count):
        worker = myThread(queue, i)
        worker.setDaemon(True)
        worker.start()
        threads.append(worker)
    with open("list.txt", "r") as main_file:
        for line in main_file:
            line = line.replace("\n", "").strip()
            if line == "":
                continue
            queue.put(line)
        for item in threads:
            item.join()
