from datetime import datetime

from sqlalchemy import Column, Integer, String

from backend.sc_database.model.BaseModel import BaseModel


class Units(BaseModel):
    __tablename__ = 'Units'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(64), nullable=False, unique=True, default=datetime.now())
    root_id = Column(Integer)

    def __repr__(self):
        return f'<Units ({self.name})>'