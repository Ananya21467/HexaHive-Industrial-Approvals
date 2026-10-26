import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import os

# ---------------- DATABASE ----------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "stockify.db")


def connect_db():
    return sqlite3.connect(DB_PATH)


def create_table():
    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            product_id TEXT PRIMARY KEY,
            product_name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            quantity INTEGER NOT NULL
        )
    """)

    connection.commit()
    connection.close()


# ---------------- APPLICATION ----------------

class StockifyApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Stockify - Product Management System")
        self.root.geometry("850x650")
        self.root.configure(bg="#eef2f7")

        self.product_id = None
        self.show_login()

    # ---------------- COMMON FUNCTIONS ----------------

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_header(self, subtitle):
        header = tk.Frame(self.root, bg="#243b53")
        header.pack(fill="x")

        tk.Label(
            header,
            text="STOCKIFY",
            font=("Arial", 25, "bold"),
            bg="#243b53",
            fg="white"
        ).pack(pady=(15, 3))

        tk.Label(
            header,
            text=subtitle,
            font=("Arial", 12),
            bg="#243b53",
            fg="white"
        ).pack(pady=(0, 15))

    def create_button(self, parent, text, command):
        return tk.Button(
            parent,
            text=text,
            command=command,
            font=("Arial", 11, "bold"),
            bg="white",
            fg="black",
            activebackground="#d9e2ec",
            cursor="hand2",
            padx=12,
            pady=7
        )

    def create_entry(self, parent, **kwargs):
        """Create an input field with a visible focus border."""
        options = {
            "font": ("Arial", 11),
            "bg": "white",
            "fg": "black",
            "relief": "solid",
            "bd": 1,
            "highlightthickness": 2,
            "highlightbackground": "#cccccc",
            "highlightcolor": "#243b53"
        }
        options.update(kwargs)
        return tk.Entry(parent, **options)

    def parse_price(self, value):
        value = value.strip().replace(",", "").replace("₹", "").strip()
        price = float(value)

        if price < 0:
            raise ValueError("Price cannot be negative.")

        return price

    def parse_quantity(self, value):
        quantity = int(value.strip())

        if quantity < 0:
            raise ValueError("Quantity cannot be negative.")

        return quantity

    # ---------------- LOGIN ----------------

    def show_login(self):
        self.clear_window()
        self.root.geometry("420x500")
        self.create_header("Product Management System")

        form = tk.Frame(self.root, bg="white", padx=30, pady=25)
        form.pack(fill="x", padx=35, pady=30)

        tk.Label(
            form,
            text="Login",
            font=("Arial", 20, "bold"),
            bg="white",
            fg="#243b53"
        ).pack(pady=(0, 20))

        tk.Label(
            form, text="Username", bg="white", fg="black"
        ).pack(anchor="w")

        self.username_entry = self.create_entry(form)
        self.username_entry.pack(fill="x", pady=(5, 15))

        tk.Label(
            form, text="Password", bg="white", fg="black"
        ).pack(anchor="w")

        self.password_entry = self.create_entry(form, show="*")
        self.password_entry.pack(fill="x", pady=(5, 20))

        self.create_button(
            form, "Login", self.login
        ).pack(pady=5)

        self.password_entry.bind(
            "<Return>", lambda event: self.login()
        )

        self.username_entry.focus_set()

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get()

        if username == "s_ify" and password == "stock3456":
            self.show_dashboard()
        else:
            messagebox.showerror(
                "Login Failed",
                "Invalid username or password!"
            )

    # ---------------- DASHBOARD ----------------

    def show_dashboard(self):
        self.clear_window()
        self.root.geometry("600x600")
        self.create_header("Product Management System")

        tk.Label(
            self.root,
            text="Welcome to Stockify!",
            font=("Arial", 19, "bold"),
            bg="#eef2f7",
            fg="#243b53"
        ).pack(pady=25)

        tk.Label(
            self.root,
            text="Manage your products easily",
            font=("Arial", 11),
            bg="#eef2f7",
            fg="black"
        ).pack(pady=(0, 15))

        buttons = [
            ("Add Product", self.show_add_product),
            ("View Products", self.show_view_products),
            ("Update Product", self.show_update_product),
            ("Delete Product", self.show_delete_product),
            ("Logout", self.show_login)
        ]

        for text, command in buttons:
            self.create_button(
                self.root, text, command
            ).pack(pady=7, ipadx=35)

    # ---------------- ADD PRODUCT ----------------

    def show_add_product(self):
        self.clear_window()
        self.root.geometry("600x650")
        self.create_header("Add New Product")

        form = tk.Frame(self.root, bg="white", padx=25, pady=20)
        form.pack(fill="x", padx=35, pady=15)

        self.add_entries = {}

        fields = [
            ("Product ID", "product_id"),
            ("Product Name", "product_name"),
            ("Category", "category"),
            ("Price", "price"),
            ("Quantity", "quantity")
        ]

        for label_text, key in fields:
            tk.Label(
                form,
                text=label_text,
                font=("Arial", 11),
                bg="white",
                fg="black"
            ).pack(anchor="w", pady=(4, 0))

            entry = self.create_entry(form)
            entry.pack(fill="x", pady=(3, 6))
            self.add_entries[key] = entry

        self.create_button(
            form, "Save Product", self.add_product
        ).pack(pady=10)

        self.create_button(
            self.root, "Back to Dashboard", self.show_dashboard
        ).pack(pady=5)

    def add_product(self):
        values = {
            key: entry.get().strip()
            for key, entry in self.add_entries.items()
        }

        if any(not value for value in values.values()):
            messagebox.showerror(
                "Error", "Please fill in all fields."
            )
            return

        try:
            price = self.parse_price(values["price"])
            quantity = self.parse_quantity(values["quantity"])
        except ValueError:
            messagebox.showerror(
                "Invalid Input",
                "Enter a valid non-negative price and whole-number quantity."
            )
            return

        connection = connect_db()

        try:
            connection.execute("""
                INSERT INTO products
                (product_id, product_name, category, price, quantity)
                VALUES (?, ?, ?, ?, ?)
            """, (
                values["product_id"],
                values["product_name"],
                values["category"],
                price,
                quantity
            ))

            connection.commit()

            messagebox.showinfo(
                "Success", "Product added successfully!"
            )
            self.show_add_product()

        except sqlite3.IntegrityError:
            messagebox.showerror(
                "Error", "This Product ID already exists!"
            )

        except sqlite3.Error as error:
            messagebox.showerror("Database Error", str(error))

        finally:
            connection.close()

    # ---------------- VIEW PRODUCTS ----------------

    def show_view_products(self):
        self.clear_window()
        self.root.geometry("850x600")
        self.create_header("View Products")

        search_frame = tk.Frame(self.root, bg="#eef2f7")
        search_frame.pack(fill="x", padx=15, pady=15)

        tk.Label(
            search_frame,
            text="Search:",
            bg="#eef2f7",
            fg="black"
        ).pack(side="left", padx=5)

        self.search_entry = self.create_entry(search_frame)
        self.search_entry.pack(
            side="left", padx=5, fill="x", expand=True
        )

        self.create_button(
            search_frame, "Search", self.load_products
        ).pack(side="left", padx=5)

        self.create_button(
            search_frame, "Show All", self.show_all_products
        ).pack(side="left", padx=5)

        table_frame = tk.Frame(self.root)
        table_frame.pack(
            fill="both", expand=True, padx=15, pady=5
        )

        columns = (
            "ID", "Name", "Category", "Price", "Quantity"
        )

        self.tree = ttk.Treeview(
            table_frame, columns=columns, show="headings"
        )

        for column in columns:
            self.tree.heading(column, text=column)
            self.tree.column(
                column, width=120, anchor="center"
            )

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.tree.yview
        )

        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.count_label = tk.Label(
            self.root,
            text="",
            bg="#eef2f7",
            fg="black"
        )
        self.count_label.pack(pady=5)

        self.create_button(
            self.root, "Back to Dashboard", self.show_dashboard
        ).pack(pady=10)

        self.load_products()

    def load_products(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        search = self.search_entry.get().strip()
        connection = connect_db()

        try:
            cursor = connection.cursor()

            if search:
                cursor.execute("""
                    SELECT * FROM products
                    WHERE product_id LIKE ?
                       OR product_name LIKE ?
                       OR category LIKE ?
                    ORDER BY product_id
                """, (
                    f"%{search}%",
                    f"%{search}%",
                    f"%{search}%"
                ))
            else:
                cursor.execute(
                    "SELECT * FROM products ORDER BY product_id"
                )

            products = cursor.fetchall()

            for product in products:
                self.tree.insert("", "end", values=product)

            self.count_label.config(
                text=f"Total products displayed: {len(products)}"
            )

        except sqlite3.Error as error:
            messagebox.showerror("Database Error", str(error))

        finally:
            connection.close()

    def show_all_products(self):
        self.search_entry.delete(0, tk.END)
        self.load_products()

    # ---------------- FIND PRODUCT ----------------

    def find_product(self, product_id):
        connection = connect_db()

        try:
            cursor = connection.cursor()
            cursor.execute(
                "SELECT * FROM products WHERE product_id = ?",
                (product_id,)
            )
            return cursor.fetchone()

        finally:
            connection.close()

    # ---------------- UPDATE PRODUCT ----------------

    def show_update_product(self):
        self.clear_window()
        self.root.geometry("600x650")
        self.create_header("Update Product")

        form = tk.Frame(self.root, bg="white", padx=25, pady=20)
        form.pack(fill="x", padx=35, pady=15)

        tk.Label(
            form,
            text="Enter Product ID",
            bg="white",
            fg="black"
        ).pack(anchor="w")

        self.update_id_entry = self.create_entry(form)
        self.update_id_entry.pack(fill="x", pady=5)

        self.create_button(
            form, "Find Product", self.find_for_update
        ).pack(pady=8)

        self.update_entries = {}

        fields = [
            ("Product Name", "name"),
            ("Category", "category"),
            ("Price", "price"),
            ("Quantity", "quantity")
        ]

        for label_text, key in fields:
            tk.Label(
                form,
                text=label_text,
                bg="white",
                fg="black"
            ).pack(anchor="w", pady=(4, 0))

            entry = self.create_entry(form)
            entry.pack(fill="x", pady=3)
            self.update_entries[key] = entry

        self.create_button(
            form, "Save Changes", self.update_product
        ).pack(pady=10)

        self.create_button(
            self.root, "Back to Dashboard", self.show_dashboard
        ).pack(pady=5)

    def find_for_update(self):
        product_id = self.update_id_entry.get().strip()

        if not product_id:
            messagebox.showerror("Error", "Enter a Product ID.")
            return

        product = self.find_product(product_id)

        if not product:
            self.product_id = None
            messagebox.showerror("Not Found", "Product not found.")
            return

        self.product_id = product_id

        values = {
            "name": product[1],
            "category": product[2],
            "price": str(product[3]),
            "quantity": str(product[4])
        }

        for key, value in values.items():
            entry = self.update_entries[key]
            entry.delete(0, tk.END)
            entry.insert(0, value)

    def update_product(self):
        if not self.product_id:
            messagebox.showerror(
                "Error", "Find a product before updating it."
            )
            return

        values = {
            key: entry.get().strip()
            for key, entry in self.update_entries.items()
        }

        if any(not value for value in values.values()):
            messagebox.showerror(
                "Error", "Please fill in all fields."
            )
            return

        try:
            price = self.parse_price(values["price"])
            quantity = self.parse_quantity(values["quantity"])
        except ValueError:
            messagebox.showerror(
                "Invalid Input",
                "Enter a valid non-negative price and whole-number quantity."
            )
            return

        connection = connect_db()

        try:
            cursor = connection.cursor()
            cursor.execute("""
                UPDATE products
                SET product_name = ?,
                    category = ?,
                    price = ?,
                    quantity = ?
                WHERE product_id = ?
            """, (
                values["name"],
                values["category"],
                price,
                quantity,
                self.product_id
            ))

            connection.commit()

            if cursor.rowcount > 0:
                messagebox.showinfo(
                    "Success", "Product updated successfully!"
                )
                self.product_id = None
                self.show_dashboard()
            else:
                messagebox.showerror(
                    "Error", "Product not found."
                )

        except sqlite3.Error as error:
            messagebox.showerror("Database Error", str(error))

        finally:
            connection.close()

    # ---------------- DELETE PRODUCT ----------------

    def show_delete_product(self):
        self.clear_window()
        self.root.geometry("600x450")
        self.create_header("Delete Product")

        form = tk.Frame(self.root, bg="white", padx=25, pady=25)
        form.pack(fill="x", padx=35, pady=30)

        tk.Label(
            form,
            text="Enter Product ID to Delete",
            font=("Arial", 12, "bold"),
            bg="white",
            fg="black"
        ).pack(anchor="w", pady=5)

        self.delete_id_entry = self.create_entry(form)
        self.delete_id_entry.pack(fill="x", pady=10)

        self.create_button(
            form, "Delete Product", self.delete_product
        ).pack(pady=10)

        self.create_button(
            self.root, "Back to Dashboard", self.show_dashboard
        ).pack(pady=10)

    def delete_product(self):
        product_id = self.delete_id_entry.get().strip()

        if not product_id:
            messagebox.showerror("Error", "Enter a Product ID.")
            return

        product = self.find_product(product_id)

        if not product:
            messagebox.showerror(
                "Not Found", "No product found with this ID."
            )
            return

        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Delete product '{product[1]}'?"
        )

        if not confirm:
            return

        connection = connect_db()

        try:
            cursor = connection.cursor()
            cursor.execute(
                "DELETE FROM products WHERE product_id = ?",
                (product_id,)
            )
            connection.commit()

            if cursor.rowcount > 0:
                messagebox.showinfo(
                    "Success", "Product deleted successfully!"
                )
                self.delete_id_entry.delete(0, tk.END)

        except sqlite3.Error as error:
            messagebox.showerror("Database Error", str(error))

        finally:
            connection.close()


# ---------------- START APPLICATION ----------------

if __name__ == "__main__":
    create_table()

    root = tk.Tk()
    app = StockifyApp(root)
    root.mainloop()
