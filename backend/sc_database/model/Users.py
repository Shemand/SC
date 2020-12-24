from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

from backend.sc_database.model.BaseModel import BaseModel
from backend.sc_database.model.Logons import Logons


class Users(BaseModel):
    __tablename__ = 'Users'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    username = Column(String(256), nullable=False)
    full_name = Column(String(256))
    created = Column(DateTime, nullable=False, default=datetime.now())

    logons = relationship('Logons', back_populates='user')

    def __repr__(self):
        return f'<Users ({self.username})>'