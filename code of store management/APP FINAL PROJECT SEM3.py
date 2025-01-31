# Importing the required modules
import tkinter
from tkinter import *
from tkinter import ttk
from tkinter import font
from tkinter import messagebox
from tkinter.simpledialog import askstring
import mysql.connector

# Connecting to the database and creating table
db = mysql.connector.connect(user="root", passwd="chetan17012005", host="localhost")

my_cursor = db.cursor()  # getting the cursor object
my_cursor.execute("CREATE DATABASE IF NOT EXISTS Shop")  # creating the database named library

db = mysql.connector.connect(user="root", passwd="chetan17012005", host="localhost", database='Shop')
my_cursor = db.cursor()
# query to create a table products
query = "CREATE TABLE IF NOT EXISTS products (date VARCHAR(10),prodName VARCHAR(20), prodPrice VARCHAR(50))"
my_cursor.execute(query)  # executing the query

db = mysql.connector.connect(user="root", passwd="chetan17012005", host="localhost", database='Shop')
my_cursor = db.cursor()
# query to create a table sale
query = "CREATE TABLE IF NOT EXISTS sale (custName VARCHAR(20), date VARCHAR(10), prodName VARCHAR(30),qty INTEGER, price INTEGER )"
my_cursor.execute(query)  # executing the query


# Function to add the product to the database
def prodtoTable():
    # Getting the user inputs of product details from the user
    pname = prodName.get()
    price = prodPrice.get()
    dt = date.get()
    # Connecting to the database
    db = mysql.connector.connect(user="root", passwd="chetan17012005", host="localhost", database='Shop')
    cursor = db.cursor()

    # query to add the product details to the table
    query = "INSERT INTO products(date,prodName,prodPrice) VALUES(%s,%s,%s)"
    details = (dt, pname, price)

    # Executing the query and showing the pop up message
    try:
        cursor.execute(query, details)
        db.commit()
        messagebox.showinfo('Success', "Product added successfully")
    except Exception as e:
        print("The exception is:", e)
        messagebox.showinfo("Error", "Trouble adding data into Database")

    wn.destroy()


# Function to get details of the product to be added
def addProd():
    global prodName, prodPrice, date, Canvas1, wn

    # Creating the window
    wn = tkinter.Tk()
    wn.title("Welcome to Malasminimart")
    wn.configure(bg='mint cream')
    wn.minsize(width=500, height=500)
    wn.geometry("700x600")

    Canvas1 = Canvas(wn)
    Canvas1.config(bg='LightBlue1')
    Canvas1.pack(expand=True, fill=BOTH)

    headingFrame1 = Frame(wn, bg='LightBlue1', bd=5)
    headingFrame1.place(relx=0.25, rely=0.1, relwidth=0.5, relheight=0.13)
    headingLabel = Label(headingFrame1, text="Add a Product", fg='grey19', font=('Courier', 15, 'bold'))
    headingLabel.place(relx=0, rely=0, relwidth=1, relheight=1)

    labelFrame = Frame(wn)
    labelFrame.place(relx=0.1, rely=0.4, relwidth=0.8, relheight=0.4)

    # Getting Date
    lable1 = Label(labelFrame, text="Date : ", fg='black')
    lable1.place(relx=0.05, rely=0.3, relheight=0.08)

    date = Entry(labelFrame)
    date.place(relx=0.3, rely=0.3, relwidth=0.62, relheight=0.08)

    # Product Name
    lable2 = Label(labelFrame, text="Product Name : ", fg='black')
    lable2.place(relx=0.05, rely=0.45, relheight=0.08)

    prodName = Entry(labelFrame)
    prodName.place(relx=0.3, rely=0.45, relwidth=0.62, relheight=0.08)

    # Product Price
    lable3 = Label(labelFrame, text="Product Price : ", fg='black')
    lable3.place(relx=0.05, rely=0.6, relheight=0.08)

    prodPrice = Entry(labelFrame)
    prodPrice.place(relx=0.3, rely=0.6, relwidth=0.62, relheight=0.08)

    # Add Button
    Btn = Button(wn, text="ADD", bg='#d1ccc0', fg='black', command=prodtoTable)
    Btn.place(relx=0.28, rely=0.85, relwidth=0.18, relheight=0.08)

    Quit = Button(wn, text="Quit", bg='#f7f1e3', fg='black', command=wn.destroy)
    Quit.place(relx=0.53, rely=0.85, relwidth=0.18, relheight=0.08)

    wn.mainloop()


