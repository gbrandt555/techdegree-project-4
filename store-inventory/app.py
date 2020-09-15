from peewee import *
from collections import OrderedDict

import csv
import datetime
import os


db = SqliteDatabase("inventory.db")
new_inventory = []

class Product(Model):
    product_id = AutoField()
    product_name = CharField(max_length=255, unique=True)
    product_quantity = IntegerField(default=0)
    product_price = IntegerField(default=0)
    date_updated = DateTimeField()

    class Meta:
        database = db


def clean_data():
    with open("inventory.csv", newline='') as csvfile:
        product_reader = csv.DictReader(csvfile, delimiter=',')
        rows = list(product_reader)
        for row in rows:
            row['product_quantity'] = int(row['product_quantity'])
            row['product_price'] = int(row['product_price'].replace('$', '').replace('.', ''))
            row['date_updated'] = datetime.datetime.strptime(row['date_updated'], '%m/%d/%Y')

            new_inventory.append(dict(
                product_name = row['product_name'],
                product_quantity = row['product_quantity'],
                product_price = row['product_price'],
                date_updated = row['date_updated']
            ))
        


def menu_loop():
    choice = None
    choices = ['v', 'a', 'b']
    while choice != 'q':
        print("Store Inventory...\n\n")
        print("Choose one of the following options or press 'q' to quit.\n")
        for key, value in menu.items():
            print("{}) {}".format(key, value.__doc__)) 
        choice = input("\nChoose an option: ").lower().strip()
        if choice not in choices:
            print("\n\nInvalid option, please try again")
        elif choice in menu:
            menu[choice]()

def view_entry():
    """View a single product's inventory"""
    new_id = input("Enter the product ID: ")
    entries = Product.select().where(Product.product_id == new_id)
    if entries:
        print("Product ID: {}\n".format(new_id))
        for entry in entries:
            print("Product name: {}".format(entry.product_name))
            print("Product price: {}".format(entry.product_price))
            print("Product quantity: {}".format(entry.product_quantity))
            print("Date updated: {}".format(entry.date_updated))


def add_entry():
    """Add a new product to the database"""


def backup_data():
    """Make a backup of the entire inventory"""



menu = OrderedDict([
    ('v', view_entry),
    ('a', add_entry),
    ('b', backup_data),
])    
    
       
        




if __name__ == "__main__":
    db.connect()
    db.create_tables([Product], safe=True)
    clean_data()
    menu_loop()