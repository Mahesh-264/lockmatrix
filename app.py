from flask import Flask, render_template, request, jsonify
import random
import string
import mysql.connector

app = Flask(__name__)

print("🔄 Starting Backend Server...")

# -----------------------
# MySQL Connection
# -----------------------
try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",   # <-- change this
        database="paswordmanager"
    )
    cursor = db.cursor(dictionary=True)
    print("✅ Connected to MySQL Database: paswordmanager")

except Exception as e:
    print("❌ Database Connection Failed:", e)


# -----------------------
# Password Generator Logic
# -----------------------
def generate_password(length, use_upper, use_digits, use_symbols):
    characters = string.ascii_lowercase

    if use_upper:
        characters += string.ascii_uppercase
    if use_digits:
        characters += string.digits
    if use_symbols:
        characters += string.punctuation

    return ''.join(random.choice(characters) for _ in range(length))


# -----------------------
# Routes
# -----------------------

@app.route('/')
def index():
    print("📄 Homepage Loaded")
    return render_template('index.html')


@app.route('/generate', methods=['POST'])
def generate():
    print("⚡ Generate API called")

    data = request.json
    username = data['username']
    pwd_type = data['type']
    length = int(data['length'])

    special_chars = "!@#$%&*"

    if pwd_type == "numeric":
        characters = string.digits
    elif pwd_type == "string":
        characters = string.ascii_letters
    else:
        characters = string.ascii_letters + string.digits

    # Ensure username is included
    base = username[:3]  # first 3 letters of username

    remaining_length = length - len(base) - 2

    random_part = ''.join(random.choice(characters) for _ in range(remaining_length))
    special_part = random.choice(special_chars) + random.choice(special_chars)

    password = base + random_part + special_part

    cursor.execute(
        "INSERT INTO passwords (username, password, type) VALUES (%s, %s, %s)",
        (username, password, pwd_type)
    )
    db.commit()

    print("💾 Password Stored Successfully")

    return jsonify({"password": password})

@app.route('/passwords', methods=['GET'])
def get_passwords():
    print("📥 Fetching Stored Passwords")
    cursor.execute("SELECT * FROM passwords ORDER BY id DESC")
    passwords = cursor.fetchall()
    return jsonify(passwords)


# -----------------------
# Run Server
# -----------------------
if __name__ == '__main__':
    print("🚀 Backend Running at http://127.0.0.1:5000")
    app.run(debug=True)