# Function to remove the product from the database
def removeProd():
    # Getting the product name from the user to be removed
    name = prodName.get()
    name = name.lower()

    # Connecting to the database
    db = mysql.connector.connect(user="root", passwd="chetan17012005", host="localhost", database='Shop')
    cursor = db.cursor()

    # Query to delete the respective product from the database
    query = "DELETE from products where LOWER(prodName) = '" + name + "'"
    # Executing the query and showing the message box
    try:
        cursor.execute(query)
        db.commit()
        # cur.execute(deleteIssue)
        # con.commit()

        messagebox.showinfo('Success', "Product Record Deleted Successfully")

    except Exception as e:
        print("The exception is:", e)
        messagebox.showinfo("Please check Product Name")

    wn.destroy()


# Function to get product details from the user to be deleted
def delProd():
    global prodName, Canvas1, wn
    # Creating a window
    wn = tkinter.Tk()
    wn.title("Shop Management System")
    wn.configure(bg='mint cream')
    wn.minsize(width=500, height=500)
    wn.geometry("700x600")

    Canvas1 = Canvas(wn)
    Canvas1.config(bg="misty rose")
    Canvas1.pack(expand=True, fill=BOTH)

    headingFrame1 = Frame(wn, bg="misty rose", bd=5)
    headingFrame1.place(relx=0.25, rely=0.1, relwidth=0.5, relheight=0.13)
    headingLabel = Label(headingFrame1, text="Delete Product", fg='grey19', font=('Courier', 15, 'bold'))
    headingLabel.place(relx=0, rely=0, relwidth=1, relheight=1)

    labelFrame = Frame(wn)
    labelFrame.place(relx=0.1, rely=0.3, relwidth=0.8, relheight=0.5)

    # Product Name to Delete
    lable = Label(labelFrame, text="Product Name : ", fg='black')
    lable.place(relx=0.05, rely=0.5)

    prodName = Entry(labelFrame)
    prodName.place(relx=0.3, rely=0.5, relwidth=0.62)

    # Delete Button
    Btn = Button(wn, text="DELETE", bg='#d1ccc0', fg='black', command=removeProd)
    Btn.place(relx=0.28, rely=0.9, relwidth=0.18, relheight=0.08)

    Quit = Button(wn, text="Quit", bg='#f7f1e3', fg='black', command=wn.destroy)
    Quit.place(relx=0.53, rely=0.9, relwidth=0.18, relheight=0.08)

    wn.mainloop()


# Function to show all the products in the database
def viewProds():
    global wn
    # Creating the window to show the products details
    wn = tkinter.Tk()
    wn.title(" Shop Management System")
    wn.configure(bg='mint cream')
    wn.minsize(width=500, height=500)
    wn.geometry("700x600")

    Canvas1 = Canvas(wn)
    Canvas1.config(bg="old lace")
    Canvas1.pack(expand=True, fill=BOTH)

    headingFrame1 = Frame(wn, bg='old lace', bd=5)
    headingFrame1.place(relx=0.25, rely=0.1, relwidth=0.5, relheight=0.13)

    headingLabel = Label(headingFrame1, text="View Products", fg='black', font=('Courier', 15, 'bold'))
    headingLabel.place(relx=0, rely=0, relwidth=1, relheight=1)

    labelFrame = Frame(wn)
    labelFrame.place(relx=0.1, rely=0.3, relwidth=0.8, relheight=0.5)
    y = 0.25

    # Connecting to database
    db = mysql.connector.connect(user="root", passwd="chetan17012005", host="localhost", database='Shop')
    cursor = db.cursor()
    # query to select all products from the table
    query = 'SELECT * FROM products'

    Label(labelFrame, text="%-50s%-50s%-50s" % ('Date', 'Product', 'Price'), font=('calibri', 11, 'bold'),
          fg='black').place(relx=0.07, rely=0.1)
    Label(labelFrame, text="----------------------------------------------------------------------------",
          fg='black').place(relx=0.05, rely=0.2)
    # Executing the query and showing the products details
    try:
        cursor.execute(query)
        res = cursor.fetchall()

        for i in res:
            Label(labelFrame, text="%-50s%-50s%-50s" % (i[0], i[1], i[2]), fg='black').place(relx=0.07, rely=y)
            y += 0.1
    except Exception as e:
        print("The exception is:", e)
        messagebox.showinfo("Failed to fetch files from database")

    Quit = Button(wn, text="Quit", bg='#f7f1e3', fg='black', command=wn.destroy)
    Quit.place(relx=0.4, rely=0.9, relwidth=0.18, relheight=0.08)

    wn.mainloop()


