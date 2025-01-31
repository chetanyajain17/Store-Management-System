import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
import datetime  # Import datetime module for date-related operations

# Connect to MySQL database
db = mysql.connector.connect(user="root", passwd="chetan17012005", host="localhost", database='sem4')
cursor = db.cursor()

# Create necessary tables if they don't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS supplier (
        supplierID INT PRIMARY KEY,
        supplierName VARCHAR(50) NOT NULL,
        contact VARCHAR(20),
        email VARCHAR(50),
        company_name VARCHAR(50)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        prodID INT PRIMARY KEY,
        prodName VARCHAR(50) NOT NULL,
        prodPrice DECIMAL(10, 2) NOT NULL,
        supplierID INT,
        product_company VARCHAR(50),
        quantity INT DEFAULT 0,
        FOREIGN KEY (supplierID) REFERENCES supplier(supplierID)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS customer (
        customerID INT PRIMARY KEY,
        customerName VARCHAR(50) NOT NULL,
        contact VARCHAR(20),
        email VARCHAR(50)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS bill (
        billID INT AUTO_INCREMENT PRIMARY KEY,
        customerID INT,
        total_amount DECIMAL(10, 2),
        bill_date DATE,
        FOREIGN KEY (customerID) REFERENCES customer(customerID)
    )
""")

# Function to update supplier options in the dropdown
def update_supplier_options():
    cursor.execute("SELECT supplierID, supplierName FROM supplier")
    suppliers = cursor.fetchall()
    supplier_options = {supplier[0]: supplier[1] for supplier in suppliers}

    if supplier_options:
        supplier_var.set(list(supplier_options.keys())[0])
        supplier_dropdown['values'] = list(supplier_options.values())
    else:
        supplier_var.set("")
        supplier_dropdown['values'] = []


# Function to update product options in the dropdown
def update_product_options():
    cursor.execute("SELECT prodID, prodName FROM products")
    products = cursor.fetchall()
    product_options = {product[1]: product[0] for product in products}

    if product_options:
        product_var.set(list(product_options.keys())[0])
        product_dropdown['values'] = list(product_options.keys())
    else:
        product_var.set("")
        product_dropdown['values'] = []


# Function to add a new supplier to the database
def add_supplier():
    supplier_id = int(supplier_id_entry.get())
    name = supplier_name_entry.get()
    contact = contact_entry.get()
    email = email_entry.get()
    company = company_name_entry.get()

    if name and company:
        try:
            # Insert Supplier into Database
            query = "INSERT INTO supplier (supplierID, supplierName, contact, email, company_name) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(query, (supplier_id, name, contact, email, company))
            db.commit()
            messagebox.showinfo("Success", "Supplier added successfully")
            update_supplier_options()  # Refresh supplier options after adding new supplier
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add supplier: {e}")
    else:
        messagebox.showerror("Error", "Please provide supplier ID, name, and company name")


# Function to add a new product to the database
def add_product():
    name = prod_name_entry.get()
    price = float(prod_price_entry.get())
    company = prod_company_entry.get()
    supplier_id = supplier_var.get()
    product_id = int(prod_id_entry.get()) if prod_id_entry.get() else None  # Get the product ID if provided

    if name and price > 0 and supplier_id:
        try:
            # Insert Product into Database
            if product_id:
                query = "INSERT INTO products (prodID, prodName, prodPrice, supplierID, product_company) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(query, (product_id, name, price, supplier_id, company))
            else:
                query = "INSERT INTO products (prodName, prodPrice, supplierID, product_company) VALUES (%s, %s, %s, %s)"
                cursor.execute(query, (name, price, supplier_id, company))

            db.commit()
            messagebox.showinfo("Success", "Product added successfully")
            update_product_options()  # Refresh product options after adding new product
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add product: {e}")
    else:
        messagebox.showerror("Error", "Please provide product name, price, company, and select a supplier")


# Function to delete a product from the database by ID
def delete_product_by_id():
    product_id = int(delete_id_entry.get())

    if product_id:
        try:
            # Delete Product from Database
            query = "DELETE FROM products WHERE prodID = %s"
            cursor.execute(query, (product_id,))
            db.commit()
            messagebox.showinfo("Success", f"Product with ID '{product_id}' deleted successfully")
            update_product_options()  # Refresh product options after deletion
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete product: {e}")
    else:
        messagebox.showerror("Error", "Please enter a valid product ID")


# Function to view all products
def view_products():
    # Fetch products from the database
    cursor.execute("SELECT prodID, prodName, prodPrice, product_company FROM products")
    products = cursor.fetchall()

    if products:
        # Create a new window to display products
        products_window = tk.Toplevel(root)
        products_window.title("Products")

        # Display products in a treeview
        tree = ttk.Treeview(products_window, columns=("Name", "Price (₹)", "Company"))
        tree.heading("#0", text="ID")
        tree.heading("Name", text="Name")
        tree.heading("Price (₹)", text="Price (₹)")
        tree.heading("Company", text="Company")

        for product in products:
            tree.insert("", "end", text=product[0], values=(product[1], f"₹{product[2]:.2f}", product[3]))

        tree.pack(expand=True, fill="both")
    else:
        messagebox.showinfo("No Products", "No products found in the database.")

def add_customer():
    customer_id = int(customer_id_entry.get())
    name = customer_name_entry.get()
    contact = customer_contact_entry.get()
    email = customer_email_entry.get()

    if name:
        try:
            # Insert Customer into Database
            query = "INSERT INTO customer (customerID, customerName, contact, email) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (customer_id, name, contact, email))
            db.commit()
            messagebox.showinfo("Success", "Customer added successfully")
            update_customer_options()  # Refresh customer options after adding new customer
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add customer: {e}")
    else:
        messagebox.showerror("Error", "Please provide customer ID and name")


def update_customer_options():
    cursor.execute("SELECT customerID, customerName FROM customer")
    customers = cursor.fetchall()
    customer_options = {customer[0]: customer[1] for customer in customers}

    if customer_options:
        customer_var.set(list(customer_options.keys())[0])
        customer_dropdown['values'] = list(customer_options.values())
    else:
        customer_var.set("")
        customer_dropdown['values'] = []


def view_customers():
    # Fetch customers from the database
    cursor.execute("SELECT customerID, customerName, contact, email FROM customer")
    customers = cursor.fetchall()

    if customers:
        # Create a new window to display customers
        customers_window = tk.Toplevel(root)
        customers_window.title("Customers")

        # Display customers in a treeview
        tree = ttk.Treeview(customers_window, columns=("Name", "Contact", "Email"))
        tree.heading("#0", text="ID")
        tree.heading("Name", text="Name")
        tree.heading("Contact", text="Contact")
        tree.heading("Email", text="Email")

        for customer in customers:
            tree.insert("", "end", text=customer[0], values=(customer[1], customer[2], customer[3]))

        tree.pack(expand=True, fill="both")
    else:
        messagebox.showinfo("No Customers", "No customers found in the database.")

# Function to generate a receipt
def generate_receipt(customer_name, bill_date, products, total_amount):
    receipt_window = tk.Toplevel(root)
    receipt_window.title("Receipt")

    receipt_frame = ttk.Frame(receipt_window, padding="20")
    receipt_frame.grid(row=0, column=0, sticky="nsew")

    tk.Label(receipt_frame, text=f"Customer Name: {customer_name}").grid(row=0, column=0, sticky="w")
    tk.Label(receipt_frame, text=f"Bill Date: {bill_date}").grid(row=1, column=0, sticky="w")

    tk.Label(receipt_frame, text="Products:").grid(row=2, column=0, sticky="w")
    for idx, product in enumerate(products, start=3):
        tk.Label(receipt_frame, text=f"{product[0]} (Qty: {product[1]}) - ₹{product[2]:.2f}").grid(row=idx, column=0, sticky="w")

    tk.Label(receipt_frame, text="-------------------------------------------").grid(row=idx+1, column=0, sticky="w")
    tk.Label(receipt_frame, text=f"Total Amount: ₹{total_amount:.2f}").grid(row=idx+2, column=0, sticky="w")

# Function to generate a bill
def generate_bill():
    customer_id = customer_var.get()
    total_amount = calculate_total_amount()
    bill_date = datetime.date.today()

    if customer_id and total_amount > 0:
        try:
            # Insert Bill into Database
            query = "INSERT INTO bill (customerID, total_amount, bill_date) VALUES (%s, %s, %s)"
            cursor.execute(query, (customer_id, total_amount, bill_date))
            db.commit()
            messagebox.showinfo("Success", "Bill generated and stored successfully")

            # Fetch customer details
            cursor.execute("SELECT customerName FROM customer WHERE customerID = %s", (customer_id,))
            customer_name = cursor.fetchone()[0]

            # Fetch products selected for the bill
            products = []
            for product_id, quantity in selected_products.items():
                cursor.execute("SELECT prodName, prodPrice FROM products WHERE prodID = %s", (product_id,))
                product_details = cursor.fetchone()
                product_name = product_details[0]
                product_price = product_details[1]
                products.append((product_name, quantity, product_price))

            # Generate and display the receipt
            generate_receipt(customer_name, bill_date, products, total_amount)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate bill: {e}")
    else:
        messagebox.showerror("Error", "Please select a customer and add products to generate a bill")

def calculate_total_amount():
    # Fetch products selected for the bill and calculate total amount
    total_amount = 0

    for product_id, quantity in selected_products.items():
        cursor.execute("SELECT prodPrice FROM products WHERE prodID = %s", (product_id,))
        product_price = cursor.fetchone()[0]
        total_amount += product_price * quantity

    return total_amount

# Function to handle adding selected products to the bill
selected_products = {}

def add_product_to_bill():
    product_id = product_var.get()
    quantity = int(quantity_entry.get())

    if product_id and quantity > 0:
        selected_products[product_id] = quantity
        messagebox.showinfo("Success", "Product added to bill")
    else:
        messagebox.showerror("Error", "Please select a product and provide quantity")

# GUI Setup
root = tk.Tk()
root.title("Shop Management System")

# Supplier Section
supplier_frame = ttk.LabelFrame(root, text="Add Supplier")
supplier_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

tk.Label(supplier_frame, text="Supplier ID:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
supplier_id_entry = tk.Entry(supplier_frame, width=30)
supplier_id_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

tk.Label(supplier_frame, text="Supplier Name:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
supplier_name_entry = tk.Entry(supplier_frame, width=30)
supplier_name_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

tk.Label(supplier_frame, text="Contact:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
contact_entry = tk.Entry(supplier_frame, width=30)
contact_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

tk.Label(supplier_frame, text="Email:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
email_entry = tk.Entry(supplier_frame, width=30)
email_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")

tk.Label(supplier_frame, text="Company Name:").grid(row=4, column=0, padx=5, pady=5, sticky="e")
company_name_entry = tk.Entry(supplier_frame, width=30)
company_name_entry.grid(row=4, column=1, padx=5, pady=5, sticky="w")

add_supplier_button = tk.Button(supplier_frame, text="Add Supplier", command=add_supplier)
add_supplier_button.grid(row=5, column=0, columnspan=2, pady=10)

# Product Section
product_frame = ttk.LabelFrame(root, text="Add Product")
product_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

tk.Label(product_frame, text="Product ID:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
prod_id_entry = tk.Entry(product_frame, width=30)
prod_id_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

tk.Label(product_frame, text="Product Name:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
prod_name_entry = tk.Entry(product_frame, width=30)
prod_name_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

tk.Label(product_frame, text="Product Price (₹):").grid(row=2, column=0, padx=5, pady=5, sticky="e")
prod_price_entry = tk.Entry(product_frame, width=30)
prod_price_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

tk.Label(product_frame, text="Product Company:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
prod_company_entry = tk.Entry(product_frame, width=30)
prod_company_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")

# Fetch initial supplier options and populate the dropdown
supplier_var = tk.IntVar()
supplier_dropdown = ttk.Combobox(product_frame, textvariable=supplier_var, width=27)
supplier_dropdown.grid(row=4, column=1, padx=5, pady=5, sticky="w")

update_supplier_options()  # Populate supplier options initially

tk.Label(product_frame, text="Supplier:").grid(row=4, column=0, padx=5, pady=5, sticky="e")

add_product_button = tk.Button(product_frame, text="Add Product", command=add_product)
add_product_button.grid(row=5, column=0, columnspan=2, pady=10)

# Delete Product Section
delete_frame = ttk.LabelFrame(root, text="Delete Product")
delete_frame.grid(row=2, column=2, padx=10, pady=10, sticky="nsew")

tk.Label(delete_frame, text="Product ID:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
delete_id_entry = tk.Entry(delete_frame, width=30)
delete_id_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

delete_product_button = tk.Button(delete_frame, text="Delete Product", command=delete_product_by_id)
delete_product_button.grid(row=1, column=0, columnspan=2, pady=10)


# View Products Section
view_products_button = tk.Button(root, text="View Products", command=view_products)
view_products_button.grid(row=3, column=0, padx=10, pady=10)

# Customer Section
customer_frame = ttk.LabelFrame(root, text="Add Customer")
customer_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

tk.Label(customer_frame, text="Customer ID:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
customer_id_entry = tk.Entry(customer_frame, width=30)
customer_id_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

tk.Label(customer_frame, text="Customer Name:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
customer_name_entry = tk.Entry(customer_frame, width=30)
customer_name_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

tk.Label(customer_frame, text="Contact:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
customer_contact_entry = tk.Entry(customer_frame, width=30)
customer_contact_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

tk.Label(customer_frame, text="Email:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
customer_email_entry = tk.Entry(customer_frame, width=30)
customer_email_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")

add_customer_button = tk.Button(customer_frame, text="Add Customer", command=add_customer)
add_customer_button.grid(row=4, column=0, columnspan=2, pady=10)

# Fetch initial customer options and populate the dropdown
customer_var = tk.IntVar()
customer_dropdown = ttk.Combobox(customer_frame, textvariable=customer_var, width=27)
customer_dropdown.grid(row=5, column=1, padx=5, pady=5, sticky="w")

update_customer_options()  # Populate customer options initially

tk.Label(customer_frame, text="Customer:").grid(row=5, column=0, padx=5, pady=5, sticky="e")

# View Customers Section
view_customers_button = tk.Button(root, text="View Customers", command=view_customers)
view_customers_button.grid(row=1, column=1, padx=10, pady=10)

# GUI Updates
bill_frame = ttk.LabelFrame(root, text="Generate Bill")
bill_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

tk.Label(bill_frame, text="Select Product:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
product_var = tk.IntVar()
product_dropdown = ttk.Combobox(bill_frame, textvariable=product_var, width=27)
product_dropdown.grid(row=0, column=1, padx=5, pady=5, sticky="w")

update_product_options()  # Populate product options initially

tk.Label(bill_frame, text="Quantity:").grid(row=0, column=2, padx=5, pady=5, sticky="e")
quantity_entry = tk.Entry(bill_frame, width=10)
quantity_entry.grid(row=0, column=3, padx=5, pady=5, sticky="w")

add_to_bill_button = tk.Button(bill_frame, text="Add to Bill", command=add_product_to_bill)
add_to_bill_button.grid(row=0, column=4, padx=10, pady=5)

tk.Label(bill_frame, text="Select Customer:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
customer_dropdown_bill = ttk.Combobox(bill_frame, textvariable=customer_var, width=27)
customer_dropdown_bill.grid(row=1, column=1, padx=5, pady=5, sticky="w")

update_customer_options()  # Populate customer options initially

generate_bill_button = tk.Button(bill_frame, text="Generate Bill", command=generate_bill)
generate_bill_button.grid(row=1, column=2, columnspan=2, padx=10, pady=5)

root.mainloop()

