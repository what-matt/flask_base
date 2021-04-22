from flask_restful import abort

from app.api.base import DaoResource
from app.schema import MenuSchema

class MenuListResource(DaoResource):
  def get(self):
        return MenuSchema(many=True).dump(self.dao.find_all())

class MenuResource(DaoResource):
    def get(self, menu_id):
        menu = self.dao.find_by_id(menu_id)
        if not menu:
            return abort(404, message=f"Menu {menu_id} does not exist")
        return MenuSchema().dump(menu)