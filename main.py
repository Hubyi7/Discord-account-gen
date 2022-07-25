import requests
import random
import string
import time
import threading
import json
import os
import base64

readproxy = open('proxies.txt','r')
readproxy2 = readproxy.readlines()
workproxy = []
for proxy3 in readproxy2:
    proxystrip = proxy3.strip('\n')
    workproxy.append(proxystrip)



with open('config.json') as f:
    cfg = json.load(f)

capkey = cfg['capmonster_key']
threads = cfg['threads']
invite = cfg['invite']


url = "https://discord.com/"
site_key = '4c672d35-0701-42b2-88c3-78380b0db560'


def randomPass():
    return ("".join(random.SystemRandom().choice(string.ascii_lowercase + string.digits)for _ in range(12))) + ("".join(random.SystemRandom().choice(string.ascii_uppercase)))

passwords = "imhAPPYHERE123!" #randomPass()

erorr_count = 0
count = 0


class Generator:
    def __init__(self):
        self._token = None
        self.session = requests.session
        self.capkey = capkey
        
        for _ in range(2):
            threading.Thread(target=self.get_captcha).start()


    def get_captcha(self):

        taskid = 0
        tok = ""
        try:
            json = {
                "clientKey": capkey,
                "task":
                    {
                        "type": "HCaptchaTaskProxyless",
                        "websiteURL": "https://discord.com",
                        "websiteKey": site_key
                    }
            }
            r = requests.post('https://api.capmonster.cloud/createTask', json=json)

            if r.json()['errorId'] == 0:
                taskid = r.json()['taskId']
        except:
            pass
        json = {
            "clientKey": capkey,
            "taskId": taskid
        }

        r = requests.post('https://api.capmonster.cloud/getTaskResult', json=json)
        if r.json()['errorId'] == 0:
            if r.json()['status'] == 'ready':
                tok = r.json()['solution']['gRecaptchaResponse']

        time.sleep(1)
        while 'processing' in r.text:
            time.sleep(2)
            if r.json()['status'] == 'ready':
                tok = r.json()['solution']['gRecaptchaResponse']

        self.GenerateToken(tok)

    def get_x_properties(self):
        data = {
            "os": "Windows",
            "browser": "Chrome",
            "device": "",
            "system_locale": "en-US",
            "browser_user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36",
            "browser_version": "102.0.5005.61",
            "os_version": "10",
            "referrer": "",
            "referring_domain": "",
            "referrer_current": "",
            "referring_domain_current": "",
            "release_channel": "stable",
            "client_build_number": 130153,
            "client_event_source": None
        }

        return base64.b64encode(json.dumps(data).encode())


    def GenerateToken(self, captcha_token):
        global count
        while True: 
            randomday = random.randint(1,30000000)
            randommon = random.randint(1,12)
            email = "catchatok" + str(randomday) + "@gmail.com"
            usernamesf = open("usernames.txt")
            usernames = random.choice(usernamesf.read().splitlines())
            usernamesf.close()
            rate_limit = 0

            response = requests.get('https://discord.com/register')
            dcfduid = response.headers['Set-Cookie'].split('__dcfduid=')[1].split(';')[0]
            response.cookies['__dcfduid'] = dcfduid
            sdcfduid = response.headers['Set-Cookie'].split('__sdcfduid=')[1].split(';')[0]

            proxyb = random.choice(workproxy)
            proxies = {'http': f'http://{proxyb}','https':f'http://{proxyb}'}
            url = "https://discord.com/api/v10/auth/register"
            req = requests.get(
            url='https://discord.com/api/v9/experiments',
            )


            fingerprint = req.json()['fingerprint']

            payload = {
                "captcha_service": "hcaptcha",
                "captcha_key": captcha_token,
                "consent": "true",
                "date_of_birth": "2000-02-13",
                "email": f"{email}",
                "fingerprint": fingerprint,
                "gift_code_sku_id": "null",
                "invite": f"{invite}",
                "password": f"{passwords}",
                "promotional_email_opt_in": "false",
                "username": usernames,
            }

            headers = {
                "host": "discord.com",
                "connection": "keep-alive",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36",
                "content-type": "text/plain;charset=UTF-8",
                'Accept': '*/*',
                'Accept-Language': 'en',
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive',
                'Pragma': 'no-cache',
                'Content-Type': 'application/json',
                'Origin': 'https://discord.com/',
                'Referer': 'https://discord.com/register',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'x-discord-locale': 'en',
                'Sec-Fetch-Site': 'same-origin',
                'Cookie': '__dcfduid=' + dcfduid + '; __sdcfduid=' + sdcfduid,
                'X-Super-Properties': self.get_x_properties(),
                'x-fingerprint': fingerprint,
                'TE': 'Trailers'
            }
            
            r = requests.post("https://discord.com/api/v10/auth/register", proxies=proxies, headers=headers, json=payload)

            if "The resource is being rate limited." in r.text:
                #print('You Are Being Rate Limited')
                rate_limit += 1
            elif "invalid-response" in r.text:
                print('Captcha Solved Incorrectly')

            elif "token" in r.text:
                token = r.json()["token"]
                
                gfd = open('Out/tokens.txt','a+')
                gfd.write(str(token) + str('\n'))
                gfd2 = open('Out/accounts.txt','a+')
                gfd2.write(f'{usernames}:{passwords}\n')
                count += 1
                os.system(f"title  Total Tokens: {count}  Last: {token}")
                print(f"discord.gg/catcha  Catcha Discord gen V1 | {token}\n")
                break
            time.sleep(3)



def start():
    time.sleep(1)
    os.system("cls")
    print(f"catcha Discord Gen V1 : Enjoy Skid\n")
    for i in range(int(threads)):
        threading.Thread(target=Generator).start()
        
start()