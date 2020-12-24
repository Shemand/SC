from sqlalchemy import Column, Integer, ForeignKey, String

from backend.sc_database.model.BaseModel import BaseModel


class CryptoGateways(BaseModel):
    __tablename__ = 'CryptoGateways'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    Units_id = Column(Integer, ForeignKey('Units.id'), nullable=False)
    address = Column(String(16), nullable=False)
    mask = Column(Integer, nullable=False)
    caption = Column(String(128), nullable=False)
    name = Column(String(5), nullable=False)

    def __repr__(self):
        return f'<CryptoGateways ({self.name})>'