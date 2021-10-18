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
UserID
Symbol
Passphrase
InstanceID
Tradetype
condition

```
```bash
0: no condition
1: if global-a >0 ; global-a -= 1; order 30, buy Symbol from InstanceID
2: if global-b >0 ; global-b -= 1; order 30, buy Symbol OCO 30/10 InstnaceID
```

0,AAPL,ABC1234,1,

## Initial Doc
