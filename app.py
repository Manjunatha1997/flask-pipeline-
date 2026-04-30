from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, World!"


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    # -------------------------
    # 1. VALIDATION LAYER
    # -------------------------
    if not data:
        return jsonify({"message": "Missing JSON body"}), 400

    username = data.get("username")
    password = data.get("password")

    if username is None or password is None:
        return jsonify({"message": "Missing fields"}), 400

    if not isinstance(username, str) or not isinstance(password, str):
        return jsonify({"message": "Invalid data types"}), 400

    if username.strip() == "" or password.strip() == "":
        return jsonify({"message": "Empty fields"}), 400

    # -------------------------
    # 2. AUTHENTICATION LAYER
    # -------------------------
    if username == "admin" and password == "password":
        return jsonify({"message": "Login successful"}), 200

    return jsonify({"message": "Invalid credentials"}), 401

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)