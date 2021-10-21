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
symbol="AAPL"
price=90.0
limit_profit = price + 0.30
qty = 1
stop_loss = price - (price * 0.07)
a = wb.place_order_otoco(symbol, price=price, stop_loss_price=stop_loss, limit_profit_price=limit_profit, time_in_force='DAY', quant=qty)

print(a)
