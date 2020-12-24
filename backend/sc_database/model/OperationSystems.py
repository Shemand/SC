from sqlalchemy import Column, Integer, String, Boolean

from backend.sc_database.model.BaseModel import BaseModel


class OperationSystems(BaseModel):
    __tablename__ = 'OperationSystems'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(64), nullable=False)
    isUnix = Column(Boolean, nullable=False)

    def __repr__(self):
        return f'<OperationSystems ({self.name})>'