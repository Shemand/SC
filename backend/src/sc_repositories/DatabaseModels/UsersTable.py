from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from .BaseModel import BaseTableModel
# from backend.sc_database.model.Logons import Logons


class Users(BaseTableModel):
    __tablename__ = 'Users'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    login = Column(String(256), nullable=False, index=True)
    privileges = Column(Integer, nullable=False, default=1) # 0 - is blocked, 1 - is active,
    created = Column(DateTime, nullable=False, default=datetime.now())
    Users_ActiveDirectory_id = Column(Integer, ForeignKey('Users_ActiveDirectory.id'))
    Units_id = Column(Integer, ForeignKey('Units.id'), nullable=False)

    # logons = relationship('Logons', back_populates='user')

    def __repr__(self):
        return f'<Users ({self.username})>'