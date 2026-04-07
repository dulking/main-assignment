import tkinter as tk
from tkinter import messagebox
import random
import math
from datetime import datetime

# ----------------------------------------------------------
# Party Hire System
# This program allows the user to enter customer hire details,
# check that the input is valid, store the details in lists,
# display the stored records in the GUI, and delete a selected
# record. It also calculates how many boxes are needed and
# generates a random raffle number for each customer.
# ----------------------------------------------------------

# ----------------------------------------------------------
# Constants for validation and calculations
# These values stay the same throughout the whole program.
# MAX_QUANTITY is the largest number of items allowed.
# BOX_SIZE is how many items fit into one box.
# DATE_FORMAT is the required format for entered dates.
# ----------------------------------------------------------
MAX_QUANTITY = 500
BOX_SIZE = 25
DATE_FORMAT = "%d/%m/%Y"

# ----------------------------------------------------------
# Lists used to store program data
# hire_list stores the full record for each customer.
# raffle_list stores only the customer name and raffle number.
# ----------------------------------------------------------
hire_list = []
raffle_list = []

# ----------------------------------------------------------
# Calculates how many boxes are needed
# Each box holds 25 items, so math.ceil is used to round up.
# For example, 26 items will need 2 boxes.
# ----------------------------------------------------------
def calculate_boxes(quantity):
   return math.ceil(quantity / BOX_SIZE)

# ----------------------------------------------------------
# Generates a raffle number between 1 and 1000
# This gives each customer a random raffle ticket number.
# ----------------------------------------------------------
def generate_raffle():
    return random.randint(1, 1000)

# ----------------------------------------------------------
# Checks that the user input is valid before storing it
# This function:
# 1. Cleans and formats the input
# 2. Checks for blank fields
# 3. Checks that numbers are really numbers
# 4. Checks that quantity is within the allowed range
# 5. Checks that dates are written correctly
# 6. Checks that the return date is after the hire date
# If everything is valid, it creates and returns a full record.
# If not valid, it returns False and an error message.
# ----------------------------------------------------------
def validate_input(name, receipt, item, quantity, hire_date, return_date):
    # Remove extra spaces and format text neatly
    name = name.strip().title()
    item = item.strip().title()
    receipt = receipt.strip()
    quantity = quantity.strip()
    hire_date = hire_date.strip()
    return_date = return_date.strip()

    # Check that customer name has been entered
    if name == "":
        return False, "Customer name is required"

    # Check that receipt number is numeric
    if not receipt.isdigit():
        return False, "Receipt number must be a number"

    # Check that item hired has been entered
    if item == "":
        return False, "Item hired is required"

    # ----------------------------------------------------------
    # Check that quantity is a valid number
    # Try to convert the input to an integer first
    # This allows negative numbers (e.g. -1) to be recognised as numbers
    # If conversion fails (e.g. letters), show an error
    # ----------------------------------------------------------
    try:
      quantity = int(quantity)
    except ValueError:
     return False, "Number hired must be a number"
    # ----------------------------------------------------------
    # Check that quantity is within the allowed range (1–500)
    # This ensures negative numbers and numbers above 500 are rejected
    # ----------------------------------------------------------
    if quantity < 1 or quantity > MAX_QUANTITY:
     return False, "Number hired must be between 1 and 500"

    # Check that quantity is within the allowed range
    if quantity < 1 or quantity > MAX_QUANTITY:
        return False, "Number hired must be between 1 and 500"

    # Check that both date fields have been entered
    if hire_date == "" or return_date == "":
        return False, "Both dates are required"
    
    # Try to convert the entered dates into real dates
    # If the format is wrong, a ValueError occurs
    try:
        hired_date = datetime.strptime(hire_date, DATE_FORMAT)
        returned_date = datetime.strptime(return_date, DATE_FORMAT)
    except ValueError:
        return False, "Dates must be in DD/MM/YYYY format"

    # Check that the return date is not earlier than the hire date
    if returned_date < hired_date:
        return False, "Return date must be after hire date"

    # Calculate boxes needed and generate raffle number
    boxes = calculate_boxes(quantity)
    raffle = generate_raffle()

    # Create one full record containing all customer data
    record = [name, receipt, item, quantity, hire_date, return_date, boxes, raffle]

    # Return True and the completed record
    return True, record

