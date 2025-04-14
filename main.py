import tkinter as tk
from tkinter import ttk

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

ttk.Label(cars_tab, text="Cars CRUD UI").pack(pady=20)
ttk.Label(customers_tab, text="Customers CRUD UI").pack(pady=20)
ttk.Label(salespersons_tab, text="Salespersons CRUD UI").pack(pady=20)
ttk.Label(sales_tab, text="Sales CRUD UI").pack(pady=20)

root.mainloop()
