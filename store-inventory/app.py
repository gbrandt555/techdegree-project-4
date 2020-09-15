from peewee import *

import csv
import datetime
import os


db = SqliteDatabase("inventory.db")


class Product(Model):
    product_id = AutoField()
    product_name = CharField(max_length=255, unique=True)
    product_quantity = IntegerField(default=0)
    product_price = IntegerField(default=0)
    date_updated = DateTimeField()


with open("inventory.csv", newline='') as csvfile:
    product_reader = csv.DictReader(csvfile, delimiter=',')
    rows = list(product_reader)
    for row in rows:
        print(row)



if __name__ == "__main__":
    db.connect()
    db.create_tables([Product], safe=True)