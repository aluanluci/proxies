import queue, threading,subprocess
from requests import get
import json, re


q = queue.Queue()
url="https://api.prezaofree.com.br/adserver/campaign/v3/2b25a088-84ea-11ef-9082-0e639a16be05?size=100"

with open('proxies.txt', 'r') as f:
    proxies = f.read().split('\n')
    if len(proxies) > 1:
        for p in proxies:
            q.put(p)
    else:
        print('proxies.txt is empty.')
        exit()

def run(commands):
    try:
        res=subprocess.run(commands, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return res.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f'Erro ao executar {" ".join(commands)}: {e.stderr.strip()}')
        raise e
        

def main():

    global q

    with open('valids.json', 't+r') as f:
        j=json.load(f)
        j['https']=[]
        j['http']=[]
        f.seek(0)
        json.dump(j, f, indent=4)
        f.truncate()

    while not q.empty():
        proxy = str(q.get())
        try:
            proxy=proxy.replace(re.findall(r".*://", proxy)[0], '')
        except:
            continue
        try:
            https=get(url, proxies={"https": proxy}, timeout=5)
        except:
            continue
        try: 
            http=get(url.replace('https', 'http'), proxies={"http": proxy}, timeout=5)
        except:
            continue
        if https.status_code==401:
            print(f'\033[32m(https) {proxy}\033[0m')
            with open('valids.json', 't+r') as f:
                j=json.load(f)
                if not proxy in j['https']:
                    j['https'].append(proxy)
                    f.seek(0)
                    json.dump(j, f, indent=4)
                    f.truncate()
            run(['git', 'add', 'valids.json'])
            run(['git', 'commit', '-m', 'Updated: valids.json'])
            run(['git', 'push', 'origin', 'main'])

        if http.status_code==401:
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
