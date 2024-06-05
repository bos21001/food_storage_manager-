# Importing database setting up function and seed function
from food_storage_manager import database_connection, seed_food_types

# Importing CRUD functions for food types
from food_storage_manager import read_all_food_types, read_food_type_by_id, read_food_type_by_name, create_food_type, \
    update_food_type_by_id, delete_food_type_by_id

# Importing CRUD functions for food storage
from food_storage_manager import read_all_food_storage, read_food_storage_by_id, create_food_storage, \
    update_food_storage_by_id, delete_food_storage_by_id
import pytest

"""
Testing for GUI were not implemented as it is not possible to test GUI using pytest.
But all its backend functionalities are tested.
"""


@pytest.fixture
def db_connection():
    connection, cursor = database_connection()
    yield cursor
    connection.close()


def test_seed_food_types(db_connection):
    seed_food_types(db_connection)
    all_food_types = read_all_food_types(db_connection)
    names = [food_type["name"] for food_type in all_food_types]

    expected_food_types = ["Fruit", "Vegetable", "Grain", "Protein", "Dairy", "Beverage", "Snack", "Condiment",
                           "Frozen", "Canned", "Baking", "Spice", "Other"]

    for food_type in expected_food_types:
        assert food_type in names


# Testing CRUD functions for food types

def test_create_food_type(db_connection):
    created_food_type = create_food_type(db_connection, "Valid Food Type")
    assert created_food_type["name"] == "Valid Food Type"
    assert created_food_type["id"] is not None
    assert created_food_type["created_at"] is not None
    assert created_food_type["updated_at"] is not None

    created_food_type = create_food_type(db_connection, "    Valid Food  Type 2 ")
    assert created_food_type["name"] == "Valid Food  Type 2"

    created_food_type = create_food_type(db_connection, created_food_type["name"])
    assert created_food_type == "A food type with this name already exists."

    created_food_type = create_food_type(db_connection, "")
    assert created_food_type == "A food type name cannot be empty."

    created_food_type = create_food_type(db_connection, " ")
    assert created_food_type == "A food type name cannot be empty."

    created_food_type = create_food_type(db_connection, "  ")
    assert created_food_type == "A food type name cannot be empty."

    created_food_type = create_food_type(db_connection, None)
    assert created_food_type == "A food type name cannot be empty."


def test_read_all_food_types(db_connection):
    seed_food_types(db_connection)

    all_food_types = read_all_food_types(db_connection)
    assert len(all_food_types) >= 13

    for food_type in all_food_types:
        assert food_type["name"] is not None
        assert food_type["id"] is not None
        assert food_type["created_at"] is not None
        assert food_type["updated_at"] is not None


def test_read_food_type_by_id(db_connection):
    seed_food_types(db_connection)

    all_food_types = read_all_food_types(db_connection)
    for food_type in all_food_types:
        food_type_id = food_type["id"]
        food_type_by_id = read_food_type_by_id(db_connection, food_type_id)
        assert food_type_by_id["name"] == food_type["name"]
        assert food_type_by_id["id"] == food_type["id"]
        assert food_type_by_id["created_at"] == food_type["created_at"]
        assert food_type_by_id["updated_at"] == food_type["updated_at"]

    food_type_by_id = read_food_type_by_id(db_connection, 9999)
    assert food_type_by_id == "A food type with this id does not exist."


def test_read_food_type_by_name(db_connection):
    seed_food_types(db_connection)

    all_food_types = read_all_food_types(db_connection)
    for food_type in all_food_types:
        food_type_name = food_type["name"]
        food_type_by_name = read_food_type_by_name(db_connection, food_type_name)
        assert food_type_by_name["name"] == food_type["name"]
        assert food_type_by_name["id"] == food_type["id"]
        assert food_type_by_name["created_at"] == food_type["created_at"]
        assert food_type_by_name["updated_at"] == food_type["updated_at"]

    food_type_by_name = read_food_type_by_name(db_connection, "Invalid Food Type")
    assert food_type_by_name == "A food type with this name does not exist."


