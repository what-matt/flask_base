import pytest

from app.dao.base import MenuNotFound
from app.dao.redis import MenuDaoRedis
from app.models import Menu


@pytest.fixture
def menu_dao(redis, key_schema):
    yield MenuDaoRedis(redis, key_schema)


def test_does_not_exist(menu_dao):
    with pytest.raises(MenuNotFound):
        menu_dao.find_by_id(0)


def test_insert(redis, menu_dao):
    menu = Menu(id=1,
                name="cazuela",
                type="normal")

    menu_dao.insert(menu)
    assert menu_dao.find_by_id(1) == menu


def test_insert_many(menu_dao):
    menu1 = Menu(id=1,
                name="cazuela",
                type="normal")

    menu2 = Menu(id=2,
                name="porotos",
                type="vegetariana")

    menu3 = Menu(id=3,
                name="humitas",
                type="vegana")

    menu_dao.insert_many(menu1, menu2, menu3)

    assert menu_dao.find_by_id(1) == menu1
    assert menu_dao.find_by_id(2) == menu2
    assert menu_dao.find_by_id(3) == menu3


def test_find_by_id_existing_menu(menu_dao):
    menu_id = 1
    menu = Menu(id=menu_id,
                name="cazuela",
                type="normal")

    menu_dao.insert(menu)
    found_menu = menu_dao.find_by_id(menu_id)

    assert found_menu == menu


def test_find_all(menu_dao):
    menu1 = Menu(id=1,
                name="cazuela",
                type="normal")

    menu2 = Menu(id=2,
                name="porotos",
                type="vegetariana")

    menu3 = Menu(id=3,
                name="humitas",
                type="vegana")

    menu_dao.insert_many(menu1, menu2, menu3)
    assert menu_dao.find_all() == {menu1, menu2, menu3}