# Function to generate the bill
def bill():
    cName = custName.get()
    dt = date.get()

    name1_qty = name1.get()
    name2_qty = name2.get()
    name3_qty = name3.get()
    name4_qty = name4.get()

    totalBill = 0

    query = "SELECT * FROM products"
    my_cursor.execute(query)
    res = my_cursor.fetchall()

    # Process product 1
    if name1_qty and name1_qty.isdigit():
        i = res[0]
        qty = int(name1_qty)
        total = qty * int(i[2])
        totalBill += total
        insert_sale_query = "INSERT INTO sale (custName, date, prodName, qty, price) VALUES (%s, %s, %s, %s, %s)"
        sale_details = (cName, dt, i[1], qty, total)
        my_cursor.execute(insert_sale_query, sale_details)

    # Process product 2
    if name2_qty and name2_qty.isdigit():
        i = res[1]
        qty = int(name2_qty)
        total = qty * int(i[2])
        totalBill += total
        insert_sale_query = "INSERT INTO sale (custName, date, prodName, qty, price) VALUES (%s, %s, %s, %s, %s)"
        sale_details = (cName, dt, i[1], qty, total)
        my_cursor.execute(insert_sale_query, sale_details)

    # Process product 3
    if name3_qty and name3_qty.isdigit():
        i = res[2]
        qty = int(name3_qty)
        total = qty * int(i[2])
        totalBill += total
        insert_sale_query = "INSERT INTO sale (custName, date, prodName, qty, price) VALUES (%s, %s, %s, %s, %s)"
        sale_details = (cName, dt, i[1], qty, total)
        my_cursor.execute(insert_sale_query, sale_details)

    if name4_qty and name4_qty.isdigit():
        i = res[2]
        qty = int(name4_qty)
        total = qty * int(i[2])
        totalBill += total
        insert_sale_query = "INSERT INTO sale (custName, date, prodName, qty, price) VALUES (%s, %s, %s, %s, %s)"
        sale_details = (cName, dt, i[1], qty, total)
        my_cursor.execute(insert_sale_query, sale_details)

    db.commit()

    # Display the bill
    bill_text = f" Malas Minimart\nCustomer Name: {cName}\nDate: {dt}\n\n"

    if name1_qty and name1_qty.isdigit():
        bill_text += f"{res[0][1]} x {name1_qty}: {int(res[0][2]) * int(name1_qty)}\n"

    if name2_qty and name2_qty.isdigit():
        bill_text += f"{res[1][1]} x {name2_qty}: {int(res[1][2]) * int(name2_qty)}\n"

    if name3_qty and name3_qty.isdigit():
        bill_text += f"{res[2][1]} x {name3_qty}: {int(res[2][2]) * int(name3_qty)}\n"

    bill_text += f"\nTotal: {totalBill}\n\nThank you for shopping!"

    # Display the bill in a separate window
    bill_window = tkinter.Tk()
    bill_window.title("Bill")
    bill_window.geometry("400x400")

    bill_label = Label(bill_window, text=bill_text)
    bill_label.pack()

    bill_window.mainloop()

# Function to take the inputs form the user to generate bill
def newCust():
    global wn, name1, name2, name3, name4, date, custName
    # Creating a window
    wn = tkinter.Tk()
    wn.title("Shop Management System")
    wn.configure(bg='lavender blush2')
    wn.minsize(width=500, height=500)
    wn.geometry("700x600")
    headingFrame1 = Frame(wn, bg="lavender blush2", bd=5)
    headingFrame1.place(relx=0.2, rely=0.1, relwidth=0.6, relheight=0.16)
    headingLabel = Label(headingFrame1, text="New Customer", fg='grey19', font=('Courier', 15, 'bold'))
    headingLabel.place(relx=0, rely=0, relwidth=1, relheight=1)

    lable1 = Label(wn, text="Date : ", fg='black')
    lable1.place(relx=0.05, rely=0.3, )

    # Getting date
    date = Entry(wn)
    date.place(relx=0.3, rely=0.3, relwidth=0.62)

    lable2 = Label(wn, text="Customer Name : ", fg='black')
    lable2.place(relx=0.05, rely=0.4, )

    # Getting customer name
    custName = Entry(wn)
    custName.place(relx=0.3, rely=0.4, relwidth=0.62)

    labelFrame = Frame(wn)
    labelFrame.place(relx=0.1, rely=0.45, relwidth=0.8, relheight=0.4)

    y = 0.3
    Label(labelFrame, text="Please enter the quantity of the products you want to buy", font=('calibri', 11, 'bold'),
          fg='black').place(relx=0.07, rely=0.1)

    Label(labelFrame, text="%-50s%-50s%-30s" % ('Product', 'Price', 'Quantity'), font=('calibri', 11, 'bold'),
          fg='black').place(relx=0.07, rely=0.2)

    # Connecting to the database
    db = mysql.connector.connect(user="root", passwd="chetan17012005", host="localhost", database='Shop')
    cursor = db.cursor()
    query = 'SELECT * FROM products'
    cursor.execute(query)
    res = cursor.fetchall()
    print(res)
    c = 1

    # Showing all the products and creating entries to take the input of the quantity
    i = res[0]
    Label(labelFrame, text="%-50s%-50s" % (i[1], i[2]), fg='black').place(relx=0.07, rely=y)
    name1 = Entry(labelFrame)
    name1.place(relx=0.6, rely=y, relwidth=0.2)
    y += 0.1
    i = res[1]
    Label(labelFrame, text="%-50s%-50s" % (i[1], i[2]), fg='black').place(relx=0.07, rely=y)
    name2 = Entry(labelFrame)
    name2.place(relx=0.6, rely=y, relwidth=0.2)
    y += 0.1
    i = res[2]
    Label(labelFrame, text="%-50s%-50s" % (i[1], i[2]), fg='black').place(relx=0.07, rely=y)
    name3 = Entry(labelFrame)
    name3.place(relx=0.6, rely=y, relwidth=0.2)
    y += 0.1

    i = res[3]
    Label(labelFrame, text="%-50s%-50s" % (i[1], i[2]), fg='black').place(relx=0.07, rely=y)
    name4 = Entry(labelFrame)
    name4.place(relx=0.6, rely=y, relwidth=0.2)
    y += 0.1

    # Button to generate bill
    Btn = Button(wn, text="Generate Bill", bg='#d1ccc0', fg='black', command=bill)
    Btn.place(relx=0.28, rely=0.9, relwidth=0.18, relheight=0.08)

    Quit = Button(wn, text="Quit", bg='#f7f1e3', fg='black', command=wn.destroy)
    Quit.place(relx=0.55, rely=0.9, relwidth=0.18, relheight=0.08)

    wn.mainloop()

