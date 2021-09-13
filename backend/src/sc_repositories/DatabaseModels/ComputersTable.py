from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship

from .AdaptersTable import AdaptersTable
from .BaseModel import BaseTableModel
from .Logons import Logons


class ComputersTable(BaseTableModel):
    __tablename__ = 'Computers'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(128), nullable=False, unique=True, index=True)
    comment = Column(Text)
    created = Column(DateTime, nullable=False, default=datetime.now())
    Units_id = Column(Integer, ForeignKey('Units.id'), nullable=False)

    def __repr__(self):
        return f'<Computers (name: {self.name})>'