# ----------------------------------------------------------
# Adds a new hire record to the lists
# This function gets the values from the entry boxes,
# sends them to the validation function, and if valid:
# - adds the full record to hire_list
# - adds the customer name and raffle number to raffle_list
# - updates the listbox display
# - clears the entry fields
# If invalid, it shows an error message and stops.
# ----------------------------------------------------------
def append_details():
    # Get text entered by the user from the GUI entry boxes
    name = entry_name.get()
    receipt = entry_receipt.get()
    item = entry_item.get()
    quantity = entry_quantity.get()
    hire_date = entry_hire_date.get()
    return_date = entry_return_date.get()

    # Check if the entered values are valid
    valid, result = validate_input(name, receipt, item, quantity, hire_date, return_date)

    # If not valid, show an error message and stop the function
    if not valid:
        messagebox.showerror("Error", result)
        return

    # If valid, add the full record to the main hire list
    hire_list.append(result)

    # Add customer name and raffle number to the separate raffle list
    raffle_list.append([result[0], result[7]])

    # Refresh the display and clear the input boxes
    print_details()
    clear_fields()

# ----------------------------------------------------------
# Displays all stored hire records
# This function clears the listbox first, then loops through
# all records in hire_list and displays selected fields in a
# neatly spaced format.
# ----------------------------------------------------------
def print_details():
    # Clear all old items from the listbox before reprinting
    listbox.delete(0, tk.END)

    # Go through each record in hire_list
    for row, record in enumerate(hire_list):
        # Create a formatted line showing row number, name,
        # receipt number, item hired, and quantity
        line = f"{row:<4}{record[0]:<20}{record[1]:<16}{record[2]:<16}{record[3]:<14}"
        
        # Insert the formatted line into the listbox
        listbox.insert(tk.END, line)   

# ----------------------------------------------------------
# Deletes a selected row number
# This function:
# 1. Gets the row number entered by the user
# 2. Checks that the row number is numeric
# 3. Checks that the row actually exists
# 4. Removes the record from hire_list
# 5. Removes the matching raffle entry from raffle_list
# 6. Refreshes the display
# ----------------------------------------------------------
def delete_row():
    # Get the row number entered by the user
    row = entry_row.get().strip()

    # Check that the row number is numeric
    if not row.isdigit():
        messagebox.showerror("Error", "Row number must be a number")
        return

    # Convert row from text to integer
    row = int(row)

    # Check that the row number exists in the list
    if row < 0 or row >= len(hire_list):
        messagebox.showerror("Error", "Row does not exist")
        return

    # Remove the selected record from the hire list
    deleted_record = hire_list.pop(row)

    # Find and remove the matching raffle record
    for raffle_record in raffle_list:
        if raffle_record[0] == deleted_record[0] and raffle_record[1] == deleted_record[7]:
            raffle_list.remove(raffle_record)
            break

    # Refresh the display and clear the delete row entry box
    print_details()
    entry_row.delete(0, tk.END)

# ----------------------------------------------------------
# Clears entry boxes after data is added
# This makes the program easier to use because the user can
# enter a new record without manually deleting the old text.
# ----------------------------------------------------------
def clear_fields():
    entry_name.delete(0, tk.END)
    entry_receipt.delete(0, tk.END)
    entry_item.delete(0, tk.END)
    entry_quantity.delete(0, tk.END)
    entry_hire_date.delete(0, tk.END)
    entry_return_date.delete(0, tk.END)

# ----------------------------------------------------------
# Creates the main window
# This sets up the main GUI window title, size, and colour.
# ----------------------------------------------------------
window = tk.Tk()
window.title("Party Hire System")
window.geometry("1100x500")
window.configure(bg="#d9edf7")

