@app.route("/product")
def product():
    product_id = int(request.args.get("id"))

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    query = f"""
        SELECT id, name, price, category
        FROM products
        WHERE id = {product_id}
    """

    cursor.execute(query)
    row = cursor.fetchone()
    conn.close()

    if row is None:
        return jsonify({"error": "Product not found"}), 404

    return jsonify({
        "id": row[0],
        "name": row[1],
        "price": row[2],
        "category": row[3]
    })


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)

