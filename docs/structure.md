# INTRODUCTION

This document will serve to replace my scraps of paper where I have outlined data types/schema.

## Structures

```bash
User
  UserID
  Username
  Password
  Fullname
```

Accountbalance:
```bash
  UserID:
    userid:
    fundid
    exchangeid
    settled
    unsettled
```

ExchangeID:
```bash
0 Webull Paper
1 Webull Live
2 TD Ameritrade Paper
3 TD Ameritrade Live
4 Alpaca Paper
5 Alpaca Live
```

ExchangeAccount:
```bash
InstanceID:
UserID:
ExchangeID:
exchangenickname
exchangeusername
exchangepassword
exchangetoken
```
 - Note "import.py" which can be used to import exchange credentials

In this way a single user may operate with multiple ExchangeIDs.
i.e. If you have more than one TD Ameritrade accounts

Condition
```bash
Status       # enabled / disabled
UserID
Symbol
Passphrase
InstanceID
Tradetype
condition
qty
ordertype    # market,limit
trakeprofit  # 
stoploss     # if stoploss
igg          # if global is greater than 0
```
 
## Initial Doc

The conditions part of tha tradinghook is where the real work occurs.  This matches a hook an an "action".  Hooks are realtively dumb
as they are merely thrown.

To review the theory of operation.  One would use a program like Tradinghook or another program (say Python, C#) to throw a hook.
Trading hook catches the hook and by using conditional logic turns it into an order.

Let's talk some about how a hook can be matched to a condition. We need the conditions portion to be flexiable enough to
work out all the trading conditions we would want.

```bash
SYMBOL=APPL
Passphrase=abc123
InstanceID=2
UserID=1
qty=20
side=BUY
igg=a
```

Hook abc123,AAPL,140.0,BUY

This is a simple: example where the hook matches the condition.  We seimple place a market BUY for APPL using the Webull Live account.
At the end of the trade the "condition's" status is marked disabled for the remaineder of the day. (assuming a was 1)

We could have a condition also with SYMBOL=*

The rule of thumb is going to be to iterate over the "enabled" conditions to match with symbol first.  The wildcard can be used as a
last resort to match a hook with a particular trade.

This process does mean that tht "work" will need to be put in to match the exchange accounts with the trade size.

This also gives us the ability to match match a hook and create a BUY LIMIT OCO type order.

In case by some insane reason someone else is reading this, or in case I am and I have to look this over again, currently I am using
igg as primitive conditional tool to manipulate something called a "global variable".  

  i.e.  If "IGG" If Global is Greater than 0 then this is a valid condition to evaluate.
        If  IGG global var decrements to 0 then also disable this rule.

By using a global variable we give ourselves primitive programming to create something that equates to ... out of this pool I can only trade 3 times.

```bash
{
 "condition": [
        {
            "Status": 1,
            "UserID": 1,
            "Symbol": AAPL,
            "Passphrase": abcd1234,
            "InstanceID": 1,
            "Tradetype": OTCO,
            "qty": 20,
            "ordertype": limit,
            "trakeprofit:" +0.30,
            "stoploss":   -0.07,
            "igg": a,
        }
    ]
}
```
