# character statistics history class



# Python module imports
import logging
import typing
from datetime import datetime
from typing import List

from flask import flash
from sqlalchemy import  Integer,\
                        String,\
                        Text,\
                        DateTime,\
                        ForeignKey

from sqlalchemy.orm import  relationship,\
                            Mapped,\
                            mapped_column


# internal imports
from pen_n_paperless import db

# prevent cyclic import
if typing.TYPE_CHECKING:
    from .characters import Character




class Entry(db.Model):
    __tablename__ = "table_history_entries"

    _id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)

    # associate the history table in a one-to-many relationship
    _history_id: Mapped[int | None] = mapped_column(ForeignKey('table_history._id'))
    _history: Mapped["History | None"] = relationship("History", back_populates='_entries')


    # Members
    _value: Mapped[int] = mapped_column(Integer, default=0)
    _description: Mapped[str] = mapped_column(Text, default='')
    _timestamp: Mapped[datetime] = mapped_column(DateTime, default=None)

    def __init__(self, value: int, description: str):
        self._value = value
        self._description = description
        self._timestamp = datetime.now()

    @property
    def id(self) -> int:
        return self._id
    @property
    def value(self) -> int:
        return self._value
    @property
    def description(self) -> str:
        return self._description
    @property
    def timestamp(self) -> datetime:
        return self._timestamp




class History(db.Model):
    __tablename__ = "table_history"

    _id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)

    # Connection to Character
    # associate the character table in a one-to-many relationship
    _character_id: Mapped[int] = mapped_column(ForeignKey("table_characters._id"))
    _character: Mapped["Character"] = relationship("Character", back_populates='_histories')

    # Connections to entries
    # associate the entry table in a many-to-one relationship
    _entries: Mapped[List[Entry]] = relationship("Entry", back_populates='_history')



    # Members
    _name: Mapped[str] = mapped_column(String, default='')


    def __init__(self, history_name: str):
        self._name = history_name
        return


    # Methods
    def get_total(self) -> int:
        """
        Calculate the total of the values of each entry.
        
        :param self: Description
        :return: Description
        :rtype: int
        """

        sum = 0

        for entry in self._entries:
            sum += entry.value

        return sum
    
    def add_entry(self, value: int, description: str):

        if type(value) is not int:
            logging.error(f'"{value}" is not an integer. Description: "{description}"')
            return False

        self._entries.append(Entry(value, description))

        print(self._entries)

        db.session.commit()
        print(self._entries)
        flash("New entry added", "success")
        return True
    
    def delete_entry(self, id: int) -> bool:
        """
        Docstring for delete_entry
        
        :param self: Description
        :param id: Description
        :type id: int
        :return: True when entry successfully deleted
        :rtype: bool
        """

        if type(id) is not int:
            logging.error(f'"{id}" is not an integer.')
            return False
        
        print(self._entries)

        for entry in self._entries:
            if entry._id == id:
                self._entries.remove(entry)
                
                flash("Entry removed", "success")
                db.session.commit()
                return True
        
        logging.error(f"Failed to delete entry with ID {id}. Entry not found.")
        flash("Internal error", "error")
        return False
    
    def get_entries(self) -> List:
        return self._entries
    


