from sqlalchemy import Column, Integer, String, Boolean

from .BaseModel import BaseTableModel


class OperationSystemsTable(BaseTableModel):
    __tablename__ = 'OperationSystems'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(64), nullable=False)
    isUnix = Column(Boolean, nullable=False)