def test_update_food_type_by_id(db_connection):
    seed_food_types(db_connection)

    all_food_types = read_all_food_types(db_connection)
    for food_type in all_food_types:
        food_type_id = food_type["id"]
        updated_food_type = update_food_type_by_id(db_connection, food_type_id, f"Updated Food Type{food_type_id}")
        if food_type["name"] == "Other":
            assert updated_food_type == "Cannot update the default food type."
        else:
            assert updated_food_type["name"] == f"Updated Food Type{food_type_id}"
            assert updated_food_type["id"] == food_type_id
            assert updated_food_type["created_at"] == food_type["created_at"]
            assert updated_food_type["updated_at"] is not food_type["updated_at"]

    updated_food_type = update_food_type_by_id(db_connection, 9999, "Updated Food Type")
    assert updated_food_type == "A food type with this id does not exist."

    updated_food_type = update_food_type_by_id(db_connection, all_food_types[0]["id"], "")
    assert updated_food_type == "A food type name cannot be empty."

    updated_food_type = update_food_type_by_id(db_connection, all_food_types[0]["id"], " ")
    assert updated_food_type == "A food type name cannot be empty."

    updated_food_type = update_food_type_by_id(db_connection, all_food_types[0]["id"], "  ")
    assert updated_food_type == "A food type name cannot be empty."

    updated_food_type = update_food_type_by_id(db_connection, all_food_types[0]["id"], None)
    assert updated_food_type == "A food type name cannot be empty."

    food_type = read_food_type_by_id(db_connection, all_food_types[0]["id"])
    updated_food_type = update_food_type_by_id(db_connection, food_type["id"], food_type["name"])
    assert updated_food_type == "A food type with this name already exists."


def test_delete_food_type_by_id(db_connection):
    seed_food_types(db_connection)

    all_food_types = read_all_food_types(db_connection)
    for food_type in all_food_types:
        food_type_id = food_type["id"]
        deleted_food_type = delete_food_type_by_id(db_connection, food_type_id)
        if food_type["name"] == "Other":
            assert deleted_food_type == "Cannot delete the default food type."
        else:
            assert deleted_food_type is None
            food_type_by_id = read_food_type_by_id(db_connection, food_type_id)
            assert food_type_by_id == "A food type with this id does not exist."

    deleted_food_type = delete_food_type_by_id(db_connection, 9999)
    assert deleted_food_type == "A food type with this id does not exist."


# Testing CRUD functions for food storage

def test_create_food_storage(db_connection):
    created_food_type = create_food_type(db_connection, "Valid Food Type")
    created_food_storage = create_food_storage(db_connection, "Valid Food Storage", 10, "Kg",
                                               created_food_type["id"], "2021-01-01")

    assert created_food_storage["name"] == "Valid Food Storage"
    assert created_food_storage["quantity"] == 10
    assert created_food_storage["unit"] == "Kg"
    assert created_food_storage["food_type_id"] == created_food_type["id"]
    assert created_food_storage["expiration_date"] == "2021-01-01"
    assert created_food_storage["id"] is not None
    assert created_food_storage["created_at"] is not None
    assert created_food_storage["updated_at"] is not None

    created_food_storage = create_food_storage(db_connection, "    Valid Food  Storage 2 ", 10, "Kg",
                                               created_food_type["id"], "2021-01-01")

    assert created_food_storage["name"] == "Valid Food  Storage 2"
    assert created_food_storage["quantity"] == 10
    assert created_food_storage["unit"] == "Kg"
    assert created_food_storage["food_type_id"] == created_food_type["id"]
    assert created_food_storage["expiration_date"] == "2021-01-01"
    assert created_food_storage["id"] is not None

    created_food_storage = create_food_storage(db_connection, "", 10, "Kg",
                                               created_food_type["id"], "2021-01-01")
    assert created_food_storage == "Name cannot be empty."

    created_food_storage = create_food_storage(db_connection, " ", 10, "Kg",
                                               created_food_type["id"], "2021-01-01")
    assert created_food_storage == "Name cannot be empty."

    created_food_storage = create_food_storage(db_connection, "  ", 10, "Kg",
                                               created_food_type["id"], "2021-01-01")
    assert created_food_storage == "Name cannot be empty."

    created_food_storage = create_food_storage(db_connection, None, 10, "Kg",
                                               created_food_type["id"], "2021-01-01")
    assert created_food_storage == "Name cannot be empty."

    created_food_storage = create_food_storage(db_connection, "Valid Food Storage", -1, "Kg",
                                               created_food_type["id"], "2021-01-01")
    assert created_food_storage == "Quantity cannot be negative."

    created_food_storage = create_food_storage(db_connection, "Valid Food Storage", "wrong", "Kg",
                                               created_food_type["id"], "2021-01-01")
    assert created_food_storage == "Quantity must be a number."

    created_food_storage = create_food_storage(db_connection, "Valid Food Storage", 10, "Kg",
                                               9999, "2021-01-01")
    assert created_food_storage == "A food type with this id does not exist."

    created_food_storage = create_food_storage(db_connection, "Valid Food Storage", 10, "Kg",
                                               created_food_type["id"], "")
    assert created_food_storage == "Expiration Date cannot be empty."

    created_food_storage = create_food_storage(db_connection, "Valid Food Storage", 10, "Kg",
                                               created_food_type["id"], " ")
    assert created_food_storage == "Expiration Date cannot be empty."

    created_food_storage = create_food_storage(db_connection, "Valid Food Storage", 10, "Kg",
                                               created_food_type["id"], "  ")
    assert created_food_storage == "Expiration Date cannot be empty."

    created_food_storage = create_food_storage(db_connection, "Valid Food Storage", 10, "Kg",
                                               created_food_type["id"], None)
    assert created_food_storage == "Expiration Date cannot be empty."

    created_food_storage = create_food_storage(db_connection, "Valid Food Storage", 10, "Kg",
                                               created_food_type["id"], "2021-30-01")
    assert created_food_storage == "Expiration Date must be in the format YYYY-MM-DD."

    created_food_storage = create_food_storage(db_connection, "Valid Food Storage", 10, "",
                                               created_food_type["id"], "2021-01-30")
    assert created_food_storage == "Unit cannot be empty."


