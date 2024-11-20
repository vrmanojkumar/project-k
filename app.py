import db
import json
from flask import Flask, request, render_template

app = Flask(__name__)


@app.route('/', methods = ['GET', 'POST'])
def home():
    return render_template("signin.html")


@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    return render_template("signup.html")



@app.route('/signin', methods = ['GET', 'POST'])
def signin():
    status, username = db.check_user()

    data = {
        "username": username,
        "status": status
    }

    return json.dumps(data)



@app.route('/register', methods = ['GET', 'POST'])
def register():
    status = db.insert_data()
    return json.dumps(status)

@app.route('/dashboard', methods=['GET'])
def dashboard():
    # Ensure the username is passed to the dashboard
    username = request.args.get('username')
    return render_template("dashboard.html", username=username)

@app.route('/add_product', methods=['POST'])
def add_product():
    if 'phone' not in session:  # Ensure the user is logged in
        return {"error": "Unauthorized access"}, 401  # Return unauthorized error

    # Extract form data
    product_name = request.form.get('product_name')
    purchase_date = request.form.get('purchase_date')
    phone = session.get('phone')  # Get the logged-in user's phone number

    # Validate form data
    if not product_name or not purchase_date:
        return {"error": "Missing required fields"}, 400  # Bad request if fields are missing

    # Save product to the database
    status = db.add_product(product_name, purchase_date, phone)

    if status:
        return {"message": "Product added successfully"}, 200  # Success response
    else:
        return {"error": "Failed to add product"}, 500  # Internal server error

@app.route('/view_products', methods=['GET'])
def view_products():
    if 'phone' not in session:  # Ensure the user is logged in
        return redirect('/')  # Redirect to login if not logged in

    phone = session['phone']  # Get the logged-in user's phone number
    user_products = db.get_user_products(phone)  # Fetch products from the database

    return render_template('view_products.html', products=user_products, username=session['username'])



if __name__ == '__main__':
    app.run(debug = True)