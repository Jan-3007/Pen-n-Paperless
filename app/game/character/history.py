from ... import db

import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.orm import relationship, Mapped, mapped_column
import typing
if typing.TYPE_CHECKING:
    from .character import Character

from ...strings import Strings, Messages



class XPHistory(db.Model):
    __tablename__ = "xp_history_table"

    # database connections
    _id: Mapped[int] = mapped_column(primary_key=True)
    _character_id: Mapped[int] = mapped_column(ForeignKey('character_table._id'))
    _character: Mapped["Character"] = relationship(back_populates="_new_xp_history")
    

    # properties
    _value = db.Column(db.Integer, default=0)
    _description = db.Column(db.String(255), default="")
    _timestamp = db.Column(db.String(100), default="")


    def __str__(self):
        return f"Contains a history entry of the character."
    
    def __repr__(self):
        return f"<HistoryEntry id: {self._id}.>"
    
    def __init__(self, value:int, description:str):
        self._value = value
        self._description = description
        self._timestamp = datetime.datetime.now()
        


    def get_properties(self) -> dict:
        """returns the properties of this history entry as a dict"""
        return {
            Strings.entry_number.value: self._id,
            Strings.val.value: self._value,
            Strings.description.value: self._description,
            Strings.timestamp.value: self._timestamp,
        }
    


class HPHistory(db.Model):
    __tablename__ = "hp_history_table"

    # database connections
    _id: Mapped[int] = mapped_column(primary_key=True)
    _character_id: Mapped[int] = mapped_column(ForeignKey('character_table._id'))
    _character: Mapped["Character"] = relationship(back_populates="_new_hp_history")
    

    # properties
    _value = db.Column(db.Integer, default=0)
    _description = db.Column(db.String(255), default="")
    _timestamp = db.Column(db.String(100), default="")


    def __str__(self):
        return f"Contains a history entry of the character."
    
    def __repr__(self):
        return f"<HistoryEntry id: {self._id}. >"
    
    def __init__(self, value:int, description:str):
        self._value = value
        self._description = description
        self._timestamp = datetime.datetime.now()
        


    def get_properties(self) -> dict:
        """returns the properties of this history entry as a dict"""
        return {
            Strings.entry_number.value: self._id,
            Strings.val.value: self._value,
            Strings.description.value: self._description,
            Strings.timestamp.value: self._timestamp,
        }
    


    