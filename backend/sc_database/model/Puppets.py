from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship

from backend.sc_database.model.BaseModel import BaseModel


class Puppets(BaseModel):
    __tablename__ = 'Puppets'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    Computers_id = Column(Integer, ForeignKey('Computers.id'), nullable=False)
    enviroment = Column(String(64), nullable=False)
    last_visible = Column(DateTime, nullable=False, default=datetime.now())
    updated = Column(DateTime, nullable=False, default=datetime.now())
    created = Column(DateTime, nullable=False, default=datetime.now())

    computer = relationship('Computers', backref='puppet')

    def __repr__(self):
        return f'<Puppets ({self.computer.name})>'