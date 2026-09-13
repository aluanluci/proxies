import queue, threading
from requests import get
import json


q = queue.Queue()
valid=[]

with open('proxies.txt', 'r') as f:
    proxies = f.read().split('\n')
    if len(proxies) > 0:
        for p in proxies:
            q.put(p)
    else:
        print('proxies.txt is empty.')
        exit()
def main():

    global q

    while not q.empty():
        proxy = q.get()
        try:
            https=get('https://ipinfo.io/json', proxies={"https": proxy}, timeout=20)
        except:
            continue
        try: 
            http=get('http://ipinfo.io/json', proxies={"http": proxy}, timeout=20)
        except:
            continue
        if https.status_code==200:
            print(f'\033[32m(https) {proxy}\033[0m')
            with open('valids.json', 't+r') as f:
                j=json.load(f)
                if not proxy in j['https']:
                    j['https'].append(proxy)
                    f.seek(0)
                    json.dump(j, f, indent=4)
                    f.truncate()

        if http.status_code==200:
            print(f'\033[32m(http) {proxy}\033[0m')
            with open('valids.json', 't+r') as f:
                j=json.load(f)
                if not proxy in j['http']:
                    j['http'].append(proxy)
                    f.seek(0)
                    json.dump(j, f, indent=4)
                    f.truncate()


for _ in range(10):
    threading.Thread(target=main).start()
# parser=argparse.ArgumentParser("Autotest Proxies")
# parser.add_argument('url', 'u', required=False)
# args=parser.parse_args()
# q = queue.Queue()
# valid_proxies=[]

# with open('proxies.txt', 'r') as f:
#     proxies = f.read().split('\n')
#     for p in proxies:
#         q.put(p)

# def check_proxies():
#     global q
#     while not q.empty():
#         proxy=q.get()
#         try:
#             res=requests.get("https://ipinfo.io/json", 
#                 proxies={
#                     "http": proxy,
#                     "https": proxy
#                 }
#             )
#         except:
#             continue
#         if res.status_code==200:
#             print(proxy)

# for _ in range(10):
#     threading.Thread(target=check_proxies).start()


