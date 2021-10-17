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

Exchanges:
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
  UserID:
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

```bash
Condition
  UserID
  Symbol
  Passphrase
  FundID
  Tradetype
  condition
```

## Initial Doc
