import json
from app import tradecode

f = open('exchangeaccounts.json',)
 
data = json.load(f)
 
for i in data['exchangeaccounts']:
    print(i)
 
f.close()
