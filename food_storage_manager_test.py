# Importing the necessary functions and libraries.
from food_storage_manager import *
import pytest


@pytest.fixture
def db_connection():
    connection, cursor = database_connection()
    yield cursor
    connection.close()


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
    create_food_type(db_connection, "Fruits")
    result = update_food_type_by_id(db_connection, 1, "Vegetables")
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
    food_storage = create_food_storage(db_connection, "Apple", 1.0, "kg", food_type["id"], "2022-12-31")
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
    result = update_food_storage_by_id(db_connection, food_storage["id"], "Banana", 2.0, "kg", food_type["id"], "2023-12-31")
    assert result['name'] == "Banana"


def test_update_non_existing_food_storage_by_id(db_connection):
    result = update_food_storage_by_id(db_connection, 999, "Banana", 2.0, "kg", 1, "2023-12-31")
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


# If you want to run the tests directly from this file, uncomment the line below
pytest.main(["-v", "--tb=line", "-rN", __file__])
