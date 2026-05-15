"""
password_checker.py
NIST SP 800-63B compliant
NIST says:
  ✅ Length is the most important factor (min 8, encourage 15+)
  ✅ Check against breached / common passwords (blocklist)
  ✅ Estimate real-world guessability — not arbitrary complexity rules
  ✅ Allow ALL printable characters (spaces, emojis, symbols — everything)
  ❌ Do NOT require uppercase, symbols, digits
  ❌ Do NOT enforce composition rules

Uses the `zxcvbn` library which estimates how many guesses an attacker
would need which is the same approach used by Dropbox internally.

Install:  pip install zxcvbn
Run:      python password_checker.py
"""

import sys

try:
    from zxcvbn import zxcvbn
except ImportError:
    print("Missing dependency. Run:  pip install zxcvbn")
    sys.exit(1)


#  NIST Blocklist (sample — real deployments
#  should use HaveIBeenPwned's 500k+ list)

BLOCKLIST = {
    "password", "123456", "123456789", "qwerty", "abc123",
    "password1", "111111", "12345678", "iloveyou", "admin",
    "letmein", "monkey", "sunshine", "master", "princess",
    "dragon", "passw0rd", "shadow", "superman", "welcome",
    "login", "hello", "charlie", "donald", "password123",
    "qwerty123", "baseball", "football", "michael",
}

NIST_MIN_LENGTH = 8


#  NIST-compliant check

def check_password(password: str) -> dict:
    # Gate 1: blocklist
    if password.lower() in BLOCKLIST:
        return {
            "blocked":    True,
            "too_short":  False,
            "score":      0,
            "rating":     "BLOCKED",
            "crack_time": "instant",
            "guesses":    0,
            "feedback":   ["This password is on the breached/common passwords list."],
            "warning":    "Choose something that isn't a well-known password.",
        }

    # Gate 2: minimum length (NIST minimum is 8)
    if len(password) < NIST_MIN_LENGTH:
        return {
            "blocked":    False,
            "too_short":  True,
            "score":      0,
            "rating":     "TOO SHORT",
            "crack_time": "very fast",
            "guesses":    0,
            "feedback":   [f"NIST requires at least {NIST_MIN_LENGTH} characters."],
            "warning":    "",
        }

    # zxcvbn guessability estimate
    result  = zxcvbn(password)
    score   = result["score"]   # 0 (worst) to 4 (best)
    guesses = result["guesses"]
    crack   = result["crack_times_display"]["offline_slow_hashing_1e4_per_second"]
    warning = result["feedback"]["warning"]
    tips    = list(result["feedback"]["suggestions"])

    RATINGS = {0: "VERY WEAK", 1: "WEAK", 2: "FAIR", 3: "STRONG", 4: "VERY STRONG"}

    # NIST nudge: reward length
    if len(password) < 12:
        tips.insert(0, "💡 NIST tip: a longer passphrase beats a complex short password.")
    elif len(password) >= 20:
        tips.insert(0, "✅ Great length — length is the strongest factor per NIST.")

    return {
        "blocked":    False,
        "too_short":  False,
        "score":      score,
        "rating":     RATINGS[score],
        "crack_time": crack,
        "guesses":    guesses,
        "feedback":   tips,
        "warning":    warning,
    }


#  Display helpers

ANSI = {
    "BLOCKED":      "\033[91m",
    "TOO SHORT":    "\033[91m",
    "VERY WEAK":    "\033[91m",
    "WEAK":         "\033[93m",
    "FAIR":         "\033[33m",
    "STRONG":       "\033[92m",
    "VERY STRONG":  "\033[96m",
    "BOLD":         "\033[1m",
    "RESET":        "\033[0m",
}

SCORE_BARS = {0: "▓░░░░", 1: "▓▓░░░", 2: "▓▓▓░░", 3: "▓▓▓▓░", 4: "▓▓▓▓▓"}

def c(text, key):
    return f"{ANSI.get(key, '')}{text}{ANSI['RESET']}"

def print_result(result: dict, password: str) -> None:
    rating = result["rating"]
    bar    = SCORE_BARS.get(result["score"], "░░░░░")

    print()
    print(c("─" * 50, "BOLD"))
    print(c("  🔐 NIST SP 800-63B Password Checker", "BOLD"))
    print(c("─" * 50, "BOLD"))
    print(f"\n  Password   : {'•' * len(password)}")
    print(f"  Length     : {len(password)} characters")

    if not result["blocked"] and not result["too_short"]:
        print(f"  Strength   : {c(bar + '  ' + rating, rating)}")
        print(f"  Crack time : {result['crack_time']}  ({result['guesses']:,} guesses)")
    else:
        print(f"  Status     : {c(rating, rating)}")

    if result["warning"]:
        print(f"\n  ⚠️  {result['warning']}")

    if result["feedback"]:
        print("\n  Suggestions:")
        for tip in result["feedback"]:
            print(f"    → {tip}")

    print()
    print(c("  ℹ️  Per NIST: length matters most. Uppercase,", "BOLD"))
    print(c("     symbols, and digits are not REQUIRED.", "BOLD"))
    print(c("─" * 50, "BOLD"))


#  Main

def main():
    print(c("\n🔐 NIST-Compliant Password Strength Checker", "BOLD"))
    print("   Based on NIST SP 800-63B guidelines.")
    print("   Type 'quit' to exit.\n")

    while True:
        try:
            pwd = input("  Enter a password: ")
        except (KeyboardInterrupt, EOFError):
            print("\n  Bye!")
            sys.exit(0)

        if pwd.lower() == "quit":
            print("  Bye!")
            break

        if not pwd:
            print("  ⚠️  Please enter something.\n")
            continue

        result = check_password(pwd)
        print_result(result, pwd)
        print()


if __name__ == "__main__":
    main()
