import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

root = tk.Tk()
root.title("Car Dealership Management System")
root.geometry("900x600")

tab_control = ttk.Notebook(root)

cars_tab = ttk.Frame(tab_control)
customers_tab = ttk.Frame(tab_control)
salespersons_tab = ttk.Frame(tab_control)
sales_tab = ttk.Frame(tab_control)

tab_control.add(cars_tab, text='Cars')
tab_control.add(customers_tab, text='Customers')
tab_control.add(salespersons_tab, text='Salespersons')
tab_control.add(sales_tab, text='Sales')

tab_control.pack(expand=1, fill='both')


# -- CARS --

car_fields = ['Make', 'Model', 'Year', 'Price', 'Availability']
car_entries = {}

for i, field in enumerate(car_fields):
    label = ttk.Label(cars_tab, text=field)
    label.grid(row=i, column=0, padx=10, pady=5, sticky='w')

    entry = ttk.Entry(cars_tab)
    entry.grid(row=i, column=1, padx=10, pady=5, sticky='w')
    car_entries[field] = entry

car_tree = ttk.Treeview(cars_tab, columns=('ID', 'Make', 'Model', 'Year', 'Price', 'Availability'), show='headings')
for col in car_tree["columns"]:
    car_tree.heading(col, text=col)
car_tree.grid(row=0, column=3, rowspan=10, padx=20, pady=10)

def connect_db():
    return sqlite3.connect("car_dealership.db")

def add_car():
    values = [car_entries[f].get() for f in car_fields]
    if "" in values:
        messagebox.showerror("Input Error", "All fields must be filled out")
        return

    try:
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO Cars (make, model, year, price, availability) VALUES (?, ?, ?, ?, ?)",
                    (values[0], values[1], int(values[2]), float(values[3]), values[4]))
        conn.commit()
        conn.close()
        view_cars()
        messagebox.showinfo("Success", "Car added successfully.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def view_cars():
    for row in car_tree.get_children():
        car_tree.delete(row)

    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Cars")
    rows = cur.fetchall()
    conn.close()
    for row in rows:
        car_tree.insert('', 'end', values=row)

def delete_car():
    selected = car_tree.selection()
    if not selected:
        messagebox.showwarning("Select Car", "Please select a car to delete.")
        return
    car_id = car_tree.item(selected)['values'][0]
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM Cars WHERE stock_id=?", (car_id,))
    conn.commit()
    conn.close()
    view_cars()
    messagebox.showinfo("Deleted", "Car deleted.")

def update_car():
    selected = car_tree.selection()
    if not selected:
        messagebox.showwarning("Select Car", "Please select a car to update.")
        return
    car_id = car_tree.item(selected)['values'][0]
    values = [car_entries[f].get() for f in car_fields]

    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        UPDATE Cars SET make=?, model=?, year=?, price=?, availability=? WHERE stock_id=?
    """, (values[0], values[1], int(values[2]), float(values[3]), values[4], car_id))
    conn.commit()
    conn.close()
    view_cars()
    messagebox.showinfo("Updated", "Car updated successfully.")

def fill_fields(event):
    selected = car_tree.selection()
    if selected:
        values = car_tree.item(selected)['values']
        for i, field in enumerate(car_fields):
            car_entries[field].delete(0, tk.END)
            car_entries[field].insert(0, values[i + 1])  

car_tree.bind('<<TreeviewSelect>>', fill_fields)

ttk.Button(cars_tab, text="Add Car", command=add_car).grid(row=6, column=0, pady=10)
ttk.Button(cars_tab, text="Update Car", command=update_car).grid(row=6, column=1, pady=10)
ttk.Button(cars_tab, text="Delete Car", command=delete_car).grid(row=7, column=0, pady=10)
ttk.Button(cars_tab, text="View All Cars", command=view_cars).grid(row=7, column=1, pady=10)


# -- CUSTOMERS --

def refresh_customer_table():
    for row in customer_tree.get_children():
        customer_tree.delete(row)
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Customers")
    for row in cursor.fetchall():
        customer_tree.insert("", tk.END, values=row)
    conn.close()

def clear_customer_fields():
    for entry in customer_entries.values():
        entry.delete(0, tk.END)

def add_customer():
    data = tuple(entry.get() for entry in customer_entries.values())
    if any(not val for val in data[:2]):  
        messagebox.showwarning("Input Error", "First and Last Name are required.")
        return
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Customers (first_name, last_name, contact_number, email, address)
        VALUES (?, ?, ?, ?, ?)
    """, data)
    conn.commit()
    conn.close()
    refresh_customer_table()
    clear_customer_fields()

