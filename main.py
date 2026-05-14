import sqlite3
import re
from zxcvbn import zxcvbn

# ==============================
# 🔍 التحقق من قاعدة البيانات
# ==============================
def check_password_db(password):
    conn = sqlite3.connect("weak_passwords.db")
    cursor = conn.cursor()

    cursor.execute("SELECT 1 FROM weak_passwords WHERE password = ?", (password,))
    result = cursor.fetchone()

    conn.close()
    return result is not None


# ==============================
# 🧠 قواعد كلمة المرور
# ==============================
def check_rules(password):
    rules = {
        "length": len(password) >= 8,
        "uppercase": bool(re.search(r"[A-Z]", password)),
        "lowercase": bool(re.search(r"[a-z]", password)),
        "digits": bool(re.search(r"\d", password)),
        "symbols": bool(re.search(r"[!@#$%^&*(),.?\":{}|<>]", password))
    }
    return rules


# ==============================
# 📊 عرض القواعد
# ==============================
def display_rules(rules):
    print("\n=== Password Rules Check ===")

    print("✔ Length >= 8:", "✅" if rules["length"] else "❌")
    print("✔ Uppercase:", "✅" if rules["uppercase"] else "❌")
    print("✔ Lowercase:", "✅" if rules["lowercase"] else "❌")
    print("✔ Numbers:", "✅" if rules["digits"] else "❌")
    print("✔ Symbols:", "✅" if rules["symbols"] else "❌")


# ==============================
# 🔥 تحليل كلمة المرور
# ==============================
def analyze_password(password):
    result = zxcvbn(password)

    print("\n=== Password Strength Analysis ===")

    levels = ["Very Weak ❌", "Weak ⚠️", "Fair ⚠️", "Strong ✅", "Very Strong 🔒"]
    print(f"Score: {result['score']} / 4")
    print(f"Strength: {levels[result['score']]}")

    # ⏱️ زمن الكسر
    crack_time = result['crack_times_display']
    print("\n⏱️ Estimated Crack Time:")
    print("Online attack:", crack_time['online_no_throttling_10_per_second'])
    print("Offline slow hash:", crack_time['offline_slow_hashing_1e4_per_second'])
    print("Offline fast hash:", crack_time['offline_fast_hashing_1e10_per_second'])

    # ⚠️ التحذيرات
    if result['feedback']['warning']:
        print("\n⚠️ Warning:", result['feedback']['warning'])

    # 💡 الاقتراحات
    if result['feedback']['suggestions']:
        print("\n💡 Suggestions:")
        for s in result['feedback']['suggestions']:
            print("-", s)


# ==============================
# 🎯 التوصيات النهائية
# ==============================
def give_recommendations(rules, is_weak):
    print("\n=== Recommendations ===")

    if is_weak:
        print("❌ Your password is in a known weak database!")

    if not rules["length"]:
        print("- Increase password length (at least 12 recommended)")

    if not rules["uppercase"]:
        print("- Add uppercase letters (A-Z)")

    if not rules["lowercase"]:
        print("- Add lowercase letters (a-z)")

    if not rules["digits"]:
        print("- Add numbers (0-9)")

    if not rules["symbols"]:
        print("- Add symbols (!@#$...)")

    print("\n✔ Tip: Use a passphrase like: BlueSky!Car2026")


# ==============================
# 🚀 البرنامج الرئيسي
# ==============================
def main():
    password = input("Enter your password: ")

    # 1. تحقق من DB
    is_weak = check_password_db(password)

    # 2. تحقق من القواعد
    rules = check_rules(password)
    display_rules(rules)

    # 3. تحليل zxcvbn
    analyze_password(password)

    # 4. توصيات
    give_recommendations(rules, is_weak)


if __name__ == "__main__":
    main()