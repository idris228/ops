import pymysql


def get_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="root",
        database="shop_db",
        cursorclass=pymysql.cursors.DictCursor
    )


def auth(login, password):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = """
            SELECT *
            FROM users
            WHERE login=%s AND password=%s
            """
            cursor.execute(sql, (login, password))
            return cursor.fetchone()
    finally:
        conn.close()


def get_products(search="", sort=""):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = """
            SELECT *
            FROM products
            WHERE name LIKE %s
            """
            params = [f"%{search}%"]
            if sort == "price_asc":
                sql += " ORDER BY price ASC"
            elif sort == "price_desc":
                sql += " ORDER BY price DESC"
            cursor.execute(sql, params)
            return cursor.fetchall()
    finally:
        conn.close()


def add_product(data):
    conn = get_connection()

    try:
        with conn.cursor() as cursor:

            sql = """
            INSERT INTO products(
                category,
                name,
                description,
                manufacturer,
                supplier,
                price,
                stock_quantity,
                discount,
                image_path
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """

            cursor.execute(sql, (
                data["category"],
                data["name"],
                data["description"],
                data["manufacturer"],
                data["supplier"],
                data["price"],
                data["stock_quantity"],
                data["discount"],
                data["image_path"]
            ))

            conn.commit()

    finally:
        conn.close()


def update_product(product_id, data):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = """
            UPDATE products
            SET
                category=%s,
                name=%s,
                description=%s,
                manufacturer=%s,
                supplier=%s,
                price=%s,
                stock_quantity=%s,
                discount=%s,
                image_path=%s
            WHERE id=%s
            """
            cursor.execute(sql, (
                data["category"],
                data["name"],
                data["description"],
                data["manufacturer"],
                data["supplier"],
                data["price"],
                data["stock_quantity"],
                data["discount"],
                data["image_path"],
                product_id
            ))
            conn.commit()
    finally:
        conn.close()


def delete_product(product_id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = "DELETE FROM products WHERE id=%s"
            cursor.execute(sql, (product_id,))
            conn.commit()
    finally:
        conn.close()


def get_orders():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = """
            SELECT
                orders.id,
                orders.user_id,
                orders.product_id,
                orders.quantity,
                orders.total_price,
                orders.status,
                users.login AS client_name,
                products.name AS product_name
            FROM orders
            JOIN users ON users.id = orders.user_id
            JOIN products ON products.id = orders.product_id
            """
            cursor.execute(sql)
            return cursor.fetchall()
    finally:
        conn.close()


def add_order(data):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = """
            INSERT INTO orders(
                user_id,
                product_id,
                quantity,
                total_price,
                status
            )
            VALUES (%s,%s,%s,%s,%s)
            """
            cursor.execute(sql, (
                data["user_id"],
                data["product_id"],
                data["quantity"],
                data["total_price"],
                data["status"]
            ))
            conn.commit()
    finally:
        conn.close()


def update_order(order_id, data):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = """
            UPDATE orders
            SET
                user_id=%s,
                product_id=%s,
                quantity=%s,
                total_price=%s,
                status=%s
            WHERE id=%s
            """
            cursor.execute(sql, (
                data["user_id"],
                data["product_id"],
                data["quantity"],
                data["total_price"],
                data["status"],
                order_id
            ))
            conn.commit()
    finally:
        conn.close()


def delete_order(order_id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = "DELETE FROM orders WHERE id=%s"
            cursor.execute(sql, (order_id,))
            conn.commit()
    finally:
        conn.close()
