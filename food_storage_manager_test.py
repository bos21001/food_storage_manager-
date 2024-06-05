# Importing the necessary functions and libraries.
from food_storage_manager import *
import pytest


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


def test_create_and_read_food_type(db_connection):
    food_type = create_food_type(db_connection, "Fruits")
    result = read_food_type_by_id(db_connection, food_type["id"])
    assert result['name'] == "Fruits"


def test_create_existing_food_type(db_connection):
    create_food_type(db_connection, "Fruits")
    result = create_food_type(db_connection, "Fruits")
    assert result == "A food type with this name already exists."


def test_read_non_existing_food_type_by_id(db_connection):
    result = read_food_type_by_id(db_connection, 999)
    assert result is None


def test_update_existing_food_type_by_id(db_connection):
    created_food_type = create_food_type(db_connection, "Fruits")
    result = update_food_type_by_id(db_connection, created_food_type["id"], "Vegetables")
    assert result['name'] == "Vegetables"


def test_update_non_existing_food_type_by_id(db_connection):
    result = update_food_type_by_id(db_connection, 999, "Vegetables")
    assert result == "A food type with this id does not exist."


def test_delete_existing_food_type_by_id(db_connection):
    food_type = create_food_type(db_connection, "Fruits")
    delete_food_type_by_id(db_connection, food_type["id"])
    result = read_food_type_by_id(db_connection, food_type["id"])
    assert result is None


def test_delete_non_existing_food_type_by_id(db_connection):
    result = delete_food_type_by_id(db_connection, 999)
    assert result == "A food type with this id does not exist."


def test_create_and_read_food_storage(db_connection):
    food_type = create_food_type(db_connection, "Fruits")
    create_food_storage(db_connection, "Apple", 1.0, "kg", food_type["id"], "2022-12-31")
    result = read_food_type_by_id(db_connection, food_type["id"])
    assert result['name'] == "Fruits"


def test_create_food_storage_with_non_existing_food_type(db_connection):
    result = create_food_storage(db_connection, "Apple", 1.0, "kg", 999, "2022-12-31")
    assert result == "A food type with this id does not exist."


def test_read_non_existing_food_storage_by_id(db_connection):
    result = read_food_storage_by_id(db_connection, 999)
    assert result is None


def test_update_existing_food_storage_by_id(db_connection):
    food_type = create_food_type(db_connection, "Fruits")
    food_storage = create_food_storage(db_connection, "Apple", 1.0, "kg", food_type["id"], "2022-12-31")
    result = update_food_storage_by_id(db_connection, food_storage["id"], "Banana", 2.0, "kg", food_type["id"],
                                       "2023-12-31")
    assert result['name'] == "Banana"


def test_update_non_existing_food_storage_by_id(db_connection):
    all_food_types = read_all_food_types(db_connection)
    result = update_food_storage_by_id(db_connection, 999, "Banana", 2.0, "kg", all_food_types[0]["id"], "2023-12-31")
    assert result == "A food storage item with this id does not exist."


def test_delete_existing_food_storage_by_id(db_connection):
    food_type = create_food_type(db_connection, "Fruits")
    food_storage = create_food_storage(db_connection, "Apple", 1.0, "kg", food_type["id"], "2022-12-31")
    delete_food_storage_by_id(db_connection, food_storage["id"])
    result = read_food_storage_by_id(db_connection, food_storage["id"])
    assert result is None


def test_delete_non_existing_food_storage_by_id(db_connection):
    result = delete_food_storage_by_id(db_connection, 999)
    assert result == "A food storage item with this id does not exist."


def test_update_food_storage_with_non_existing_food_type(db_connection):
    created_food_type = create_food_type(db_connection, "Something Else")
    food_storage = create_food_storage(db_connection, "Apple", 1.0, "kg", created_food_type["id"], "2022-12-31")
    result = update_food_storage_by_id(db_connection, food_storage["id"], "Banana", 2.0, "kg", 999, "2023-12-31")
    assert result == "A food type with this id does not exist."


def test_create_and_read_all_food_storage(db_connection):
    food_type = create_food_type(db_connection, "Fruits")
    apple = create_food_storage(db_connection, "Apple", 1.0, "kg", food_type["id"], "2022-12-31")
    banana = create_food_storage(db_connection, "Banana", 2.0, "kg", food_type["id"], "2023-01-31")
    result = read_all_food_storage(db_connection)
    # for loop to check if the food storage items are in the result
    for food_storage in result:
        if food_storage["id"] == apple["id"]:
            assert food_storage["name"] == "Apple"
        elif food_storage["id"] == banana["id"]:
            assert food_storage["name"] == "Banana"


def test_create_and_read_food_type_by_name(db_connection):
    create_food_type(db_connection, "Something Else")
    result = read_food_type_by_name(db_connection, "Something Else")
    assert result['name'] == "Something Else"

    result = read_food_type_by_name(db_connection, "Other Thing")
    assert result is None

    result = read_food_type_by_name(db_connection, "")
    assert result is None


# Boundary tests
def test_create_food_type_with_empty_name(db_connection):
    result = create_food_type(db_connection, "")
    assert result == "A food type name cannot be empty."

    result = create_food_type(db_connection, " ")
    assert result == "A food type name cannot be empty."

    result = create_food_type(db_connection, "  ")
    assert result == "A food type name cannot be empty."

    result = create_food_type(db_connection, None)
    assert result == "A food type name cannot be empty."


def test_create_food_storage_with_negative_quantity(db_connection):
    food_type = create_food_type(db_connection, "Fruits")
    result = create_food_storage(db_connection, "Apple", -1.0, "kg", food_type["id"], "2022-12-31")
    assert result == "Quantity cannot be negative."


# Integration tests
def test_create_update_delete_food_type(db_connection):
    food_type = create_food_type(db_connection, "Fruits")
    assert food_type["name"] == "Fruits"

    updated_food_type = update_food_type_by_id(db_connection, food_type["id"], "Vegetables")
    assert updated_food_type["name"] == "Vegetables"

    delete_food_type_by_id(db_connection, food_type["id"])
    result = read_food_type_by_id(db_connection, food_type["id"])
    assert result is None


pytest.main(["-v", "--tb=line", "-rN", __file__])
