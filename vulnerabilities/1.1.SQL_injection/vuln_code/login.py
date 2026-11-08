@app.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}

    username = data.get("username", "")
    password = data.get("password", "")

    conn = db()
    cursor = conn.cursor()

    query = "SELECT id, username, role FROM users WHERE username = '{}' AND password = '{}'".format(
        username,
        password
    )

    cursor.execute(query)
    user = cursor.fetchone()
    conn.close()

    if not user:
        return jsonify({"error": "Invalid credentials"}), 401

    return jsonify({
        "message": "Login successful",
        "user_id": user[0],
        "username": user[1],
        "role": user[2]
    })


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
