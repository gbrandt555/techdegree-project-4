from peewee import *
from collections import OrderedDict

import csv
import datetime
import os
import sys


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
        for row in rows:
            try:    
                Product.create(
                    product_name = row['product_name'],
                    product_quantity = row['product_quantity'],
                    product_price = row['product_price'],
                    date_updated = row['date_updated']
                ).save()
            except IntegrityError:
                temp = Product.get(product_name=row['product_name'])
                temp.product_name = row['product_name']
                temp.product_quantity = row['product_quantity']
                temp.product_price = row['product_price']
                temp.date_updated = row['date_updated']
                temp.save()
        
        


def menu_loop():
    choice = None
    choices = ['v', 'a', 'b', 'q']
    while choice != 'q':
        print("Store Inventory...\n\n")
        print("Choose one of the following options or press 'q' to quit.\n")
        for key, value in menu.items():
            print("{}) {}".format(key, value.__doc__)) 
        choice = input("\nChoose an option: ").lower().strip()
        if choice not in choices:
            clear()
            print("\n\nInvalid option, please try again")
        elif choice in menu:
            menu[choice]()

def view_entry(try_again=None):
    """View a single product's inventory"""
    if try_again:
        clear()
        print("Product ID {} was not found. Please try again.".format(try_again))

    while True:
        new_id = input("Enter the product ID: ")
        try:
            new_id = int(new_id)
            break
        except ValueError:
            clear()
            print("You must enter a number")

    entries = Product.select().where(Product.product_id == new_id)
    if entries:
        clear()
        print("Product ID: {}\n".format(new_id))
        for entry in entries:
            print("Product name: {}".format(entry.product_name))
            print("Product price: {}".format(entry.product_price))
            print("Product quantity: {}".format(entry.product_quantity))
            print("Date updated: {}".format(entry.date_updated))
    else:
        view_entry(try_again=new_id)
       


def add_entry():
    """Add a new product to the database"""
    clear()
    name = input("Enter the product name: ")
    while True:
        quantity = input("Enter the quantity: ")
        try:
            quantity = int(quantity)
            break
        except ValueError:
            print("You must enter a number")
            continue
    
    while True:
        price = input("Enter the price: ")
        try:
            price = float(price)
            price = int(price*100)
            break
        except ValueError:
            print("You must enter a number")
            continue
    Product.create(
        product_name = name,
        product_quantity = quantity,
        product_price = price,
        date_updated = datetime.datetime.now()
    ).save()
        


def backup_data():
    """Make a backup of the entire inventory"""
    clear()
    filename = "Backup_Inventory.csv"
    fieldnames = [
        'product_id',
        'product_name',
        'product_quantity',
        'product_price',
        'date_updated'
    ]

    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=',')
        writer.writeheader()
        all_products = Product.select()
        for item in all_products:
            writer.writerow({
                'product_id': item.product_id,
                'product_name': item.product_name,
                'product_quantity': item.product_quantity,
                'product_price': item.product_price,
                'date_updated': item.date_updated
            })
    
    if os.path.isfile(filename):
        clear()
        print("Backup was successful!")
    else:
        clear()
        print("Backup was not able to be completed...")



menu = OrderedDict([
    ('v', view_entry),
    ('a', add_entry),
    ('b', backup_data),
])    
    
       
def clear():
    os.system("cls" if os.name == 'nt' else "clear")        




if __name__ == "__main__":
    db.connect()
    db.create_tables([Product], safe=True)
    clean_data()
    menu_loop()