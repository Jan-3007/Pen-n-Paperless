from ... import db

from flask import flash

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column


from ..profession import Profession
from ...strings import Strings



class Statistics(db.Model):
    __tablename__ = "statistics_t"

    _id: Mapped[int] = mapped_column(primary_key=True)
    _character_id: Mapped[int] = mapped_column(ForeignKey('character_table._id'))
    _character: Mapped["Character"] = relationship(back_populates="_statistics")




    _level = db.Column(db.Integer, default=1)
    _experience = db.Column(db.Integer, default=0)
    _max_hp = db.Column(db.Integer, default=10)
    _current_hp = db.Column(db.Integer, default=10)
    
    def __str__(self):
        return f"Statistics of the player"
    
    def __repr__(self):
        return f"<Statistics of the player: Level: {self._level}, Experience: {self._experience}, Max HP: {self._max_hp}, Current HP: {self._current_hp}. Contains methods to modify and retrieve statistics.>"
    

    @property
    def level(self) -> int:
        return self._level
    @level.setter
    def Level(self, value: int):
        self._level = value

    @property
    def Experience(self) -> int:
        return self._experience
    
    @property
    def Max_HP(self) -> int:
        return self._max_hp
    
    @property
    def Current_HP(self) -> int:
        return self._current_hp
    


    def _update_max_hp(self, attribute_bonuses: dict, profession: str) -> int:
        # TODO error: when no max_hp in profession, use max_hp of specialization
        hp = ( attribute_bonuses().get(Strings.Attributes.endurance_bonus.value)
              + Profession.get_properties(profession).get(Strings.Statistics.max_hp.value, 0)
              ) * self._level

        self._max_hp = hp

        self._update_current_hp()
        db.session.commit()
        return

    def _update_current_hp(self):

        hp = self._max_hp

        for entry in self._new_hp_history:
            # stored value has to be negative in order to be interpreted as damage
            hp += int(entry.get_properties().get(Strings.val.value, 0))

        if hp <= 0:
            hp = 0
            flash('Health critical', 'error')

        print(f"New HP: {hp}")
        self._current_hp = hp

        db.session.commit()
        return