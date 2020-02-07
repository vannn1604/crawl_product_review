# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import psycopg2
import json
from . import settings


class CrawlProductPipeline(object):
    def process_item(self, item, spider):
        try:
            connection = psycopg2.connect(
                host=settings.DB_HOST,
                database=settings.DB_NAME,
                user=settings.DB_USER,
                password=settings.DB_PASSWORD,
            )
            connection.autocommit = True
            cur = connection.cursor()
            cur.execute("select id from products where name=%s", (item["name"],))

            product_id = cur.fetchone()

            if product_id:
                cur.execute(
                    "insert into product_review(product,data) values(%s,%s)",
                    (product_id[0], json.dumps(item["review"])),
                )
            cur.close()
            connection.close()
        except:
            pass

        return item
