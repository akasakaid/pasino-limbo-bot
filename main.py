import os
import json
import time
import hashlib
from base64 import b64encode
from config import *
try:
    import requests
    from colorama import *
    init(autoreset=True)
    hijau = Fore.LIGHTGREEN_EX
    merah = Fore.LIGHTRED_EX

except ImportError:
    exit("# module not installed !")

class mainbot:
    def __init__(self):
        self.ses = requests.Session()
        headers = {"Host": "api.pasino.com","User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:93.0) Gecko/20100101 Firefox/93.0","Accept": "*/*","Accept-Language": "en-US,en;q=0.5","Referer": "https://pasino.com/","Content-Type": "application/x-www-form-urlencoded","Origin": "https://pasino.com","Connection": "keep-alive","Sec-Fetch-Dest": "empty","Sec-Fetch-Mode": "cors","Sec-Fetch-Site": "same-site","TE": "trailers"}
        self.ses.headers.update(headers)

    def get_user(self):
        url = "https://api.pasino.com/account/get-user-info"
        data = {"language":"en","token":token}
        req = self.ses.post(url,json=data).json()
        if req["success"]:
            print("# user id :",req["user_id"])
            print("# username :",req["user_name"])
        else:
            exit("# token was expired !")

    def get_balance(self):
        url = "https://api.pasino.com/coin/get-balances"
        data = {"language":"en","token":token}
        req = self.ses.post(url,json=data).json()
        if req["success"]:
            for num,coins in enumerate((req["coins"])):
                if coins["coin"] == coin:
                    return req["coins"][num]["balance"]
    
    def get_target_payout(self):
        win_chance = float(betset["chance"])
        multipler = 97 / win_chance
        return multipler

    def format_number(self,value):
        return "{:8f}".format(value)

    def format_waktu(timed):
        return

    def get_client_seed(self):
        return hashlib.md5(bytes(str(int(time.time() * 1000)),'utf-8')).hexdigest()

    def get_limbo(self):
        url = "https://api.pasino.com/limbo/play"
        basebet = self.format_number(float(betset["base bet"]))
        balance = self.get_balance()
        jumlah_win = 0
        jumlah_lose = 0
        total_win = 0
        total_lose = 0
        reset_win = 0
        reset_lose = 0
        status_win = None
        status_lose = None
        profit = 0
        while True:
            data = {
                "language":"en",
                "client_seed":self.get_client_seed(),
                "bet_amt":basebet,
                "coin":coin,
                "target_payout":self.get_target_payout(),
                "token":token
            }
            req = self.ses.post(url,json=data).json()
            if req["success"]:
                fprofit = self.format_number(float(req["profit"]))
                balance = req["balance"]
                if req["win"] != 0:
                    jumlah_win += 1
                    jumlah_lose = 0
                    reset_win += 1
                    status_win = True
                    status_lose = False
                    profit += float(fprofit)
                    status_hasil = hijau + "win"
                else:
                    jumlah_lose += 1
                    jumlah_win = 0
                    reset_lose += 1
                    status_win = False
                    status_lose = True
                    profit -= float(basebet)
                    status_hasil = merah + "lose "
                # analisi win strike lose strike
                if jumlah_win > total_win:
                    total_win += 1
                if jumlah_lose > total_lose:
                    total_lose += 1
                print(f"# {status_hasil} # {basebet} # {self.format_number(profit)} # {self.format_number(float(balance))}")
                print(f"# win strike {total_win} # lose strike {total_lose}",flush=True,end='\r')
                # perkalian if win
                if float(betset["if win"]) != 0:
                    if status_win:
                        basebet = float(basebet)
                        basebet *= float(betset["if win"])
                        basebet = self.format_number(basebet)
                        status_win = None
                # perkalian if lose
                if float(betset["if lose"]) != 0:
                    if status_lose:
                        basebet = float(basebet)
                        basebet *= float(betset["if lose"])
                        basebet = self.format_number(basebet)
                        status_lose = None
                # reset if win
                if int(betset["reset if win"]) != 0:
                    if reset_win >= int(betset["reset if win"]):
                        basebet = self.format_number(float(betset["base bet"]))
                        reset_win = 0
                # reset if lose
                if int(betset["reset if lose"]) != 0:
                    if reset_lose >= int(betset["reset if lose"]):
                        basebet = self.format_number(float(betset["base bet"]))
                        reset_lose = 0
                # stop if profit
                if float(betset["target profit"]) != 0:
                    if profit >= float(betset["target profit"]):
                        print("- " * 25)
                        print(f"# profit target reacted !")
                        print(f"# you profit : {self.format_number(profit)} {coin.upper()}")
                        print(f"# total balance : {balance} {coin.upper()}")
                        print("- " * 25)
                        exit()
                # stop if balance
                if float(betset["target balance"]) != 0:
                    if float(balance) >= float(betset["target balance"]):
                        print("- " * 25)
                        print(f"# target balance reacted !")
                        print(f"# total balance : {balance} {coin.upper()}")
                        print("- " * 25)
                        exit()
            else:
                print("- " * 25)
                print("# error !")
                print("# message :",req["message"])
                print("- " * 25)
                exit()


if __name__ == "__main__":
    try:
        app = mainbot()
        app.get_user()
        print("# balance :",app.get_balance(),coin)
        app.get_limbo()
    except KeyboardInterrupt:
        exit()