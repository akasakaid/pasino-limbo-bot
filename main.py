import os
import json
import time
from base64 import b64encode
from hashlib import md5
try:
    import requests
except ImportError:
    exit("# module not installed !")

r = requests.Session()
data = json.loads(open("config.json").read())
headers = {
    "Host": "api.pasino.com",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:93.0) Gecko/20100101 Firefox/93.0",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Referer": "https://pasino.com/",
    "Content-Type": "application/x-www-form-urlencoded",
    "Origin": "https://pasino.com",
    "Connection": "keep-alive",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "TE": "trailers"
}

def get_user(token):
    url = ""
    data = {"language":"en","token":token}

def get_balance(token,coin):
    url = "https://api.pasino.com/coin/get-balances"
    data = {"language":"en","token":token}
    req = r.post(url,headers=headers,json=data)
    print(req.json())