def test_read_all_food_storage(db_connection):
    seed_food_types(db_connection)

    all_food_types = read_all_food_types(db_connection)

    # Create food storage for each food type
    for food_type in all_food_types:
        create_food_storage(db_connection, f"Food Storage for {food_type['name']}", 10, "Kg",
                            food_type["id"], "2021-01-01")

    all_food_storage = read_all_food_storage(db_connection)
    assert len(all_food_storage) >= 1

    for food_storage in all_food_storage:
        assert food_storage["name"] is not None
        assert food_storage["quantity"] is not None
        assert food_storage["unit"] is not None
        assert food_storage["food_type_id"] is not None
        assert food_storage["expiration_date"] is not None
        assert food_storage["id"] is not None
        assert food_storage["created_at"] is not None
        assert food_storage["updated_at"] is not None


def test_read_food_storage_by_id(db_connection):
    seed_food_types(db_connection)

    all_food_storage = read_all_food_storage(db_connection)
    for food_storage in all_food_storage:
        food_storage_id = food_storage["id"]
        food_storage_by_id = read_food_storage_by_id(db_connection, food_storage_id)
        assert food_storage_by_id["name"] == food_storage["name"]
        assert food_storage_by_id["quantity"] == food_storage["quantity"]
        assert food_storage_by_id["unit"] == food_storage["unit"]
        assert food_storage_by_id["food_type_id"] == food_storage["food_type_id"]
        assert food_storage_by_id["expiration_date"] == food_storage["expiration_date"]
        assert food_storage_by_id["id"] == food_storage["id"]
        assert food_storage_by_id["created_at"] == food_storage["created_at"]
        assert food_storage_by_id["updated_at"] == food_storage["updated_at"]

    food_storage_by_id = read_food_storage_by_id(db_connection, 9999)
    assert food_storage_by_id == "A food storage with this id does not exist."


