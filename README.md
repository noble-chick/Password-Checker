# Password-Checker

A command-line password strength checker built to follow **NIST SP 800-63B** guidelines — the federal standard for password security.

## What makes this NIST-compliant?

Most password checkers get this wrong. NIST says:

| Common myth | What NIST actually says |
|---|---|
| Require uppercase + symbols + numbers | ❌ Don't enforce composition rules |
| Complex short passwords are strong | ❌ Length matters far more than complexity |
| `P@ssw0rd!` is a strong password | ❌ Predictable substitutions don't help |
| `correct horse battery staple` is weak | ✅ It's extremely strong. 28 chars, unique |

This checker follows those rules.

## How it works

**Gate 1 — Blocklist**
Instantly rejects passwords found on the breached/common passwords list (e.g. `password`, `iloveyou`, `admin`). Real deployments should plug in the [HaveIBeenPwned](https://haveibeenpwned.com/Passwords) 500k+ password list.

**Gate 2 — Minimum length**
Rejects anything under 8 characters (NIST minimum).

**Gate 3 — zxcvbn guessability estimate**
Uses the [`zxcvbn`](https://github.com/dwolfhub/zxcvbn-python) library (originally built by Dropbox) to estimate how many guesses an attacker would need. Scores 0–4 with an estimated crack time.

## Install & run

```bash
pip install zxcvbn
python password_checker.py
```

## Example output

```
  Password   : ••••••••••••••••••••••••••••
  Length     : 28 characters
  Strength   : ▓▓▓▓▓  VERY STRONG
  Crack time : centuries  (213,811,968,952,000,000,000 guesses)

  Suggestions:
    → ✅ Great length — length is the strongest factor per NIST.
```

```
  Password   : •••••••••
  Length     : 9 characters
  Strength   : ▓▓░░░  WEAK
  Crack time : 1 second  (11,100 guesses)

  ⚠️  This is similar to a commonly used password.

  Suggestions:
    → NIST tip: a longer passphrase beats a complex short password.
    → Predictable substitutions like '@' instead of 'a' don't help very much.
```

## Skills covered

- NIST SP 800-63B security standards
- Third-party library integration (`zxcvbn`)
- Blocklist / denylist pattern
- Entropy-based password scoring vs rule-based scoring
- ANSI terminal colors and CLI design

## File structure

```
password-checker/
├── password_checker.py
└── README.md
```

## References

- [NIST SP 800-63B](https://pages.nist.gov/800-63-3/sp800-63b.html)
- [zxcvbn — realistic password strength estimation](https://github.com/dropbox/zxcvbn)
- [HaveIBeenPwned password list](https://haveibeenpwned.com/Passwords)