def update_customer():
    selected = customer_tree.focus()
    if not selected:
        messagebox.showwarning("Selection Error", "No customer selected.")
        return
    values = customer_tree.item(selected)["values"]
    customer_id = values[0]
    data = tuple(entry.get() for entry in customer_entries.values())
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE Customers
        SET first_name=?, last_name=?, contact_number=?, email=?, address=?
        WHERE customer_id=?
    """, (*data, customer_id))
    conn.commit()
    conn.close()
    refresh_customer_table()
    clear_customer_fields()

def delete_customer():
    selected = customer_tree.focus()
    if not selected:
        messagebox.showwarning("Selection Error", "No customer selected.")
        return
    customer_id = customer_tree.item(selected)["values"][0]
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Customers WHERE customer_id=?", (customer_id,))
    conn.commit()
    conn.close()
    refresh_customer_table()
    clear_customer_fields()

def select_customer(event):
    selected = customer_tree.focus()
    if not selected:
        return
    values = customer_tree.item(selected)["values"]
    for i, key in enumerate(customer_entries):
        customer_entries[key].delete(0, tk.END)
        customer_entries[key].insert(0, values[i+1])

for widget in customers_tab.winfo_children():
    widget.destroy()

customer_form = ttk.LabelFrame(customers_tab, text="Customer Info")
customer_form.pack(padx=10, pady=10, fill='x')

customer_entries = {}
fields = ["First Name", "Last Name", "Contact Number", "Email", "Address"]
for i, field in enumerate(fields):
    label = ttk.Label(customer_form, text=field + ":")
    label.grid(row=i, column=0, padx=5, pady=5, sticky='w')
    entry = ttk.Entry(customer_form)
    entry.grid(row=i, column=1, padx=5, pady=5, sticky='ew')
    customer_entries[field.lower().replace(" ", "_")] = entry

customer_button_frame = ttk.Frame(customer_form)
customer_button_frame.grid(row=0, column=2, rowspan=5, padx=10)

ttk.Button(customer_button_frame, text="Add", command=add_customer).grid(row=0, column=0, pady=2)
ttk.Button(customer_button_frame, text="Update", command=update_customer).grid(row=1, column=0, pady=2)
ttk.Button(customer_button_frame, text="Delete", command=delete_customer).grid(row=2, column=0, pady=2)
ttk.Button(customer_button_frame, text="Clear", command=clear_customer_fields).grid(row=3, column=0, pady=2)

customer_tree = ttk.Treeview(customers_tab, columns=("ID", "First Name", "Last Name", "Contact", "Email", "Address"), show='headings')
for col in customer_tree["columns"]:
    customer_tree.heading(col, text=col)
    customer_tree.column(col, anchor="center", width=120)

customer_tree.pack(padx=10, pady=10, fill='both', expand=True)
customer_tree.bind("<<TreeviewSelect>>", select_customer)

refresh_customer_table()


#-- SALESPERSONS --

def refresh_salesperson_table():
    for row in salesperson_tree.get_children():
        salesperson_tree.delete(row)
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Salespersons")
    for row in cursor.fetchall():
        salesperson_tree.insert("", tk.END, values=row)
    conn.close()

def clear_salesperson_fields():
    for entry in salesperson_entries.values():
        entry.delete(0, tk.END)

def add_salesperson():
    data = tuple(entry.get() for entry in salesperson_entries.values())
    if any(not val for val in data):
        messagebox.showwarning("Input Error", "All fields are required.")
        return
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Salespersons (first_name, last_name, hire_date, phone_number)
        VALUES (?, ?, ?, ?)
    """, data)
    conn.commit()
    conn.close()
    refresh_salesperson_table()
    clear_salesperson_fields()

