from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship

from backend.sc_database.model.BaseModel import BaseModel


class Users_ActiveDirectory(BaseModel):
    __tablename__ = 'Users_ActiveDirectory'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    Users_id = Column(Integer, ForeignKey('Users.id'), nullable=False)
    Units_id = Column(Integer, ForeignKey('Units.id'), nullable=False)
    first_name = Column(String(64), nullable=False)
    second_name = Column(String(64), nullable=False)
    mail = Column(String(64))
    registred = Column(DateTime)
    updated = Column(DateTime, nullable=False, default=datetime.now())
    created = Column(DateTime, nullable=False, default=datetime.now())

    user = relationship('Users', backref='active_directory')

    def __repr__(self):
        return f'<Users_ActiveDirectory ({self.user.username})>'