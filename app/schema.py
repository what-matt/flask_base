import marshmallow
import marshmallow_dataclass

from app.models import Menu

# This Menu schema is used to serialize and deserialize a Menu to and from a
# "flat" hash in Redis. That is, the Menu's Coordinate is flattened to
# top-level "lat" and "lng" keys. This is because Redis Hashes cannot contain
# nested values.
FlatMenuSchema = marshmallow_dataclass.class_schema(Menu)

# This Menu schema is used to serialize a Menu to and from a nested JSON object
# used by the frontend to display menu data.
MenuSchema = marshmallow_dataclass.class_schema(Menu)

# This Menu schema is used to serialize a Menu to and from a nested JSON object
# used by the frontend to display menu data.
MenuSchema = marshmallow_dataclass.class_schema(Menu)

