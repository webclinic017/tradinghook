import json
import os.path
from app import tradecode

if os.path.isfile("exchangeaccounts.json"):
    f = open('exchangeaccounts.json',)
 
    data = json.load(f)
 
    for i in data['exchangeaccounts']:
        ea = tradecode.ExchangeAccount()
        ea.InstanceID = i["InstanceID"]
        ea.UserID = i["UserID"]
        ea.ExchangeID = i["ExchangeID"]
        ea.exchangenickname = i["exchangenickname"]
        ea.exchangeusername = i["exchangeusername"]
        ea.exchangepassword = i["exchangepassword"]
        ea.exchangetoken = i["exchangetoken"]
        tradecode.insert_into_ExchangeAccount(ea)
        print(i)
 
    f.close()