def test_update_food_storage_by_id(db_connection):
    seed_food_types(db_connection)

    all_food_types = read_all_food_types(db_connection)

    # Create food storage for each food type
    for food_type in all_food_types:
        create_food_storage(db_connection, f"Food Storage for {food_type['name']}", 10, "Kg",
                            food_type["id"], "2021-01-01")

    all_food_storage = read_all_food_storage(db_connection)
    for food_storage in all_food_storage:
        food_storage_id = food_storage["id"]
        updated_food_storage = update_food_storage_by_id(db_connection, food_storage_id,
                                                         f"Updated Food Storage{food_storage_id}", 20, "L",
                                                         food_storage["food_type_id"], "2021-01-01")
        assert updated_food_storage["name"] == f"Updated Food Storage{food_storage_id}"
        assert updated_food_storage["quantity"] == 20
        assert updated_food_storage["unit"] == "L"
        assert updated_food_storage["food_type_id"] == food_storage["food_type_id"]
        assert updated_food_storage["expiration_date"] == "2021-01-01"
        assert updated_food_storage["id"] == food_storage_id
        assert updated_food_storage["created_at"] == food_storage["created_at"]
        assert updated_food_storage["updated_at"] is not food_storage["updated_at"]

    updated_food_storage = update_food_storage_by_id(db_connection, 9999, "Updated Food Storage", 20, "L",
                                                     all_food_storage[0]["food_type_id"], "2021-01-01")
    assert updated_food_storage == "A food storage with this id does not exist."

    updated_food_storage = update_food_storage_by_id(db_connection, all_food_storage[0]["id"], "", 20, "L",
                                                     all_food_storage[0]["food_type_id"], "2021-01-01")
    assert updated_food_storage == "Name cannot be empty."

    updated_food_storage = update_food_storage_by_id(db_connection, all_food_storage[0]["id"], " ", 20, "L",
                                                     all_food_storage[0]["food_type_id"], "2021-01-01")
    assert updated_food_storage == "Name cannot be empty."

    updated_food_storage = update_food_storage_by_id(db_connection, all_food_storage[0]["id"], "  ", 20, "L",
                                                     all_food_storage[0]["food_type_id"], "2021-01-01")
    assert updated_food_storage == "Name cannot be empty."

    updated_food_storage = update_food_storage_by_id(db_connection, all_food_storage[0]["id"], None, 20, "L",
                                                     all_food_storage[0]["food_type_id"], "2021-01-01")
    assert updated_food_storage == "Name cannot be empty."

    updated_food_storage = update_food_storage_by_id(db_connection, all_food_storage[0]["id"], "Updated Food Storage",
                                                     -1, "L",
                                                     all_food_storage[0]["food_type_id"], "2021-01-01")
    assert updated_food_storage == "Quantity cannot be negative."

    updated_food_storage = update_food_storage_by_id(db_connection, all_food_storage[0]["id"], "Updated Food Storage",
                                                     "wrong", "L",
                                                     all_food_storage[0]["food_type_id"], "2021-01-01")
    assert updated_food_storage == "Quantity must be a number."

    updated_food_storage = update_food_storage_by_id(db_connection, all_food_storage[0]["id"], "Updated Food Storage",
                                                     20, "",
                                                     all_food_storage[0]["food_type_id"], "2021-01-01")
    assert updated_food_storage == "Unit cannot be empty."

    updated_food_storage = update_food_storage_by_id(db_connection, all_food_storage[0]["id"], "Updated Food Storage",
                                                     20, "L",
                                                     9999, "2021-01-01")
    assert updated_food_storage == "A food type with this id does not exist."

    updated_food_storage = update_food_storage_by_id(db_connection, all_food_storage[0]["id"], "Updated Food Storage",
                                                     20, "L",
                                                     all_food_storage[0]["food_type_id"], "")
    assert updated_food_storage == "Expiration Date cannot be empty."

    updated_food_storage = update_food_storage_by_id(db_connection, all_food_storage[0]["id"], "Updated Food Storage",
                                                     20, "L",
                                                     all_food_storage[0]["food_type_id"], " ")
    assert updated_food_storage == "Expiration Date cannot be empty."

    updated_food_storage = update_food_storage_by_id(db_connection, all_food_storage[0]["id"], "Updated Food Storage",
                                                     20, "L",
                                                     all_food_storage[0]["food_type_id"], "  ")
    assert updated_food_storage == "Expiration Date cannot be empty."

    updated_food_storage = update_food_storage_by_id(db_connection, all_food_storage[0]["id"], "Updated Food Storage",
                                                     20, "L",
                                                     all_food_storage[0]["food_type_id"], None)
    assert updated_food_storage == "Expiration Date cannot be empty."

    updated_food_storage = update_food_storage_by_id(db_connection, all_food_storage[0]["id"], "Updated Food Storage",
                                                     20, "L",
                                                     all_food_storage[0]["food_type_id"], "2021-30-01")
    assert updated_food_storage == "Expiration Date must be in the format YYYY-MM-DD."


def test_delete_food_storage_by_id(db_connection):
    seed_food_types(db_connection)

    all_food_storage = read_all_food_storage(db_connection)
    for food_storage in all_food_storage:
        food_storage_id = food_storage["id"]
        deleted_food_storage = delete_food_storage_by_id(db_connection, food_storage_id)
        assert deleted_food_storage is None
        food_storage_by_id = read_food_storage_by_id(db_connection, food_storage_id)
        assert food_storage_by_id == "A food storage with this id does not exist."

    deleted_food_storage = delete_food_storage_by_id(db_connection, 9999)
    assert deleted_food_storage == "A food storage with this id does not exist."


pytest.main(["-v", "--tb=line", "-rN", __file__])
