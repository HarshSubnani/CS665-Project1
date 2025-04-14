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


ttk.Label(customers_tab, text="Customers CRUD UI").pack(pady=20)
ttk.Label(salespersons_tab, text="Salespersons CRUD UI").pack(pady=20)
ttk.Label(sales_tab, text="Sales CRUD UI").pack(pady=20)

root.mainloop()


