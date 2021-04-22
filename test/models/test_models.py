from dataclasses import dataclass

from app.schema import FlatMenuSchema
from app.models.models import Menu


def test_menu_schema_loads_coordinate():
    menu = Menu(id=1,
                name="cazuela",
                type="normal")
    json = {
        "id": 1,
        "name": "cazuela",
        "type": "normal",
    }
    assert FlatMenuSchema().load(json) == menu


def test_menu_schema_dumps_coordinate():
    menu = Menu(id=1,
                name="cazuela",
                type="normal")
    json = {
        "id": 1,
        "name": "cazuela",
        "type": "normal",
    }
    assert FlatMenuSchema().dump(menu) == json
