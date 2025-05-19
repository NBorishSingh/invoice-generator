import tkinter as tk
from tkinter import messagebox
from reportlab.pdfgen import canvas
from datetime import datetime

# Main App Class
class InvoiceApp:
    def __init__(self, root):  #Fixed const name
        self.root = root
        self.root.title("Invoice Generator")

        #these tk.Labels are used to take in the customer information.
        tk.Label(root, text="First Name").grid(row=0, column=0)
        tk.Label(root, text="Last Name").grid(row=0, column=2)
        tk.Label(root, text="Phone").grid(row=1, column=0)
        tk.Label(root, text="Address").grid(row=1, column=2)
        
        #the self allows you to access the class and the tk.Entry is used to get a text input box
        self.First_name_entry = tk.Entry(root)
        self.last_name_entry = tk.Entry(root)
        self.phone_entry = tk.Entry(root)
        self.address_entry = tk.Entry(root)

        self.First_name_entry.grid(row=0, column=1)
        self.last_name_entry.grid(row=0, column=3)
        self.address_entry.grid(row=1, column=1)
        self.phone_entry.grid(row=1, column=3)

        # Item Entry
        tk.Label(root, text="Item").grid(row=3, column=0)
        tk.Label(root, text="Quantity").grid(row=3, column=1)
        tk.Label(root, text="Price").grid(row=3, column=2)

        self.item_entry = tk.Entry(root)
        self.qty_entry = tk.Entry(root)
        self.price_entry = tk.Entry(root)

        self.item_entry.grid(row=4, column=0)
        self.qty_entry.grid(row=4, column=1)
        self.price_entry.grid(row=4, column=2)

        self.items = []

        tk.Button(root, text="Add Item", command=self.add_item).grid(row=5, column=3)
        tk.Button(root, text="Generate Invoice", command=self.generate_invoice).grid(row=6, column=1, columnspan=2)

        self.items_listbox = tk.Listbox(root, width=60)
        self.items_listbox.grid(row=7, column=0, columnspan=4, pady=10)

    def add_item(self):
        if not self.items:
            messagebox.showwarning("No Items", "Please add at least one item.")
            return
        try:
            item = self.item_entry.get()
            if not item:
                raise ValueError("Please enter the item name.")
        except ValueError as e:
            messagebox.showerror("Invalid Input", str(e))
            return
        item = self.item_entry.get()
        try:
            qty = int(self.qty_entry.get())
            price = float(self.price_entry.get())
            if qty < 0 or price < 0:  # Check for negative values
                raise ValueError("Quantity and Price must be non-negative.")
        except ValueError as e:
            messagebox.showerror("Invalid Input", str(e))
            return

        self.items.append((item, qty, price))
        self.items_listbox.insert(tk.END, f"{item} - {qty} x ${price:.2f}")
        self.item_entry.delete(0, tk.END)
        self.qty_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)

    def generate_invoice(self):
        name = self.First_name_entry.get()
        name2 = self.last_name_entry.get()
        address = self.address_entry.get()
        phone = self.phone_entry.get()

        if not name or not address or not phone or not name2:
            messagebox.showwarning("Missing Info", "Please fill in all customer details.")
            return

        if not self.items:
            messagebox.showwarning("No Items", "Please add at least one item.")
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

        for item, qty, price in self.items:
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

# Run the app
root = tk.Tk()
app = InvoiceApp(root)
root.mainloop()