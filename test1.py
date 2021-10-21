from webull import webull
from webull import paper_webull
from app import tradecode

ea = tradecode.query_ExchangeAccount(2)

wb = webull()
a = wb.login(ea.exchangeusername, ea.exchangepassword)
print(a)
print("--------")
a = wb.get_trade_token(ea.exchangetoken)
print(a)
print("--------")
a = wb.place_order(stock='AAPL', price=90.0, quant=2)
print(a)
