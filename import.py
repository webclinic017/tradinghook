import json
import os.path
from app import tradecode

if exits("exchangeaccounts.json"):
    f = open('exchangeaccounts.json',)
 
    data = json.load(f)
 
    for i in data['exchangeaccounts']:
        ea = ExchangeAccount()
        eat.InstanceID = i["InstanceID"]
        ea.UserID = i["UserID"]
        ea.ExchangeID = i["ExchangeID"]
        ea.exchangenickname = i["exchangenickname"]
        ea.exchangeusername = i["exchangeusername"]
        ea.exchangepassword = i["exchangepassword"]
        ea.exchangetoken = i["exchangetoken"]
        tradecode.insert_into_ExchangeAccount(ea)
        print(i)
 
    f.close()
