import sqlite3
import tkinter as tk
from tkinter import ttk
import datetime

# Global variables
(CONNECTION, CURSOR, ROOT, ENTRY_NAME, ENTRY_QUANTITY, ENTRY_UNITY, ENTRY_EXPIRATION_DATE, FOOD_TYPE_COMBOBOX,
 FOOD_STORAGE_TREE) = (None, None, None, None, None, None, None, None, None)


def database_connection():
    """
    Connect to the database and create tables if they do not exist.
    The table schema is as follows:
    - food_storage: id, name, quantity, unit, food_type_id, expiration_date, created_at, updated_at
    - food_type: id, name, created_at, updated_at

    :return: connection, cursor
    """
    connection = sqlite3.connect('food_storage.db')
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS food_type (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS food_storage (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        quantity REAL NOT NULL,
        unit TEXT NOT NULL,
        food_type_id INTEGER NOT NULL,
        expiration_date TEXT,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL,
        FOREIGN KEY (food_type_id) REFERENCES food_type (id)
    )
    """)
    return connection, cursor


def seed_food_types(cursor):
    """
    Seed the food_type table with initial data.

    :param cursor: sqlite3.Cursor
    :return: None
    """
    food_types = [
        ('Fruit',),
        ('Vegetable',),
        ('Grain',),
        ('Protein',),
        ('Dairy',),
        ('Beverage',),
        ('Snack',),
        ('Condiment',),
        ('Frozen',),
        ('Canned',),
        ('Baking',),
        ('Spice',),
        ('Other',)
    ]

    for food_type in food_types:
        create_food_type(cursor, food_type[0])


def create_food_type(cursor, name):
    """
    Create a new food type in the database.

    :param cursor: sqlite3.Cursor
    :param name: str

    :return: dict
    """
    if not name:
        return "A food type name cannot be empty."

    cursor.execute("SELECT * FROM food_type WHERE name = ?", (name,))
    existing_food_type = cursor.fetchone()
    if existing_food_type is not None:
        return "A food type with this name already exists."

    created_at = datetime.datetime.now()
    updated_at = datetime.datetime.now()

    cursor.execute("""
    INSERT INTO food_type (name, created_at, updated_at)
    VALUES (?, ?, ?)
    """, (name, created_at, updated_at))

    cursor.execute("SELECT * FROM food_type WHERE id = ?", (cursor.lastrowid,))
    new_food_type = cursor.fetchone()

    return {
        "id": new_food_type[0],
        "name": new_food_type[1],
        "created_at": new_food_type[2],
        "updated_at": new_food_type[3]
    }


def read_all_food_types(cursor):
    """
    Retrieve all food types from the database.

    :param cursor: sqlite3.Cursor

    Returns (list):
    list of dictionaries
        - Each dictionary contains the following
            - id: int
            - name: str
            - created_at: str
            - updated_at: str
    """
    cursor.execute("""
    SELECT * FROM food_type
    """)

    all_food_types = []

    for food_type in cursor.fetchall():
        all_food_types.append({
            "id": food_type[0],
            "name": food_type[1],
            "created_at": food_type[2],
            "updated_at": food_type[3]
        })

    return all_food_types


def read_food_type_by_id(cursor, food_storage_id):
    """
    Retrieve a food type by id from the database.

    :param cursor: sqlite3.Cursor
    :param food_storage_id: int

    Returns (dict):
        - id: int
        - name: str
        - created_at: str
        - updated_at: str
    """
    cursor.execute("""
    SELECT * FROM food_type
    WHERE id = ?
    """, (food_storage_id,))
    food_type = cursor.fetchone()

    if food_type is None:
        return None

    return {
        "id": food_type[0],
        "name": food_type[1],
        "created_at": food_type[2],
        "updated_at": food_type[3]
    }


def update_food_type_by_id(cursor, food_storage_id, name):
    """
    Update a food type by id in the database.

    :param cursor: sqlite3.Cursor
    :param food_storage_id: int
    :param name: str

    Returns (dict):
        - id: int
        - name: str
        - created_at: str
        - updated_at: str
    """
    existing_food_type = read_food_type_by_id(cursor, food_storage_id)
    if existing_food_type is None:
        return "A food type with this id does not exist."

    cursor.execute("SELECT * FROM food_type WHERE name = ?", (name,))
    existing_food_type_name = cursor.fetchone()
    if existing_food_type_name is not None:
        return "A food type with this name already exists."

    updated_at = datetime.datetime.now()

    cursor.execute("""
    UPDATE food_type
    SET name = ?, updated_at = ?
    WHERE id = ?
    """, (name, updated_at, food_storage_id))

    food_type = read_food_type_by_id(cursor, food_storage_id)
    return {
        "id": food_type["id"],
        "name": food_type["name"],
        "created_at": food_type["created_at"],
        "updated_at": food_type["updated_at"]
    }


def delete_food_type_by_id(cursor, food_storage_id):
    """
    Delete a food type by id from the database.

    :param cursor: sqlite3.Cursor
    :param food_storage_id: int
    :return: str
    """
    existing_food_type = read_food_type_by_id(cursor, food_storage_id)
    if existing_food_type is None:
        return "A food type with this id does not exist."

    cursor.execute("""
    DELETE FROM food_type
    WHERE id = ?
    """, (food_storage_id,))


def create_food_storage(cursor, name, quantity, unit, food_type_id, expiration_date):
    """
    Create a new food storage item in the database.

    :param cursor: sqlite3.Cursor
    :param name: str
    :param quantity: float
    :param unit: str
    :param food_type_id: int
    :param expiration_date: str

    Returns (dict):
        - id: int
        - name: str
        - quantity: float
        - unit: str
        - food_type_id: int
        - expiration_date: str
        - created_at: str
        - updated_at: str
    """
    if quantity < 0:
        return "Quantity cannot be negative."

    existing_food_type = read_food_type_by_id(cursor, food_type_id)
    if existing_food_type is None:
        return "A food type with this id does not exist."

    created_at = datetime.datetime.now()
    updated_at = datetime.datetime.now()

    cursor.execute("""
    INSERT INTO food_storage (name, quantity, unit, food_type_id, expiration_date, created_at, updated_at)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (name, quantity, unit, food_type_id, expiration_date, created_at, updated_at))

    cursor.execute("SELECT * FROM food_storage WHERE id = ?", (cursor.lastrowid,))

    new_food_storage = cursor.fetchone()

    return {
        "id": new_food_storage[0],
        "name": new_food_storage[1],
        "quantity": new_food_storage[2],
        "unit": new_food_storage[3],
        "food_type_id": new_food_storage[4],
        "expiration_date": new_food_storage[5],
        "created_at": new_food_storage[6],
        "updated_at": new_food_storage[7]
    }