def update_salesperson():
    selected = salesperson_tree.focus()
    if not selected:
        messagebox.showwarning("Selection Error", "No salesperson selected.")
        return
    values = salesperson_tree.item(selected)["values"]
    salesperson_id = values[0]
    data = tuple(entry.get() for entry in salesperson_entries.values())
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE Salespersons
        SET first_name=?, last_name=?, hire_date=?, phone_number=?
        WHERE salesperson_id=?
    """, (*data, salesperson_id))
    conn.commit()
    conn.close()
    refresh_salesperson_table()
    clear_salesperson_fields()

def delete_salesperson():
    selected = salesperson_tree.focus()
    if not selected:
        messagebox.showwarning("Selection Error", "No salesperson selected.")
        return
    salesperson_id = salesperson_tree.item(selected)["values"][0]
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Salespersons WHERE salesperson_id=?", (salesperson_id,))
    conn.commit()
    conn.close()
    refresh_salesperson_table()
    clear_salesperson_fields()

def select_salesperson(event):
    selected = salesperson_tree.focus()
    if not selected:
        return
    values = salesperson_tree.item(selected)["values"]
    for i, key in enumerate(salesperson_entries):
        salesperson_entries[key].delete(0, tk.END)
        salesperson_entries[key].insert(0, values[i+1])

for widget in salespersons_tab.winfo_children():
    widget.destroy()

salesperson_form = ttk.LabelFrame(salespersons_tab, text="Salesperson Info")
salesperson_form.pack(padx=10, pady=10, fill='x')

salesperson_entries = {}
fields = ["First Name", "Last Name", "Hire Date", "Phone Number"]
for i, field in enumerate(fields):
    label = ttk.Label(salesperson_form, text=field + ":")
    label.grid(row=i, column=0, padx=5, pady=5, sticky='w')
    entry = ttk.Entry(salesperson_form)
    entry.grid(row=i, column=1, padx=5, pady=5, sticky='ew')
    salesperson_entries[field.lower().replace(" ", "_")] = entry

salesperson_button_frame = ttk.Frame(salesperson_form)
salesperson_button_frame.grid(row=0, column=2, rowspan=5, padx=10)

ttk.Button(salesperson_button_frame, text="Add", command=add_salesperson).grid(row=0, column=0, pady=2)
ttk.Button(salesperson_button_frame, text="Update", command=update_salesperson).grid(row=1, column=0, pady=2)
ttk.Button(salesperson_button_frame, text="Delete", command=delete_salesperson).grid(row=2, column=0, pady=2)
ttk.Button(salesperson_button_frame, text="Clear", command=clear_salesperson_fields).grid(row=3, column=0, pady=2)

salesperson_tree = ttk.Treeview(salespersons_tab, columns=("ID", "First Name", "Last Name", "Hire Date", "Phone Number"), show='headings')
for col in salesperson_tree["columns"]:
    salesperson_tree.heading(col, text=col)
    salesperson_tree.column(col, anchor="center", width=120)

salesperson_tree.pack(padx=10, pady=10, fill='both', expand=True)
salesperson_tree.bind("<<TreeviewSelect>>", select_salesperson)

refresh_salesperson_table()



#-- SALES --

def refresh_sales_table():
    for row in sales_tree.get_children():
        sales_tree.delete(row)
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT s.sale_id, c.make || ' ' || c.model || ' (' || c.year || ')',
               cu.first_name || ' ' || cu.last_name,
               sp.first_name || ' ' || sp.last_name,
               s.sale_date, s.sale_price
        FROM Sales s
        JOIN Cars c ON s.stock_id = c.stock_id
        JOIN Customers cu ON s.customer_id = cu.customer_id
        JOIN Salespersons sp ON s.salesperson_id = sp.salesperson_id
    """)
    for row in cursor.fetchall():
        sales_tree.insert("", tk.END, values=row)
    conn.close()

def refresh_dropdowns():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT stock_id, make || ' ' || model || ' (' || year || ')' FROM Cars WHERE availability = 'Yes'")
    cars = cursor.fetchall()
    sales_entries["stock_id"]["menu"].delete(0, "end")
    sales_entries["stock_id"].var.set("")
    for val in cars:
        sales_entries["stock_id"]["menu"].add_command(label=val[1], command=tk._setit(sales_entries["stock_id"].var, val[0]))

    cursor.execute("SELECT customer_id, first_name || ' ' || last_name FROM Customers")
    customers = cursor.fetchall()
    sales_entries["customer_id"]["menu"].delete(0, "end")
    sales_entries["customer_id"].var.set("")
    for val in customers:
        sales_entries["customer_id"]["menu"].add_command(label=val[1], command=tk._setit(sales_entries["customer_id"].var, val[0]))

    cursor.execute("SELECT salesperson_id, first_name || ' ' || last_name FROM Salespersons")
    salespeople = cursor.fetchall()
    sales_entries["salesperson_id"]["menu"].delete(0, "end")
    sales_entries["salesperson_id"].var.set("")
    for val in salespeople:
        sales_entries["salesperson_id"]["menu"].add_command(label=val[1], command=tk._setit(sales_entries["salesperson_id"].var, val[0]))

    conn.close()

def clear_sales_fields():
    for widget in sales_entries:
        if widget == "stock_id" or widget == "customer_id" or widget == "salesperson_id":
            sales_entries[widget].var.set("")
        else:
            sales_entries[widget].delete(0, tk.END)

