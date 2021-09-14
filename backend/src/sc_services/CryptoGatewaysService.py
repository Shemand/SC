from sqlalchemy import select, update, insert, delete

from backend.src.sc_entities.CryptoGateway import CryptoGateway
from backend.src.sc_entities.models import CryptoGateway
from backend.src.sc_services.ServicesInterfaces import ServiceAbstract


class CryptoGatewaysService(ServiceAbstract):

    @staticmethod
    def _return_model_fields(row):
        return {
            "name": row['name'],
            "unit": {
                "name": row['Units_name']
            },
            "address": row['address'],
            "mask": row['mask'],
            "caption": row['caption'],
        }


    def create(self, model: CryptoGateway):
        params = {
            "name": model.name,
            "Units_id": select([self.db.units.c.id]).where(self.db.units.c.name == model.unit.name).limit(1),
            "address": model.address,
            "mask": model.mask,
            "caption": model.caption
        }
        query = insert(self.db.cg).values(**params)
        self.db.engine.execute(query)
        return True

    def delete(self, CG_name):
        query = delete(self.db.cg).where(self.db.cg.c.name == CG_name)
        self.db.engine.execute(query)

    def get(self, CG_name):
        fields = [self.db.cg.c.name,
                  self.db.cg.c.address,
                  self.db.cg.c.mask,
                  self.db.cg.c.caption,
                  self.db.units.c.name.label('Units_name')]
        query = select(fields).join(self.db.units, self.db.units.c.id == self.db.cg.c.Units_id, isouter=True).where(self.db.cg.c.name == CG_name).limit(1)
        row = self.db.engine.execute(query).fetchone()
        if not row:
            return None
        return CryptoGateway(**type(self)._return_model_fields(row))

    def all(self):
        fields = [self.db.cg.c.name,
                  self.db.cg.c.address,
                  self.db.cg.c.mask,
                  self.db.cg.c.caption,
                  self.db.units.c.name.label('Units_name')]
        query = select(fields).join(self.db.units, self.db.units.c.id == self.db.cg.c.Units_id, isouter=True)
        rows = self.db.engine.execute(query).fetchall()
        return [CryptoGateway(**type(self)._return_model_fields(row)) for row in rows]