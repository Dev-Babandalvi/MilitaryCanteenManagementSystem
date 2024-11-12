# Military Canteen Management System
# Created by: Baban Ramdas Dalvi
# Institution: Dr. G.Y. Pathrikar College of Computer Science and IT
# Affiliated with MGM University, Chhatrapati Sambhajinagar
# Academic Year: 2024-2025
# Email ID - @babandalvi20@gmail.com
# Contact No - 8308175140
#
# This program is a part of my final year Mini project.

import sys
import sqlite3
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton,
                             QTableWidget, QTableWidgetItem, QMessageBox, QHBoxLayout, QHeaderView, QLabel,



                             QDateEdit)
from PyQt5.QtCore import QDate

class CanteenManagementSystem(QWidget):
    def __init__(self):
        super().__init__()

        self.create_db()  # Ensure the database and tables are created at startup
        self.setWindowTitle("Military Canteen Management System")
        self.setGeometry(300, 300, 600, 600)

        # Set stylesheet for UI enhancements
        self.setStyleSheet("""
            QWidget {
                font-family: Arial;
                font-size: 14px;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)

        # Main layout
        layout = QVBoxLayout()

        # Search bar
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search by Item Name...")
        self.search_bar.textChanged.connect(self.search_items)
        layout.addWidget(self.search_bar)

        # Form layout for adding/editing items
        form_layout = QFormLayout()
        self.item_name_input = QLineEdit()
        self.item_price_input = QLineEdit()
        self.item_stock_input = QLineEdit()

        form_layout.addRow("Item Name:", self.item_name_input)
        form_layout.addRow("Price:", self.item_price_input)
        form_layout.addRow("Stock:", self.item_stock_input)
        layout.addLayout(form_layout)

        # Buttons for add, edit, delete
        button_layout = QHBoxLayout()
        self.add_button = QPushButton("Add Item")
        self.edit_button = QPushButton("Edit Item")
        self.delete_button = QPushButton("Delete Item")

        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.delete_button)

        layout.addLayout(button_layout)

        # Table for displaying items
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Item Name", "Price", "Stock"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.table)

        # Sell Item section
        self.sell_item_label = QLabel("Sell Item")
        layout.addWidget(self.sell_item_label)

        sell_form_layout = QFormLayout()
        self.sell_item_name_input = QLineEdit()
        self.sell_quantity_input = QLineEdit()

        sell_form_layout.addRow("Item Name:", self.sell_item_name_input)
        sell_form_layout.addRow("Quantity:", self.sell_quantity_input)

        self.sell_button = QPushButton("Sell")
        layout.addLayout(sell_form_layout)
        layout.addWidget(self.sell_button)

        # Sales report section
        self.report_label = QLabel("Sales Report")
        layout.addWidget(self.report_label)

        report_form_layout = QFormLayout()
        self.start_date_input = QDateEdit()
        self.end_date_input = QDateEdit()
        self.start_date_input.setDate(QDate.currentDate())
        self.end_date_input.setDate(QDate.currentDate())

        report_form_layout.addRow("Start Date:", self.start_date_input)
        report_form_layout.addRow("End Date:", self.end_date_input)

        self.generate_report_button = QPushButton("Generate Report")
        report_form_layout.addRow(self.generate_report_button)

        layout.addLayout(report_form_layout)

        # Sales history button
        self.view_sales_button = QPushButton("View Sell History")
        layout.addWidget(self.view_sales_button)

        # Sell history table
        self.sales_table = QTableWidget()
        self.sales_table.setColumnCount(4)
        self.sales_table.setHorizontalHeaderLabels(["Item Name", "Quantity", "Total Price", "Date"])
        self.sales_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.sales_table)

        self.setLayout(layout)

        # Connect buttons to their functions
        self.add_button.clicked.connect(self.add_item)
        self.edit_button.clicked.connect(self.edit_item)
        self.delete_button.clicked.connect(self.delete_item)
        self.sell_button.clicked.connect(self.sell_item)
        self.view_sales_button.clicked.connect(self.view_sales_history)
        self.generate_report_button.clicked.connect(self.generate_sales_report)

        # Load items into the table on start
        self.load_items()

        # When a row in the table is clicked, populate the input fields
        self.table.cellClicked.connect(self.populate_fields)

        # Create the sales history table
        self.create_sales_table()

    def create_db(self):
        """Create the database and items table if it doesn't exist."""
        conn = sqlite3.connect('canteen_db.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            price REAL,
            stock INTEGER
        )''')
        conn.commit()
        conn.close()

    def create_sales_table(self):
        """Create a table for recording sales if it doesn't exist."""
        conn = sqlite3.connect('canteen_db.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name TEXT,
            quantity INTEGER,
            total_price REAL,
            sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        conn.commit() 
        conn.close()

    def add_item(self):
        """Add a new item to the database."""
        name = self.item_name_input.text()
        price = self.item_price_input.text()
        stock = self.item_stock_input.text()

        if not name or not price or not stock:
            QMessageBox.warning(self, "Input Error", "Please fill out all fields!")
            return

        try:
            price = float(price)
            stock = int(stock)
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Price must be a number and stock must be an integer!")
            return

        conn = sqlite3.connect('canteen_db.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO items (name, price, stock) VALUES (?, ?, ?)', (name, price, stock))
        conn.commit()
        conn.close()

        QMessageBox.information(self, "Success", "Item added successfully!")
        self.clear_inputs()
        self.load_items()

    def load_items(self):
        """Load all items from the database and display them in the table."""
        conn = sqlite3.connect('canteen_db.db')
        cursor = conn.cursor()
        cursor.execute('SELECT name, price, stock FROM items')
        items = cursor.fetchall()
        self.table.setRowCount(0)
        for row_number, item in enumerate(items):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(item):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        conn.close()

    def search_items(self):
        """Search for items by name and display matching results."""
        search_term = self.search_bar.text().lower()

        conn = sqlite3.connect('canteen_db.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name, price, stock FROM items WHERE LOWER(name) LIKE ?", ('%' + search_term + '%',))
        items = cursor.fetchall()
        self.table.setRowCount(0)
        for row_number, item in enumerate(items):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(item):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        conn.close()

    def sell_item(self):
        """Sell an item by reducing its stock and recording the sale."""
        item_name = self.sell_item_name_input.text().strip()
        quantity = self.sell_quantity_input.text().strip()

        if not item_name or not quantity:
            QMessageBox.warning(self, "Input Error", "Please fill out all fields!")
            return

        try:
            quantity = int(quantity)
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Quantity must be an integer!")
            return

        conn = sqlite3.connect('canteen_db.db')
        cursor = conn.cursor()

        # Check if the item exists and has enough stock (case-insensitive search)
        cursor.execute('SELECT price, stock FROM items WHERE LOWER(name) = LOWER(?)', (item_name,))
        result = cursor.fetchone()
        if result:
            price, stock = result
            if stock >= quantity:
                total_price = price * quantity

                # Deduct the stock and record the sale
                cursor.execute('UPDATE items SET stock = stock - ? WHERE name = ?', (quantity, item_name))
                cursor.execute('INSERT INTO sales (item_name, quantity, total_price) VALUES (?, ?, ?)',
                               (item_name, quantity, total_price))

                conn.commit()
                QMessageBox.information(self, "Success", f"Sold {quantity} of {item_name} for {total_price:.2f}!")
                self.load_items()
                self.clear_sell_inputs()
            else:
                QMessageBox.warning(self, "Stock Error", f"Not enough stock for {item_name}. Available: {stock}")
        else:
            QMessageBox.warning(self, "Item Not Found", f"Item '{item_name}' not found.")

        conn.close()

    def view_sales_history(self):
        """Display the sales history in the sales history table."""
        conn = sqlite3.connect('canteen_db.db')
        cursor = conn.cursor()
        cursor.execute('SELECT item_name, quantity, total_price, sale_date FROM sales ORDER BY sale_date DESC')
        sales = cursor.fetchall()
        self.sales_table.setRowCount(0)
        for row_number, sale in enumerate(sales):
            self.sales_table.insertRow(row_number)
            for column_number, data in enumerate(sale):
                self.sales_table.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        conn.close()

    def generate_sales_report(self):
        """Generate a sales report for the specified date range."""
        start_date = self.start_date_input.date().toString("yyyy-MM-dd")
        end_date = self.end_date_input.date().toString("yyyy-MM-dd")

        conn = sqlite3.connect('canteen_db.db')
        cursor = conn.cursor()
        cursor.execute('SELECT item_name, quantity, total_price, sale_date FROM sales WHERE sale_date BETWEEN ? AND ?',
                       (start_date, end_date))
        report_data = cursor.fetchall()
        conn.close()

        if not report_data:
            QMessageBox.information(self, "Report", "No sales found for the selected date range.")
            return

        report_window = QWidget()
        report_window.setWindowTitle("Sales Report")
        report_layout = QVBoxLayout()
        
        report_table = QTableWidget()
        report_table.setColumnCount(4)
        report_table.setHorizontalHeaderLabels(["Item Name", "Quantity", "Total Price", "Date"])
        report_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        report_table.setRowCount(0)

        for row_number, row_data in enumerate(report_data):
            report_table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                report_table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

        report_layout.addWidget(report_table)
        report_window.setLayout(report_layout)
        report_window.setGeometry(400, 400, 600, 400)
        report_window.show()

    def populate_fields(self, row, column):
        """Populate the input fields with the selected item details from the table."""
        item_name = self.table.item(row, 0).text()
        price = self.table.item(row, 1).text()
        stock = self.table.item(row, 2).text()

        self.item_name_input.setText(item_name)
        self.item_price_input.setText(price)
        self.item_stock_input.setText(stock)

    def clear_inputs(self):
        """Clear the input fields."""
        self.item_name_input.clear()
        self.item_price_input.clear()
        self.item_stock_input.clear()

    def clear_sell_inputs(self):
        """Clear the sell item input fields."""
        self.sell_item_name_input.clear()
        self.sell_quantity_input.clear()

    def edit_item(self):
        """Edit the selected item in the database."""
        item_name = self.item_name_input.text().strip()
        price = self.item_price_input.text().strip()
        stock = self.item_stock_input.text().strip()

        if not item_name or not price or not stock:
            QMessageBox.warning(self, "Input Error", "Please fill out all fields!")
            return

        try:
            price = float(price)
            stock = int(stock)
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Price must be a number and stock must be an integer!")
            return

        conn = sqlite3.connect('canteen_db.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE items SET price = ?, stock = ? WHERE name = ?', (price, stock, item_name))
        conn.commit()
        conn.close()

        QMessageBox.information(self, "Success", "Item updated successfully!")
        self.clear_inputs()
        self.load_items()

    def delete_item(self):
        """Delete the selected item from the database."""
        item_name = self.item_name_input.text().strip()

        if not item_name:
            QMessageBox.warning(self, "Input Error", "Please select an item to delete!")
            return

        conn = sqlite3.connect('canteen_db.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM items WHERE name = ?', (item_name,))
        conn.commit()
        conn.close()

        QMessageBox.information(self, "Success", "Item deleted successfully!")
        self.clear_inputs()
        self.load_items()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CanteenManagementSystem()
    window.show()
    sys.exit(app.exec_())