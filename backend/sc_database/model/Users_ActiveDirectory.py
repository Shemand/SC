from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship

from backend.sc_database.model.BaseModel import BaseModel


class Users_ActiveDirectory(BaseModel):
    __tablename__ = 'Users_ActiveDirectory'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(64), nullable=False, index=True)
    full_name = Column(String(128), nullable=False)
    department = Column(String(128), nullable=False)
    mail = Column(String(64))
    phone = Column(String(32))
    registred = Column(DateTime)
    last_logon = Column(DateTime)
    isDeleted = Column(DateTime)
    isDisabled = Column(DateTime)
    isLocked = Column(DateTime)
    updated = Column(DateTime, nullable=False, default=datetime.now())
    created = Column(DateTime, nullable=False, default=datetime.now())


    def __repr__(self):
        return f'<Users_ActiveDirectory ({self.user.username})>'