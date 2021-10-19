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
```

## Initial Doc

The conditions part of tha tradinghook is where the real work occurs.  This matches a hook an an "action".  Hooks are realtively dumb
as they are merely thrown.  The resulting action is ...

Let's talk some about how a hook can be matched to a condition. We need the conditions portion to be flexiable enough to
work out all the trading conditions we would want.

SYMBOL=APPL
Passphrase=abc123
InstanceID=2
UserID=1
qty=20
side=BUY

Hook abc123,AAPL,140.0,BUY

This is a simple: example where the hook matches the condition.  We seimple place a market BUY for APPL using the Webull Live account.
At the end of the trade the "condition's" status is marked disabled for the remaineder of the day.

We could have a condition also with SYMBOL=*

The rule of thumb is going to be to iterate over the "enabled" conditions to match with symbol first.  The wildcard can be used as a
last resort to match a hook with a particular trade.

This process does mean that tht "work" will need to be put in to match the exchange accounts with the trade size.

This also gives us the ability to match match a hook and create a BUY LIMIT OCO type order.
