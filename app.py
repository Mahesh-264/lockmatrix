from flask import Flask, render_template, request, jsonify
import random
import string

app = Flask(__name__)

print("🔄 Starting Backend Server...")


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

    base = username[:3]

    remaining_length = max(length - len(base) - 2, 1)

    random_part = ''.join(
        random.choice(characters)
        for _ in range(remaining_length)
    )

    special_part = (
        random.choice(special_chars)
        + random.choice(special_chars)
    )

    password = base + random_part + special_part

    return jsonify({
        "password": password
    })


@app.route('/passwords', methods=['GET'])
def get_passwords():
    return jsonify([])


# -----------------------
# Run Server
# -----------------------

if __name__ == '__main__':
    print("🚀 Backend Running")
    app.run(host='0.0.0.0', port=5000)
