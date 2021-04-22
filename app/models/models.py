import datetime
from dataclasses import dataclass
from enum import Enum
from typing import List
from typing import Union
from typing import Any

@dataclass(frozen=True, eq=True)
class Menu:
    """Menu avaible in restorant"""
    id: int
    name: str
    type: str