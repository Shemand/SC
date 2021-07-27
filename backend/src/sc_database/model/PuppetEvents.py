from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, String, Text, DateTime

from .BaseModel import BaseModel


class PuppetEvents(BaseModel):
    __tablename__ = 'PuppetEvents'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    Puppets_id = Column(Integer, ForeignKey('Puppets.id'), nullable=False)
    title = Column(String(256), nullable=False, index=True)
    message = Column(Text)
    created = Column(DateTime, nullable=False, default=datetime.now())

    def __repr__(self):
        return f'<PuppetEvents ({self.title})>'