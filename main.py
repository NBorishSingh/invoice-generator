import tkinter as tk
from tkinter import messagebox
from reportlab.pdfgen import canvas
from datetime import datetime

# Main App Class

class InvoiceApp:
    def __init__(self, root):  #Fixed const name
        self.root = root
        self.root.title("INVOICE GENE")

        #these tk.Labels are used to take in the customer information.
        tk.Label(root, text="First Name").grid(row=0, column=0)
        tk.Label(root, text="Last Name").grid(row=0, column=2)
        tk.Label(root, text="Phone").grid(row=1, column=0)
        tk.Label(root, text="Address").grid(row=1, column=2)
        
        #the self allows you to access the class and the tk.Entry is used to generate a single line text input
        self.First_name_entry = tk.Entry(root)
        self.last_name_entry = tk.Entry(root)
        self.phone_entry = tk.Entry(root)
        self.address_entry = tk.Entry(root)
        #The grid here is being used to specify the position where the Customer gives his information
        self.First_name_entry.grid(row=0, column=1)
        self.last_name_entry.grid(row=0, column=3)
        self.address_entry.grid(row=1, column=1)
        self.phone_entry.grid(row=1, column=3)

        # Item Entry the tk.Labels are here used again to present the text on the screen 
        tk.Label(root, text="Item").grid(row=3, column=0)
        tk.Label(root, text="Quantity").grid(row=3, column=1)
        tk.Label(root, text="Price").grid(row=3, column=2)
        # the tk.Entry being used to generate entry box for the input.
        self.item_entry = tk.Entry(root)
        self.qty_entry = tk.Entry(root)
        self.price_entry = tk.Entry(root)
        # the grid specifies where the Entry box is generated
        self.item_entry.grid(row=4, column=0)
        self.qty_entry.grid(row=4, column=1)
        self.price_entry.grid(row=4, column=2)

        self.items = []

        tk.Button(root, text="Add Item", command=self.add_item).grid(row=5, column=3)
        tk.Button(root, text="Generate Invoice", command=self.generate_invoice).grid(row=6, column=1, columnspan=2)

        self.items_listbox = tk.Listbox(root, width=60)
        self.items_listbox.grid(row=7, column=0, columnspan=4, pady=10)

    def add_item(self):
        #we use exceptions and the messagebox from the tkinter library to generate a error box for whenever a error ouccrs
        
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
            if qty < 0 or price < 0:  # Check for negative values in the qty and price box
                raise ValueError("Quantity and Price must be non-negative.")
        except ValueError as e:
            messagebox.showerror("Invalid Input", str(e))
            return

        self.items.append((item, qty, price)) #after the the error checking we append the data
        self.items_listbox.insert(tk.END, f"{item} - {qty} x ${price:.2f}")
        self.item_entry.delete(0, tk.END)
        self.qty_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)
    #this function generate invoice takes the data taken from the user and feeds it to the 
    def generate_invoice(self):
        name = self.First_name_entry.get()
        name2 = self.last_name_entry.get()
        address = self.address_entry.get()
        phone = self.phone_entry.get()
        
        #here we check and make sure that all the variables are filled and none of them are empty. 
        
        if not name or not address or not phone or not name2:
            messagebox.showwarning("Missing Info", "Please fill in all customer details.")
            return

        if not self.items:
            messagebox.showwarning("No Items", "Please add at least one item.")
            return
        
        #here we use canvas to make a pdf for us
        filename = "invoice.pdf"
        pdf = canvas.Canvas(filename)
        pdf.setFont("Helvetica-Bold", 20)
        pdf.drawString(50, 800, "INVOICE")
        pdf.setFont("Helvetica", 10)
        pdf.drawString(50, 785, f"Date: {datetime.now().strftime('%Y-%m-%d')}")

        pdf.drawString(50, 760, f"Customer: {name} {name2}")
        pdf.drawString(50, 745, f"Address: {address}")
        pdf.drawString(50, 730, f"Phone: {phone}")

        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(150, 700, "Item")
        pdf.drawString(250, 700, "Quantity")
        pdf.drawString(350, 700, "Unit Price")
        pdf.drawString(450, 700, "Total")

        y = 680
        subtotal = 0
        pdf.setFont("Helvetica", 10)

        for item, qty, price in self.items:
            total = qty * price
            subtotal += total
            pdf.drawString(150, y, item)
            pdf.drawString(250, y, str(qty))
            pdf.drawString(350, y, f"${price:.2f}")
            pdf.drawString(450, y, f"${total:.2f}")
            y -= 20

        tax = subtotal * 0.18
        total_amount = subtotal + tax

        pdf.drawString(350, y - 20, "Subtotal:")
        pdf.drawString(450, y - 20, f"${subtotal:.2f}")
        pdf.drawString(350, y - 40, "Tax (18%):")
        pdf.drawString(450, y - 40, f"${tax:.2f}")
        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(350, y - 60, "Total:")
        pdf.drawString(450, y - 60, f"${total_amount:.2f}")

        pdf.save() #we save the pdf file in the computer
        messagebox.showinfo("Success", f"Invoice saved as {filename}")

#these are used to run the application.
root = tk.Tk()
app = InvoiceApp(root)
root.mainloop()