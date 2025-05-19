import tkinter as tk
from tkinter import messagebox
from reportlab.pdfgen import canvas
from datetime import datetime

items = []

def add_item():
    if not items:
        messagebox.showwarning("No Items", "Please add at least one item.")
        return
    try:
        item = item_entry.get()
        if not item:
            raise ValueError("Please enter the item name.")
    except ValueError as e:
        messagebox.showerror("Invalid Input", str(e))
        return
    try:
        qty = int(qty_entry.get())
        price = float(price_entry.get())
        if qty < 0 or price < 0:
            raise ValueError("Quantity and Price must be non-negative.")
    except ValueError as e:
        messagebox.showerror("Invalid Input", str(e))
        return

    items.append((item, qty, price))
    items_listbox.insert(tk.END, f"{item} - {qty} x ${price:.2f}")
    item_entry.delete(0, tk.END)
    qty_entry.delete(0, tk.END)
    price_entry.delete(0, tk.END)

def generate_invoice():
    name = first_name_entry.get()
    name2 = last_name_entry.get()
    address = address_entry.get()
    phone = phone_entry.get()

    if not name or not address or not phone or not name2:
        messagebox.showwarning("Missing Info", "Please fill in all customer details.")
        return



    filename = "invoice.pdf"
    pdf = canvas.Canvas(filename)
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(50, 800, "INVOICE")
    pdf.setFont("Helvetica", 10)
    pdf.drawString(50, 785, f"Date: {datetime.now().strftime('%Y-%m-%d')}")

    pdf.drawString(50, 760, f"Customer: {name} {name2}")
    pdf.drawString(50, 745, f"Address: {address}")
    pdf.drawString(50, 730, f"Phone: {phone}")

    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(50, 700, "Item")
    pdf.drawString(250, 700, "Quantity")
    pdf.drawString(350, 700, "Unit Price")
    pdf.drawString(450, 700, "Total")

    y = 680
    subtotal = 0
    pdf.setFont("Helvetica", 10)

    for item, qty, price in items:
        total = qty * price
        subtotal += total
        pdf.drawString(50, y, item)
        pdf.drawString(250, y, str(qty))
        pdf.drawString(350, y, f"${price:.2f}")
        pdf.drawString(450, y, f"${total:.2f}")
        y -= 20

    tax = subtotal * 0.1
    total_amount = subtotal + tax

    pdf.drawString(350, y - 20, "Subtotal:")
    pdf.drawString(450, y - 20, f"${subtotal:.2f}")
    pdf.drawString(350, y - 40, "Tax (10%):")
    pdf.drawString(450, y - 40, f"${tax:.2f}")
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(350, y - 60, "Total:")
    pdf.drawString(450, y - 60, f"${total_amount:.2f}")

    pdf.save()
    messagebox.showinfo("Success", f"Invoice saved as '{filename}'")


# Create the widgets without explicitly naming the root variable;
# Tkinter creates a default root window on first widget creation if none exists.
class InvoiceApp:
    tk.Label(text="First Name").grid(row=0, column=0)
    tk.Label(text="Last Name").grid(row=0, column=2)
    tk.Label(text="Phone").grid(row=1, column=0)
    tk.Label(text="Address").grid(row=1, column=2)

    first_name_entry = tk.Entry()
    last_name_entry = tk.Entry()
    phone_entry = tk.Entry()
    address_entry = tk.Entry()

    first_name_entry.grid(row=0, column=1)
    last_name_entry.grid(row=0, column=3)
    address_entry.grid(row=1, column=1)
    phone_entry.grid(row=1, column=3)

    tk.Label(text="Item").grid(row=3, column=0)
    tk.Label(text="Quantity").grid(row=3, column=1)
    tk.Label(text="Price").grid(row=3, column=2)

    item_entry = tk.Entry()
    qty_entry = tk.Entry()
    price_entry = tk.Entry()

    item_entry.grid(row=4, column=0)
    qty_entry.grid(row=4, column=1)
    price_entry.grid(row=4, column=2)

    tk.Button(text="Add Item", command=add_item).grid(row=5, column=3)
    tk.Button(text="Generate Invoice", command=generate_invoice).grid(row=6, column=1, columnspan=2)

    items_listbox = tk.Listbox(width=60)
    items_listbox.grid(row=7, column=0, columnspan=4, pady=10)

    tk.mainloop()  # Start the Tkinter event loop
