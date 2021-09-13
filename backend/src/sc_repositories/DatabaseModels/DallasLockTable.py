from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship

from .BaseModel import BaseTableModel


class DallasLockTable(BaseTableModel):
    __tablename__ = 'DallasLock'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    Computers_id = Column(Integer, ForeignKey('Computers.id'), nullable=False)
    status = Column(Integer, nullable=False)
    server = Column(String(64), nullable=False)
    isDeleted = Column(DateTime)
    updated = Column(DateTime, nullable=False, default=datetime.now())
    created = Column(DateTime, nullable=False, default=datetime.now())

    def __repr__(self):
        return f'<DallasLock ({self.computer.name})>'
