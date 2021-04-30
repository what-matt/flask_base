from dataclasses import dataclass
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
@dataclass(frozen=True, eq=True)
class Menu:
    """Menu avaible in restorant"""
    id: int
    name: str
    type: str

    def __repr__(self):
        return f"Menu('{self.id}', '{self.name}', '{self.type}')"

class MenuModel(db.Model):
    """Menu avaible in restorant"""
    __tablename__ = 'menu'
    id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("name", db.String(100))
    type = db.Column("type", db.String(100))

    def __repr__(self):
        return f"Menu('{self.id}', '{self.name}', '{self.type}')"