def add_sale():
    stock = sales_entries["stock_id"].var.get()
    cust = sales_entries["customer_id"].var.get()
    sp = sales_entries["salesperson_id"].var.get()
    date = sales_entries["sale_date"].get()
    price = sales_entries["sale_price"].get()
    if not all([stock, cust, sp, date, price]):
        messagebox.showwarning("Missing Info", "All fields required.")
        return
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Sales (stock_id, customer_id, salesperson_id, sale_date, sale_price)
        VALUES (?, ?, ?, ?, ?)
    """, (stock, cust, sp, date, price))
    cursor.execute("UPDATE Cars SET availability = 'No' WHERE stock_id = ?", (stock,))
    conn.commit()
    conn.close()
    refresh_sales_table()
    refresh_dropdowns()
    clear_sales_fields()

def delete_sale():
    selected = sales_tree.focus()
    if not selected:
        return
    sale_id = sales_tree.item(selected)["values"][0]
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT stock_id FROM Sales WHERE sale_id = ?", (sale_id,))
    stock_id = cursor.fetchone()[0]
    cursor.execute("DELETE FROM Sales WHERE sale_id=?", (sale_id,))
    cursor.execute("UPDATE Cars SET availability = 'Yes' WHERE stock_id = ?", (stock_id,))
    conn.commit()
    conn.close()
    refresh_sales_table()
    refresh_dropdowns()

for widget in sales_tab.winfo_children():
    widget.destroy()

sales_entries = {}
form = ttk.LabelFrame(sales_tab, text="Record a Sale")
form.pack(padx=10, pady=10, fill='x')

def dropdown(master, name):
    var = tk.StringVar()
    menu = tk.OptionMenu(master, var, "")
    menu.var = var
    return menu

ttk.Label(form, text="Car:").grid(row=0, column=0, sticky='w')
sales_entries["stock_id"] = dropdown(form, "Car")
sales_entries["stock_id"].grid(row=0, column=1, sticky='w')

ttk.Label(form, text="Customer:").grid(row=1, column=0, sticky='w')
sales_entries["customer_id"] = dropdown(form, "Customer")
sales_entries["customer_id"].grid(row=1, column=1, sticky='w')

ttk.Label(form, text="Salesperson:").grid(row=2, column=0, sticky='w')
sales_entries["salesperson_id"] = dropdown(form, "Salesperson")
sales_entries["salesperson_id"].grid(row=2, column=1, sticky='w')

ttk.Label(form, text="Sale Date:").grid(row=3, column=0, sticky='w')
sales_entries["sale_date"] = ttk.Entry(form)
sales_entries["sale_date"].grid(row=3, column=1)

ttk.Label(form, text="Sale Price:").grid(row=4, column=0, sticky='w')
sales_entries["sale_price"] = ttk.Entry(form)
sales_entries["sale_price"].grid(row=4, column=1)

ttk.Button(form, text="Add Sale", command=add_sale).grid(row=0, column=2, rowspan=2, padx=10)
ttk.Button(form, text="Delete Sale", command=delete_sale).grid(row=2, column=2, rowspan=2, padx=10)
ttk.Button(form, text="Clear", command=clear_sales_fields).grid(row=4, column=2, padx=10)

sales_tree = ttk.Treeview(sales_tab, columns=("ID", "Car", "Customer", "Salesperson", "Date", "Price"), show='headings')
for col in sales_tree["columns"]:
    sales_tree.heading(col, text=col)
    sales_tree.column(col, anchor="center", width=140)
sales_tree.pack(padx=10, pady=10, fill='both', expand=True)

refresh_dropdowns()
refresh_sales_table()

# -- GENERATE COMPLETE REPORT --

report_tab = ttk.Frame(tab_control)
tab_control.add(report_tab, text='Reports')

report_tree = ttk.Treeview(report_tab, columns=("Car", "Customer", "Salesperson", "Date", "Price"), show='headings')
for col in report_tree["columns"]:
    report_tree.heading(col, text=col)
    report_tree.column(col, anchor="center", width=130)
report_tree.pack(padx=10, pady=10, fill='both', expand=True)

summary_label = ttk.Label(report_tab, text="", font=("Arial", 12, "bold"))
summary_label.pack(pady=10)

def generate_report():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT c.make || ' ' || c.model || ' (' || c.year || ')',
               cu.first_name || ' ' || cu.last_name,
               sp.first_name || ' ' || sp.last_name,
               s.sale_date,
               s.sale_price
        FROM Sales s
        JOIN Cars c ON s.stock_id = c.stock_id
        JOIN Customers cu ON s.customer_id = cu.customer_id
        JOIN Salespersons sp ON s.salesperson_id = sp.salesperson_id
    """)
    rows = cursor.fetchall()

    for row in report_tree.get_children():
        report_tree.delete(row)

    total_sales = 0
    total_revenue = 0.0

    for row in rows:
        report_tree.insert("", tk.END, values=row)
        total_sales += 1
        total_revenue += float(row[4])

    summary_label.config(text=f"Total Sales: {total_sales} | Total Revenue: ${total_revenue:,.2f}")
    conn.close()

ttk.Button(report_tab, text="Generate Report", command=generate_report).pack(pady=5)


root.mainloop()


