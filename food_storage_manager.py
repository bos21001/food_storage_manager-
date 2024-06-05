import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
import datetime

# Global variables
global CONNECTION, CURSOR
global ROOT, ENTRY_NAME, ENTRY_QUANTITY, ENTRY_UNITY, ENTRY_EXPIRATION_DATE, FOOD_TYPE_NAME_COMBOBOX, FOOD_STORAGE_TREE
global FOOD_TYPE_NAME_ENTRY, FOOD_TYPE_TREE, TAB_CONTROL


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


def read_food_type_by_id(cursor, food_type_id):
    """
    Retrieve a food type by id from the database.

    :param cursor: sqlite3.Cursor
    :param food_type_id: int

    Returns (dict):
        - id: int
        - name: str
        - created_at: str
        - updated_at: str
    """
    cursor.execute("""
    SELECT * FROM food_type
    WHERE id = ?
    """, (food_type_id,))
    food_type = cursor.fetchone()

    if food_type is None:
        return None

    return {
        "id": food_type[0],
        "name": food_type[1],
        "created_at": food_type[2],
        "updated_at": food_type[3]
    }


def read_food_type_by_name(cursor, food_type_name):
    """
    Retrieve a food type by name from the database.

    :param cursor: sqlite3.Cursor
    :param food_type_name: str

    Returns (dict):
        - id: int
        - name: str
        - created_at: str
        - updated_at: str
    """
    cursor.execute("""
    SELECT * FROM food_type
    WHERE name = ?
    """, (food_type_name,))
    food_type = cursor.fetchone()

    if food_type is None:
        return None

    return {
        "id": food_type[0],
        "name": food_type[1],
        "created_at": food_type[2],
        "updated_at": food_type[3]
    }


