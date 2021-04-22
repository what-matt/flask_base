from flask_restful import abort

from app.api.base import DaoResource
from app.schema import MenuSchema

class MenuResource(DaoResource):
  def get(self):
        return MenuSchema(many=True).dump(self.dao.find_all())