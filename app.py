from flask import Flask, render_template, request, jsonify
import sqlite3
from zxcvbn import zxcvbn
from init_db import init_db

init_db()

app = Flask(__name__)

DATABASE = "weak_passwords.db"

def get_db():
    conn = sqlite3.connect(DATABASE)
    return conn

def check_password_db(password):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT 1 FROM weak_passwords WHERE password = ?", (password,))
    result = cursor.fetchone()

    conn.close()
    return result is not None


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/check_password", methods=["POST"])
def check_password():
    data = request.get_json()

    if not data or "password" not in data:
        return jsonify({"error": "Password required"}), 400

    password = data["password"]

    result = zxcvbn(password)
    is_weak = check_password_db(password)

    return jsonify({
        "score": result["score"],
        "crack_time": result["crack_times_display"]["offline_slow_hashing_1e4_per_second"],
        "warning": result["feedback"]["warning"] or "",
        "suggestions": result["feedback"]["suggestions"],
        "is_weak_db": is_weak
    })


if __name__ == "__main__":
    app.run(debug=True)