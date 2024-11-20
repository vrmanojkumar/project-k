import pymongo
from flask import request

client = pymongo.MongoClient('mongodb+srv://rentalagriindia:cluster123@userlogs.tbiwfbc.mongodb.net/')
userdb = client['userdb']
users = userdb.customers
products = userdb.products
def insert_data():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['pass']

        reg_user = {}
        reg_user['name'] = name
        reg_user['email'] = email
        reg_user['password'] = password

        if users.find_one({"email": email}) is None:
            users.insert_one(reg_user)
            return True
        else:
            return False

def check_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['pass']

        user = {
            "email": email,
            "password": password
        }

        user_data = users.find_one(user)
        if user_data is None:
            return False, ""
        else:
            return True, user_data["name"]

def add_product(product_name, purchase_date, phone):
    product_data = {
        "product_name": product_name,
        "purchase_date": purchase_date,
        "phone": phone,  # Associate the product with the user's phone
        "sensor_output": 0,  # Default sensor output (can be updated later)
        "expiry_date": None  # Optional, can be updated later
    }
    try:
        products.insert_one(product_data)  # Insert product into the "products" collection
        return True
    except Exception as e:
        print(f"Error adding product: {e}")
        return False

def get_user_products(phone):
    try:
        # Fetch all products associated with the user's phone number
        user_products = list(products.find({"phone": phone}))
        return user_products
    except Exception as e:
        print(f"Error retrieving products: {e}")
        return []
