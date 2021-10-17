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

accounts:
```bash
  UserID:
    InstanceID:
    AccountID:
    ExchangeNickname
    exchangeusername
    Exchangepassword
    exchangetoken
```

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
