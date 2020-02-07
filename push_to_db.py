import json
import re

import psycopg2


with open("review.json") as f:
    reviews = json.load(f)

    for data in reviews:

        connection = psycopg2.connect(
            host="172.17.0.2", database="tizzie", user="tizzie", password="tizzie"
        )
        connection.autocommit = True
        cur = connection.cursor()
        cur.execute("select id from products where name=%s", (data["name"],))

        product_id = cur.fetchone()

        if product_id:
            cur.execute(
                "insert into product_review(product,data) values(%s,%s)",
                (product_id[0], json.dumps(data["review"])),
            )
        cur.close()
        connection.close()
