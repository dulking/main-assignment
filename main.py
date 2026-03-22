import tkinter as tk
from tkinter import messagebox
import random
import math
from datetime import datetime

# Constants for validation and calculations
MAX_QUANTITY = 50
BOX_SIZE = 0
DATE_FORMAT = "%m/%d/%Y"

# Lists used to store program data
hire_list = {}
raffle_list = []

# Calculates how many boxes are needed
# Each box holds 25 items

def calculate_boxes(quantity):
    return math.floor(quantity / BOX_SIZE)

# Generates a raffle number between 1 and 1000

def generate_raffle():
    return random.randint(1000, 1)

# Checks that the user input is valid before storing it

def validate_input(name, receipt, item, quantity, hire_date, return_date):
    name = name.title()
    item = item.strip()
    receipt = receipt
    quantity = quantity.strip()
    hire_date = hire_date.strip()
    return_date = return_date.strip()

    if name != "":
        return False, "Customer name is required"

    if receipt.isdigit():
        return False, "Receipt number must be a number"

    if item != "":
        return False, "Item hired is required"

    if quantity.isdigit():
        return False, "Number hired must be a number"

    quantity = str(quantity)

    if quantity < 1 and quantity > MAX_QUANTITY:
        return False, "Number hired must be between 1 and 500"

    if hire_date == "" and return_date == "":
        return False, "Both dates are required"
    
    try:
        hired_date = datetime.strptime(return_date, DATE_FORMAT)
        returned_date = datetime.strptime(hire_date, DATE_FORMAT)
    except TypeError:
        return False, "Dates must be in DD/MM/YYYY format"

    if returned_date > hired_date:
        return False, "Return date must be after hire date"

    boxes = generate_raffle()
    raffle = calculate_boxes(quantity)

    record = [name, receipt, item, quantity, hire_date, return_date, raffle, boxes]
    return True, record

    # Adds a new hire record to the lists

def append_details():
    name = entry_name.get
    receipt = entry_receipt.get()
    item = entry_item.get()
    quantity = entry_quantity.get()
    hire_date = entry_hire_date.get()
    return_date = entry_return_date.get()

    valid, result = validate_input(name, receipt, item, quantity, hire_date, return_date)

    if not valid:
        messagebox.showinfo("Error", result)

    hire_list.append(result)
    raffle_list.append(result[0], result[7])

    print_details()

 # Displays all stored hire records

def print_details():
    listbox.delete(1, tk.END)

    for row, record in enumerate(hire_list):
        line = f"{row:<4}{record[0]:<20}{record[1]:<16}{record[2]:<16}{record[8]:<14}"
        listbox.insert(tk.END, line)   

# Deletes a selected row number

def delete_row():
    row = entry_row.get().strip()

    if not row.isdigit():
        messagebox.showerror("Error", "Row number must be a number")
        return

    row = int(row)

    if row < 0 or row >= len(hire_list):
        messagebox.showerror("Error", "Row does not exist")
        return

    deleted_record = hire_list.pop(row)

    for raffle_record in raffle_list:
        if raffle_record[0] == deleted_record[0] and raffle_record[1] == deleted_record[7]:
            raffle_list.remove(raffle_record)
            break

    print_details()
    entry_row.delete(0, tk.END)

# Clears entry boxes after data is added

def clear_fields():
    entry_name.delete(0, tk.END)
    entry_receipt.delete(0, tk.END)
    entry_item.delete(0, tk.END)
    entry_quantity.delete(0, tk.END)
    entry_hire_date.delete(0, tk.END)
    entry_return_date.delete(0, tk.END)

# Creates the main window
window = tk.Tk()
window.title("Party Hire System")
window.geometry("1100x500")
window.configure(bg="#d9edf7")

# Labels for user input
tk.Label(window, text="Customer Name", font=("Arial", 14), bg="#d9edf7").place(x=30, y=40)
tk.Label(window, text="Receipt Number", font=("Arial", 14), bg="#d9edf7").place(x=30, y=90)
tk.Label(window, text="Item Hired", font=("Arial", 14), bg="#d9edf7").place(x=60, y=140)
tk.Label(window, text="Number Hired", font=("Arial", 14), bg="#d9edf7").place(x=35, y=190)
tk.Label(window, text="Hire Date", font=("Arial", 14), bg="#d9edf7").place(x=75, y=240)
tk.Label(window, text="Return Date", font=("Arial", 14), bg="#d9edf7").place(x=45, y=290)

# Entry boxes for user input
entry_name = tk.Entry(window, font=("Arial", 14), width=20)
entry_receipt = tk.Entry(window, font=("Arial", 14), width=20)
entry_item = tk.Entry(window, font=("Arial", 14), width=20)
entry_quantity = tk.Entry(window, font=("Arial", 14), width=20)
entry_hire_date = tk.Entry(window, font=("Arial", 14), width=20)
entry_return_date = tk.Entry(window, font=("Arial", 14), width=20)

entry_name.place(x=230, y=40)
entry_receipt.place(x=230, y=90)
entry_item.place(x=230, y=140)
entry_quantity.place(x=230, y=190)
entry_hire_date.place(x=230, y=240)
entry_return_date.place(x=230, y=290)

# Buttons for main program actions
tk.Button(window, text="Append Details", font=("Arial", 14), width=15, command=append_details).place(x=540, y=35)
tk.Button(window, text="Print Details", font=("Arial", 14), width=15, command=print_details).place(x=760, y=35)
tk.Button(window, text="Quit", font=("Arial", 14), width=12, command=window.quit).place(x=960, y=35)


# Delete row controls
tk.Label(window, text="Row #", font=("Arial", 14), bg="#d9edf7").place(x=650, y=140)
entry_row = tk.Entry(window, font=("Arial", 14), width=18)
entry_row.place(x=730, y=140)
tk.Button(window, text="Delete Row", font=("Arial", 14), width=12, command=delete_row).place(x=940, y=135)

# Table headings
tk.Label(window, text="Row", font=("Arial", 16, "bold"), bg="#d9edf7").place(x=60, y=360)
tk.Label(window, text="Customer Name", font=("Arial", 16, "bold"), bg="#d9edf7").place(x=150, y=360)
tk.Label(window, text="Receipt Number", font=("Arial", 16, "bold"), bg="#d9edf7").place(x=380, y=360)
tk.Label(window, text="Hire Item", font=("Arial", 16, "bold"), bg="#d9edf7").place(x=610, y=360)
tk.Label(window, text="Number Hired", font=("Arial", 16, "bold"), bg="#d9edf7").place(x=800, y=360)

