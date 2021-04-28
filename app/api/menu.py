from typing import Tuple

from flask_restful import abort
from webargs.flaskparser import use_args, parser

from app.api.base import DaoResource
from app.models import Menu
from app.schema import MenuSchema

class MenuListResource(DaoResource):
    @use_args(MenuSchema, location='json')
    def post(self, menu: Menu) -> Tuple[str, int]:
        self.dao.insert(menu)
        return "Accepted", 202

    def get(self):
        return MenuSchema(many=True).dump(self.dao.find_all())

class MenuResource(DaoResource):
    def get(self, menu_id):
        menu = self.dao.find_by_id(menu_id)
        if not menu:
            return abort(404, message=f"Menu {menu_id} does not exist")
        return MenuSchema().dump(menu)


@parser.error_handler
def handle_request_parsing_error(err, req, schema, *, error_status_code, error_headers):
    """webargs error handler that uses Flask-RESTful's abort function to return
    a JSON error response to the client.
    """
    abort(error_status_code if error_status_code else 400 , errors=err.messages)

