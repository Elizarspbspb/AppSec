@app.route("/user")
def get_user():
    username = request.args.get("username", "")

    conn = db()
    cursor = conn.cursor()

    query = f"SELECT id, username, email, role FROM users WHERE username = '{username}'"
    cursor.execute(query)

    row = cursor.fetchone()
    conn.close()

    if not row:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "id": row[0],
        "username": row[1],
        "email": row[2],
        "role": row[3]
    })


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=True)

