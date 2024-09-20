import sys
import uuid
from db.database import get_db
from time import sleep

def get_products():
    db = get_db()

    cursor = db.cursor()
    postgreSQL_select_Query = "select sku, title, long_description, price from productos"

    cursor.execute(postgreSQL_select_Query)
    products = cursor.fetchall()

    response = []
    for product in products:
        response.append({
            "sku": product[0],
            "title": product[1],
            "long_description": product[2],
            "price": product[3],
        })
    return response


def get_product(sku):
    db = get_db()

    cursor = db.cursor()
    postgre_sql_select_query = """select sku, title, long_description, price from productos where sku=%s"""

    cursor.execute(postgre_sql_select_query, (sku, ))
    product = cursor.fetchone()

    if not product:
        return None

	# Realizar un retardo para simular que la app tarda en realizar esta operación
    sleep(0.200)

    return {
        "sku": product[0],
        "title": product[1],
        "long_description": product[2],
        "price": product[3],
    }


def create_product(sku, title, long_description, price_euro):
    db = get_db()

    cursor = db.cursor()

    sql = """INSERT INTO productos(title, long_description, price)
             VALUES(%s, %s, %s) RETURNING sku;"""

    cursor.execute(sql, (title, long_description, price_euro,))
    db.commit()
    sku = cursor.fetchone()[0]

    return sku
