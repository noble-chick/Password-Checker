# Password-Checker

A command-line tool that rates password strength as **WEAK / MEDIUM / STRONG / VERY STRONG**.

## What it checks

| Check | Details |
|---|---|
| Common passwords | Flags top 30 most-used passwords instantly |
| Keyboard patterns | Detects walks like `qwerty`, `123456` |
| Length | Short (<8) penalised, 16+ rewarded |
| Character variety | Lowercase, uppercase, digits, symbols |
| Repeated characters | Penalises `aaa`, `111`, etc. |

## How to run

```bash
python password_checker.py
```

No external libraries needed — pure Python standard library.

## Example output

```
  Password : ***********
  Length   : 11 characters

  Score    : [████████████░░░░░░░░░░░░░░░░░░] 40/100
  Rating   : MEDIUM

  What's good:
    ✅ Decent length (8–11 chars)
    ✅ Contains lowercase letters
    ✅ Contains digits

  What to improve:
    ❌ Add uppercase letters (A–Z)
    ❌ Add symbols like ! @ # $ % ^ & *
```

## Skills covered

- String manipulation and regex (`re` module)
- Functions and dictionaries
- Control flow and scoring logic
- Terminal colors with ANSI escape codes
- Input validation and loops

## File structure

```
password-checker/
├── password_checker.py
└── README.md
```