def viewSalesForDay():
    day = askstring("View Sales for Specific Day", "Enter the date (DD/MM/YY):")

    if day:
        # Creating a new window to display the sales for the specified day
        sales_window = tkinter.Tk()
        sales_window.title("Sales for Specific Day")
        sales_window.geometry("1200x800")

        sales_label = Label(sales_window, text=f"Sales for {day}", font=('Courier', 15, 'bold'))
        sales_label.pack()

        # Connecting to the database
        db = mysql.connector.connect(user="root", passwd="chetan17012005", host="localhost", database='Shop')
        cursor = db.cursor()

        # Query to select sales for the specified day
        query = f"SELECT * FROM sale WHERE date = '{day}'"
        cursor.execute(query)
        res = cursor.fetchall()

        if res:
            # Create a table to display sales
            table = ttk.Treeview(sales_window, columns=("Customer Name", "Product Name", "Quantity", "Price"))
            table.heading("#1", text="Customer Name")
            table.heading("#2", text="Product Name")
            table.heading("#3", text="Quantity")
            table.heading("#4", text="Price")

            for sale in res:
                table.insert("", "end", values=(sale[0], sale[2], sale[3], sale[4]))

            table.pack()

        else:
            no_sales_label = Label(sales_window, text="No sales for the specified day.")
            no_sales_label.pack()

        sales_window.mainloop()



# Function to take the inputs form the user to generate bill

# Creating the mail window
wn = tkinter.Tk()
wn.title("Shop Management System")

wn.minsize(width=500, height=500)
wn.geometry("700x600")

headingFrame1 = Frame(wn, bg="snow3", bd=5)
headingFrame1.place(relx=0.2, rely=0.1, relwidth=0.6, relheight=0.16)
headingLabel = Label(headingFrame1, text="Welcome to MALA'S MINIMART", fg='grey19',
                     font=('Courier', 15, 'bold'))
headingLabel.place(relx=0, rely=0, relwidth=1, relheight=1)

# Button to add a new product
btn1 = Button(wn, text="Add a Product", bg='LightBlue1', fg='black', width=20, height=2, command=addProd)
btn1['font'] = font.Font(size=12)
btn1.place(x=270, y=175)

# Button to delete a product
btn2 = Button(wn, text="Delete a Product", bg='misty rose', fg='black', width=20, height=2, command=delProd)
btn2['font'] = font.Font(size=12)
btn2.place(x=270, y=255)

# Button to view all products
btn3 = Button(wn, text="View Products", bg='old lace', fg='black', width=20, height=2, command=viewProds)
btn3['font'] = font.Font(size=12)
btn3.place(x=270, y=335)

# Button to add a new sale and generate bill
btn4 = Button(wn, text="New Customer", bg='lavender blush2', fg='black', width=20, height=2, command=newCust)
btn4['font'] = font.Font(size=12)
btn4.place(x=270, y=415)



# Button to view sales for a specific day
btn5 = Button(wn, text="View Sales for Specific Day", bg='lavender', fg='black', width=20, height=2, command=viewSalesForDay)
btn5['font'] = font.Font(size=12)
btn5.place(x=270, y=500)

wn.mainloop()

