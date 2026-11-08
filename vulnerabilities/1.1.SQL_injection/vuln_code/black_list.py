def is_safe(value):
    blocked = ["'", '"', "--", ";", " OR ", " or "]

    for item in blocked:
        if item in value:
            return False

    return True


@app.route("/products")
def products():
    category = request.args.get("category", "")
    sort = request.args.get("sort", "name")

    if not is_safe(category):
        return jsonify({"error": "Bad input"}), 400

    if sort not in ["name", "price", "created_at"]:
        sort = "name"

    conn = db()
    cursor = conn.cursor()

    query = f"""
        SELECT id, name, price, category
        FROM products
        WHERE category = '{category}'
        ORDER BY {sort}
    """

    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()

    result = []

    for row in rows:
        result.append({
            "id": row[0],
            "name": row[1],
            "price": row[2],

