from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship

from backend.sc_database.model.BaseModel import BaseModel


class Computers_ActiveDirectory(BaseModel):
    __tablename__ = 'Computers_ActiveDirectory'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    Computers_id = Column(Integer, ForeignKey('Computers.id'), nullable=False)
    isDeleted = Column(DateTime)
    last_visible = Column(DateTime)
    isActive = Column(Boolean, default=True)
    registred = Column(DateTime, nullable=False)
    updated = Column(DateTime, nullable=False, default=datetime.now())
    created = Column(DateTime, nullable=False, default=datetime.now())

    # computer = relationship('Computers', backref='active_directory')

    def __repr__(self):
        return f'<Computers_ActiveDirectory ({self.computer.name})>'