def read_all_food_storage(cursor):
    """
    Retrieve all food storage items from the database.

    :param cursor: sqlite3.Cursor

    Returns (list):
    list of dictionaries
        - Each dictionary contains the following
            - id: int
            - name: str
            - quantity: float
            - unit: str
            - food_type_id: int
            - expiration_date: str
            - created_at: str
            - updated_at: str
    """
    cursor.execute("""
    SELECT * FROM food_storage
    """)

    all_food_storage = []

    for food_storage in cursor.fetchall():
        all_food_storage.append({
            "id": food_storage[0],
            "name": food_storage[1],
            "quantity": food_storage[2],
            "unit": food_storage[3],
            "food_type_id": food_storage[4],
            "expiration_date": food_storage[5],
            "created_at": food_storage[6],
            "updated_at": food_storage[7]
        })

    return all_food_storage


def read_food_storage_by_id(cursor, food_storage_id):
    """
    Retrieve a food storage item by id from the database.

    :param cursor: sqlite3.Cursor
    :param food_storage_id: int

    Returns (dict):
        - id: int
        - name: str
        - quantity: float
        - unit: str
        - food_type_id: int
        - expiration_date: str
        - created_at: str
        - updated_at: str
    """
    cursor.execute("""
    SELECT * FROM food_storage
    WHERE id = ?
    """, (food_storage_id,))
    food_storage = cursor.fetchone()

    if food_storage is None:
        return None

    return {
        "id": food_storage[0],
        "name": food_storage[1],
        "quantity": food_storage[2],
        "unit": food_storage[3],
        "food_type_id": food_storage[4],
        "expiration_date": food_storage[5],
        "created_at": food_storage[6],
        "updated_at": food_storage[7]
    }


def update_food_storage_by_id(cursor, food_storage_id, name, quantity, unit, food_type_id, expiration_date):
    """
    Update a food storage item by id in the database.

    :param cursor: sqlite3.Cursor
    :param food_storage_id: int
    :param name: str
    :param quantity: float
    :param unit: str
    :param food_type_id: int
    :param expiration_date: str

    Returns (dict):
        - id: int
        - name: str
        - quantity: float
        - unit: str
        - food_type_id: int
        - expiration_date: str
        - created_at: str
        - updated_at: str
    """
    existing_food_type = read_food_type_by_id(cursor, food_type_id)
    if existing_food_type is None:
        return "A food type with this id does not exist."

    existing_food_storage = read_food_storage_by_id(cursor, food_storage_id)
    if existing_food_storage is None:
        return "A food storage item with this id does not exist."

    updated_at = datetime.datetime.now()

    cursor.execute("""
    UPDATE food_storage
    SET name = ?, quantity = ?, unit = ?, food_type_id = ?, expiration_date = ?, updated_at = ?
    WHERE id = ?
    """, (name, quantity, unit, food_type_id, expiration_date, updated_at, food_storage_id))
    food_storage = read_food_storage_by_id(cursor, food_storage_id)
    return {
        "id": food_storage["id"],
        "name": food_storage["name"],
        "quantity": food_storage["quantity"],
        "unit": food_storage["unit"],
        "food_type_id": food_storage["food_type_id"],
        "expiration_date": food_storage["expiration_date"],
        "created_at": food_storage["created_at"],
        "updated_at": food_storage["updated_at"]
    }