# ----------------------------------------------------------
# Labels for user input
# These labels tell the user what information to type into
# each entry box.
# ----------------------------------------------------------
tk.Label(window, text="Customer Name", font=("Arial", 14), bg="#81d2fb").place(x=30, y=40)
tk.Label(window, text="Receipt Number", font=("Arial", 14), bg="#7bd2fe").place(x=30, y=90)
tk.Label(window, text="Item Hired", font=("Arial", 14), bg="#82d3fc").place(x=60, y=140)
tk.Label(window, text="Number Hired", font=("Arial", 14), bg="#74d0fd").place(x=35, y=190)
tk.Label(window, text="Hire Date", font=("Arial", 14), bg="#71d0ff").place(x=75, y=240)
tk.Label(window, text="Return Date", font=("Arial", 14), bg="#7fcdf5").place(x=45, y=290)

# ----------------------------------------------------------
# Entry boxes for user input
# These are the text boxes where the user types the customer
# details needed by the program.
# ----------------------------------------------------------
entry_name = tk.Entry(window, font=("Arial", 14), width=20)
entry_receipt = tk.Entry(window, font=("Arial", 14), width=20)
entry_item = tk.Entry(window, font=("Arial", 14), width=20)
entry_quantity = tk.Entry(window, font=("Arial", 14), width=20)
entry_hire_date = tk.Entry(window, font=("Arial", 14), width=20)
entry_return_date = tk.Entry(window, font=("Arial", 14), width=20)

# ----------------------------------------------------------
# Positions of the entry boxes
# The place() function is used to position each entry widget
# in the correct area of the GUI window.
# ----------------------------------------------------------
entry_name.place(x=230, y=40)
entry_receipt.place(x=230, y=90)
entry_item.place(x=230, y=140)
entry_quantity.place(x=230, y=190)
entry_hire_date.place(x=230, y=240)
entry_return_date.place(x=230, y=290)

# ----------------------------------------------------------
# Buttons for main program actions
# Append Details adds a record
# Print Details shows all current records
# Quit closes the program
# ----------------------------------------------------------
tk.Button(window, text="Append Details", font=("Arial", 14), width=15, command=append_details).place(x=540, y=35)
tk.Button(window, text="Print Details", font=("Arial", 14), width=15, command=print_details).place(x=760, y=35)
tk.Button(window, text="Quit", font=("Arial", 14), width=12, command=window.quit).place(x=960, y=35)

# ----------------------------------------------------------
# Delete row controls
# This label, entry box, and button allow the user to type a
# row number and remove that record from the program.
# ----------------------------------------------------------
tk.Label(window, text="Row #", font=("Arial", 14), bg="#d9edf7").place(x=650, y=140)
entry_row = tk.Entry(window, font=("Arial", 14), width=18)
entry_row.place(x=730, y=140)
tk.Button(window, text="Delete Row", font=("Arial", 14), width=12, command=delete_row).place(x=940, y=135)

# ----------------------------------------------------------
# Table headings
# These labels act like column headings for the displayed
# output shown in the listbox below.
# ----------------------------------------------------------
tk.Label(window, text="Row", font=("Arial", 16, "bold"), bg="#d9edf7").place(x=60, y=360)
tk.Label(window, text="Customer Name", font=("Arial", 16, "bold"), bg="#d9edf7").place(x=150, y=360)
tk.Label(window, text="Receipt Number", font=("Arial", 16, "bold"), bg="#d9edf7").place(x=380, y=360)
tk.Label(window, text="Hire Item", font=("Arial", 16, "bold"), bg="#d9edf7").place(x=610, y=360)
tk.Label(window, text="Number Hired", font=("Arial", 16, "bold"), bg="#d9edf7").place(x=800, y=360)

# ----------------------------------------------------------
# Listbox used to display the records
# This is where the stored records are shown to the user.
# ----------------------------------------------------------
listbox = tk.Listbox(window, font=("Courier New", 14), width=110, height=6)
listbox.place(x=40, y=400)

# ----------------------------------------------------------
# Starts the program loop
# This keeps the window open and waiting for user actions.
# ----------------------------------------------------------
window.mainloop()