def update_food_type_by_id(cursor, food_type_id, name):
    """
    Update a food type by id in the database.

    :param cursor: sqlite3.Cursor
    :param food_type_id: int
    :param name: str

    Returns (dict):
        - id: int
        - name: str
        - created_at: str
        - updated_at: str
    """
    existing_food_type = read_food_type_by_id(cursor, food_type_id)
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
    """, (name, updated_at, food_type_id))

    food_type = read_food_type_by_id(cursor, food_type_id)
    return {
        "id": food_type["id"],
        "name": food_type["name"],
        "created_at": food_type["created_at"],
        "updated_at": food_type["updated_at"]
    }


def delete_food_type_by_id(cursor, food_type_id):
    """
    Delete a food type by id from the database.

    :param cursor: sqlite3.Cursor
    :param food_type_id: int
    :return: str
    """
    existing_food_type = read_food_type_by_id(cursor, food_type_id)
    if existing_food_type is None:
        return "A food type with this id does not exist."

    cursor.execute("""
    DELETE FROM food_type
    WHERE id = ?
    """, (food_type_id,))


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
            - food_type_name: str
            - expiration_date: str
            - created_at: str
            - updated_at: str
    """
    cursor.execute("""
    SELECT
        food_storage.id,
        food_storage.name,
        food_storage.quantity,
        food_storage.unit,
        food_storage.food_type_id,
        food_type.name,
        food_storage.expiration_date,
        food_storage.created_at,
        food_storage.updated_at
     FROM food_storage
     JOIN food_type
     ON food_storage.food_type_id = food_type.id
    """)

    all_food_storage = []

    for food_storage in cursor.fetchall():
        all_food_storage.append({
            "id": food_storage[0],
            "name": food_storage[1],
            "quantity": food_storage[2],
            "unit": food_storage[3],
            "food_type_id": food_storage[4],
            "food_type_name": food_storage[5],
            "expiration_date": food_storage[6],
            "created_at": food_storage[7],
            "updated_at": food_storage[8]
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


def get_food_storage_inputs():
    """
    Retrieve the user inputs from the entry fields.

    Returns (dict):
        - name: str
        - quantity: float
        - unit: str
        - food_type: dict
        - expiration_date: str
    """

    name = ENTRY_NAME.get()

    # If name is empty, return an error message
    if not name:
        tk.messagebox.showerror("Error", "Name cannot be empty.")
        return

    quantity = ENTRY_QUANTITY.get()

    # if quantity is empty, return an error message
    if not quantity:
        tk.messagebox.showerror("Error", "Quantity cannot be empty.")
        return
    # if quantity is not float, return an error message
    try:
        quantity = float(quantity)
    except ValueError:
        tk.messagebox.showerror("Error", "Quantity must be a number.")
        return

    if quantity < 0:
        tk.messagebox.showerror("Error", "Quantity cannot be negative.")
        return

    unit = ENTRY_UNITY.get()

    if not unit:
        tk.messagebox.showerror("Error", "Unit cannot be empty.")
        return

    food_type_name = FOOD_TYPE_NAME_COMBOBOX.get()

    if not food_type_name:
        tk.messagebox.showerror("Error", "Food Type cannot be empty.")
        return

    food_type = read_food_type_by_name(CURSOR, food_type_name)

    # if food type name is not in the list, return an error message
    if food_type is None:
        tk.messagebox.showerror("Error", "Food Type does not exist.")
        return

    expiration_date = ENTRY_EXPIRATION_DATE.get()

    if not expiration_date:
        tk.messagebox.showerror("Error", "Expiration Date cannot be empty.")
        return

    # if expiration date is not in the correct format, return an error message
    try:
        datetime.datetime.strptime(expiration_date, "%Y-%m-%d")
    except ValueError:
        tk.messagebox.showerror("Error", "Expiration Date must be in the format YYYY-MM-DD.")
        return

    return {
        "name": name,
        "quantity": quantity,
        "unit": unit,
        "food_type": food_type,
        "expiration_date": expiration_date
    }


def on_create_food_storage():
    inputs = get_food_storage_inputs()

    if not inputs:
        return

    created_food_storage = create_food_storage(CURSOR, inputs["name"], inputs["quantity"], inputs["unit"],
                                               inputs["food_type"]["id"], inputs["expiration_date"])

    if isinstance(created_food_storage, str):
        tk.messagebox.showerror("Error", created_food_storage)
        return

    load_food_storage_data()
    CURSOR.connection.commit()

    tk.messagebox.showinfo("Success", "Food Storage item created successfully.")


def on_update_food_storage():
    try:
        selected_item = FOOD_STORAGE_TREE.selection()[0]
    except IndexError:
        selected_item = None

    # if no item is selected, return an error message
    if not selected_item:
        tk.messagebox.showerror("Error", "Please select an item.")
        return

    food_storage_id = FOOD_STORAGE_TREE.item(selected_item, "values")[0]

    inputs = get_food_storage_inputs()

    if not inputs:
        return

    updated_food_storage = update_food_storage_by_id(CURSOR, food_storage_id, inputs["name"], inputs["quantity"],
                                                     inputs["unit"], inputs["food_type"]["id"],
                                                     inputs["expiration_date"])

    # if updated_food_storage is a string, it means an error occurred
    if isinstance(updated_food_storage, str):
        tk.messagebox.showerror("Unknown Error", updated_food_storage)
        return

    load_food_storage_data()
    CURSOR.connection.commit()

    tk.messagebox.showinfo("Success", "Food Storage item updated successfully.")


def on_delete_food_storage():
    food_storage_id = None

    try:
        selected_item = FOOD_STORAGE_TREE.selection()[0]
        food_storage_id = FOOD_STORAGE_TREE.item(selected_item, "values")[0]
    except IndexError:
        selected_item = None

    # if no item is selected, return an error message
    if not selected_item:
        tk.messagebox.showerror("Error", "Please select an item.")
        return

    deleted_food_storage = delete_food_storage_by_id(CURSOR, food_storage_id)

    # if deleted_food_storage is a string, it means an error occurred
    if isinstance(deleted_food_storage, str):
        tk.messagebox.showerror("Unknown Error", deleted_food_storage)
        return

    load_food_storage_data()
    CURSOR.connection.commit()

    tk.messagebox.showinfo("Success", "Food Storage item deleted successfully.")


def on_treeview_select(event):
    is_not_selected = FOOD_STORAGE_TREE.item(FOOD_STORAGE_TREE.selection())["values"] == ""

    if is_not_selected:
        return

    selected_item = FOOD_STORAGE_TREE.selection()[0]
    item = FOOD_STORAGE_TREE.item(selected_item)
    food_storage = item['values']

    ENTRY_NAME.delete(0, tk.END)
    ENTRY_NAME.insert(0, food_storage[1])

    ENTRY_QUANTITY.delete(0, tk.END)
    ENTRY_QUANTITY.insert(0, food_storage[2])

    ENTRY_UNITY.delete(0, tk.END)
    ENTRY_UNITY.insert(0, food_storage[3])

    FOOD_TYPE_NAME_COMBOBOX.set('')
    FOOD_TYPE_NAME_COMBOBOX.set(food_storage[4])

    ENTRY_EXPIRATION_DATE.delete(0, tk.END)
    ENTRY_EXPIRATION_DATE.insert(0, food_storage[5])


def load_food_storage_data():
    try:
        ENTRY_NAME.delete(0, tk.END)
        ENTRY_QUANTITY.delete(0, tk.END)
        ENTRY_UNITY.delete(0, tk.END)
        ENTRY_EXPIRATION_DATE.delete(0, tk.END)
        FOOD_TYPE_NAME_COMBOBOX.set('')

        for item in FOOD_STORAGE_TREE.get_children():
            FOOD_STORAGE_TREE.delete(item)
        food_storage_items = read_all_food_storage(CURSOR)
        for item in food_storage_items:
            FOOD_STORAGE_TREE.insert('', 'end', values=(
                item["id"], item["name"], item["quantity"], item["unit"], item["food_type_name"],
                item["expiration_date"]))

        FOOD_TYPE_NAME_COMBOBOX['values'] = [ft["name"] for ft in read_all_food_types(CURSOR)]
    except Exception as e:
        tk.messagebox.showerror("Unknown Error:", str(e))


def create_labels(food_storage_tab):
    tk.Label(food_storage_tab, text="Food Storage Name:").grid(row=0, column=0)
    tk.Label(food_storage_tab, text="Quantity:").grid(row=1, column=0)
    tk.Label(food_storage_tab, text="Unit:").grid(row=2, column=0)
    tk.Label(food_storage_tab, text="Food Type:").grid(row=3, column=0)
    tk.Label(food_storage_tab, text="Expiration Date (YYYY-MM-DD):").grid(row=4, column=0)


def create_entries(food_storage_tab):
    global ENTRY_NAME, ENTRY_QUANTITY, ENTRY_UNITY, ENTRY_EXPIRATION_DATE, FOOD_TYPE_NAME_COMBOBOX
    ENTRY_NAME = tk.Entry(food_storage_tab)
    ENTRY_NAME.grid(row=0, column=1)
    ENTRY_QUANTITY = tk.Entry(food_storage_tab)
    ENTRY_QUANTITY.grid(row=1, column=1)
    ENTRY_UNITY = tk.Entry(food_storage_tab)
    ENTRY_UNITY.grid(row=2, column=1)

    names = [ft["name"] for ft in read_all_food_types(CURSOR)]

    FOOD_TYPE_NAME_COMBOBOX = ttk.Combobox(food_storage_tab, values=names)
    FOOD_TYPE_NAME_COMBOBOX.grid(row=3, column=1)
    ENTRY_EXPIRATION_DATE = tk.Entry(food_storage_tab)
    ENTRY_EXPIRATION_DATE.grid(row=4, column=1)


def create_buttons(food_storage_tab):
    tk.Button(food_storage_tab, text="Add", command=on_create_food_storage).grid(row=5, column=0)
    tk.Button(food_storage_tab, text="Update", command=on_update_food_storage).grid(row=5, column=1)
    tk.Button(food_storage_tab, text="Delete", command=on_delete_food_storage).grid(row=5, column=2)


def create_treeview(food_storage_tab):
    global FOOD_STORAGE_TREE
    columns = ("id", "name", "quantity", "unit", "food_type_name", "expiration_date")
    FOOD_STORAGE_TREE = ttk.Treeview(food_storage_tab, columns=columns, show="headings")
    for col in columns:
        FOOD_STORAGE_TREE.heading(col, text=col)

    FOOD_STORAGE_TREE.bind('<<TreeviewSelect>>', on_treeview_select)

    FOOD_STORAGE_TREE.grid(row=6, column=0, columnspan=3)


def create_food_storage_tab():
    global ENTRY_NAME, ENTRY_QUANTITY, ENTRY_UNITY, ENTRY_EXPIRATION_DATE, FOOD_TYPE_NAME_COMBOBOX, FOOD_STORAGE_TREE

    food_storage_tab = ttk.Frame(TAB_CONTROL)
    TAB_CONTROL.add(food_storage_tab, text='Manage Food Storage')

    create_labels(food_storage_tab)
    create_entries(food_storage_tab)
    create_buttons(food_storage_tab)
    create_treeview(food_storage_tab)

    load_food_storage_data()


def create_food_type_tab():
    global FOOD_TYPE_NAME_ENTRY, FOOD_TYPE_TREE

    food_type_tab = ttk.Frame(TAB_CONTROL)
    TAB_CONTROL.add(food_type_tab, text='Manage Food Types')

    # Create widgets for food type management
    tk.Label(food_type_tab, text="Food Type Name:").grid(row=0, column=0)
    FOOD_TYPE_NAME_ENTRY = tk.Entry(food_type_tab)
    FOOD_TYPE_NAME_ENTRY.grid(row=0, column=1)

    tk.Button(food_type_tab, text="Add", command=on_create_food_type).grid(row=1, column=0)
    tk.Button(food_type_tab, text="Update", command=on_update_food_type).grid(row=1, column=1)
    tk.Button(food_type_tab, text="Delete", command=on_delete_food_type).grid(row=1, column=2)

    columns = ("id", "name")
    FOOD_TYPE_TREE = ttk.Treeview(food_type_tab, columns=columns, show="headings")
    for col in columns:
        FOOD_TYPE_TREE.heading(col, text=col)

    FOOD_TYPE_TREE.bind('<<TreeviewSelect>>', on_food_type_treeview_select)

    FOOD_TYPE_TREE.grid(row=2, column=0, columnspan=3)

    load_food_type_data()


def on_create_food_type():
    name = FOOD_TYPE_NAME_ENTRY.get()

    if not name:
        tk.messagebox.showerror("Error", "Name cannot be empty.")
        return

    created_food_type = create_food_type(CURSOR, name)

    if isinstance(created_food_type, str):
        tk.messagebox.showerror("Error", created_food_type)
        return

    load_food_type_data()
    load_food_storage_data()
    CURSOR.connection.commit()

    tk.messagebox.showinfo("Success", "Food Type created successfully.")


def on_update_food_type():
    try:
        selected_item = FOOD_TYPE_TREE.selection()[0]
    except IndexError:
        selected_item = None

    if not selected_item:
        tk.messagebox.showerror("Error", "Please select an item.")
        return

    food_type_id = FOOD_TYPE_TREE.item(selected_item, "values")[0]
    name = FOOD_TYPE_NAME_ENTRY.get()

    if not name:
        tk.messagebox.showerror("Error", "Name cannot be empty.")
        return

    updated_food_type = update_food_type_by_id(CURSOR, food_type_id, name)

    if isinstance(updated_food_type, str):
        tk.messagebox.showerror("Error", updated_food_type)
        return

    load_food_type_data()
    load_food_storage_data()
    CURSOR.connection.commit()

    tk.messagebox.showinfo("Success", "Food Type updated successfully.")


def on_delete_food_type():
    try:
        selected_item = FOOD_TYPE_TREE.selection()[0]
    except IndexError:
        selected_item = None

    if not selected_item:
        tk.messagebox.showerror("Error", "Please select an item.")
        return

    food_type_id = FOOD_TYPE_TREE.item(selected_item, "values")[0]

    # TODO: Check if food type is being used in food storage items
    # TODO: If it is being used, replace the food type with a default food type (e.g. "Other")

    delete_food_type_by_id(CURSOR, food_type_id)

    load_food_type_data()
    load_food_storage_data()
    CURSOR.connection.commit()

    tk.messagebox.showinfo("Success", "Food Type deleted successfully.")


def on_food_type_treeview_select(event):
    is_not_selected = FOOD_TYPE_TREE.item(FOOD_TYPE_TREE.selection())["values"] == ""

    if is_not_selected:
        return

    selected_item = FOOD_TYPE_TREE.selection()[0]
    item = FOOD_TYPE_TREE.item(selected_item)
    food_type = item['values']

    FOOD_TYPE_NAME_ENTRY.delete(0, tk.END)
    FOOD_TYPE_NAME_ENTRY.insert(0, food_type[1])


def load_food_type_data():
    try:
        FOOD_TYPE_NAME_ENTRY.delete(0, tk.END)

        for item in FOOD_TYPE_TREE.get_children():
            FOOD_TYPE_TREE.delete(item)
        food_types = read_all_food_types(CURSOR)
        for item in food_types:
            FOOD_TYPE_TREE.insert('', 'end', values=(item["id"], item["name"]))
    except Exception as e:
        tk.messagebox.showerror("Unknown Error:", str(e))


def main():
    global CONNECTION, CURSOR, ROOT, TAB_CONTROL
    CONNECTION, CURSOR = database_connection()

    food_types = read_all_food_types(CURSOR)
    if not food_types:
        seed_food_types(CURSOR)
        CONNECTION.commit()

    ROOT = tk.Tk()
    ROOT.title("Food Storage Manager")

    TAB_CONTROL = ttk.Notebook(ROOT)

    create_food_storage_tab()
    create_food_type_tab()

    TAB_CONTROL.pack(expand=1, fill='both')

    TAB_CONTROL.bind("<<NotebookTabChanged>>", lambda event: load_food_storage_data() or load_food_type_data())

    ROOT.mainloop()


if __name__ == '__main__':
    main()