def delete_food_storage_by_id(cursor, food_storage_id):
    """
    Delete a food storage item by id from the database.

    :param cursor: sqlite3.Cursor
    :param food_storage_id: int
    :return: None
    """
    existing_food_storage = read_food_storage_by_id(cursor, food_storage_id)
    if existing_food_storage is None:
        return "A food storage item with this id does not exist."

    cursor.execute("""
    DELETE FROM food_storage
    WHERE id = ?
    """, (food_storage_id,))


def on_create_food_storage():
    name = ENTRY_NAME.get()
    quantity = float(ENTRY_QUANTITY.get())
    unit = ENTRY_UNITY.get()
    food_type = FOOD_TYPE_COMBOBOX.get()
    expiration_date = ENTRY_EXPIRATION_DATE.get()

    CURSOR.execute("SELECT id FROM food_type WHERE name = ?", (food_type,))
    food_type_id = CURSOR.fetchone()[0]

    create_food_storage(CURSOR, name, quantity, unit, food_type_id, expiration_date)
    CONNECTION.commit()
    load_food_storage_data()


def on_update_food_storage():
    selected_item = FOOD_STORAGE_TREE.selection()[0]
    food_storage_id = FOOD_STORAGE_TREE.item(selected_item, "values")[0]

    name = ENTRY_NAME.get()
    quantity = float(ENTRY_QUANTITY.get())
    unit = ENTRY_UNITY.get()
    food_type = FOOD_TYPE_COMBOBOX.get()
    expiration_date = ENTRY_EXPIRATION_DATE.get()

    CURSOR.execute("SELECT id FROM food_type WHERE name = ?", (food_type,))
    food_type_id = CURSOR.fetchone()[0]

    update_food_storage_by_id(CURSOR, food_storage_id, name, quantity, unit, food_type_id, expiration_date)
    CONNECTION.commit()
    load_food_storage_data()


def on_delete_food_storage():
    selected_item = FOOD_STORAGE_TREE.selection()[0]
    food_storage_id = FOOD_STORAGE_TREE.item(selected_item, "values")[0]
    delete_food_storage_by_id(CURSOR, food_storage_id)
    CONNECTION.commit()
    load_food_storage_data()


def load_food_storage_data():
    for item in FOOD_STORAGE_TREE.get_children():
        FOOD_STORAGE_TREE.delete(item)
    food_storage_items = read_all_food_storage(CURSOR)
    for item in food_storage_items:
        FOOD_STORAGE_TREE.insert('', 'end', values=(
            item["id"], item["name"], item["quantity"], item["unit"], item["food_type_id"], item["expiration_date"]))


def create_labels():
    tk.Label(ROOT, text="Name:").grid(row=0, column=0)
    tk.Label(ROOT, text="Quantity:").grid(row=1, column=0)
    tk.Label(ROOT, text="Unit:").grid(row=2, column=0)
    tk.Label(ROOT, text="Food Type:").grid(row=3, column=0)
    tk.Label(ROOT, text="Expiration Date (YYYY-MM-DD):").grid(row=4, column=0)


def create_entries():
    global ENTRY_NAME, ENTRY_QUANTITY, ENTRY_UNITY, ENTRY_EXPIRATION_DATE, FOOD_TYPE_COMBOBOX
    ENTRY_NAME = tk.Entry(ROOT)
    ENTRY_NAME.grid(row=0, column=1)
    ENTRY_QUANTITY = tk.Entry(ROOT)
    ENTRY_QUANTITY.grid(row=1, column=1)
    ENTRY_UNITY = tk.Entry(ROOT)
    ENTRY_UNITY.grid(row=2, column=1)
    FOOD_TYPE_COMBOBOX = ttk.Combobox(ROOT, values=[ft["name"] for ft in read_all_food_types(CURSOR)])
    FOOD_TYPE_COMBOBOX.grid(row=3, column=1)
    ENTRY_EXPIRATION_DATE = tk.Entry(ROOT)
    ENTRY_EXPIRATION_DATE.grid(row=4, column=1)


def create_buttons():
    tk.Button(ROOT, text="Add", command=on_create_food_storage).grid(row=5, column=0)
    tk.Button(ROOT, text="Update", command=on_update_food_storage).grid(row=5, column=1)
    tk.Button(ROOT, text="Delete", command=on_delete_food_storage).grid(row=5, column=2)


def create_treeview():
    global FOOD_STORAGE_TREE
    columns = ("id", "name", "quantity", "unit", "food_type_id", "expiration_date")
    FOOD_STORAGE_TREE = ttk.Treeview(ROOT, columns=columns, show="headings")
    for col in columns:
        FOOD_STORAGE_TREE.heading(col, text=col)
    FOOD_STORAGE_TREE.grid(row=6, column=0, columnspan=3)


def main():
    global CONNECTION, CURSOR, ROOT
    CONNECTION, CURSOR = database_connection()

    food_types = read_all_food_types(CURSOR)
    if not food_types:
        seed_food_types(CURSOR)
        CONNECTION.commit()

    ROOT = tk.Tk()
    ROOT.title("Food Storage Manager")

    create_labels()
    create_entries()
    create_buttons()
    create_treeview()

    load_food_storage_data()

    ROOT.mainloop()


if __name__ == '__main__':
    main()
