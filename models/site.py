from connection_bd import banco

class SiteModel(banco.Model):
    __tablename__ = 'sites'

    site_id = banco.Column(banco.Integer, primary_key=True, autoincrement=True)
    nome = banco.Column(banco.String(80))
    hoteis = banco.relationship('HotelModel')

    def __init__(self, nome):
        self.nome - nome

    def json(self):
        return {
            'site_id': self.site_id,
            'nome': self.nome,
            'hoteis': [hotel.json() for hotel in self.hoteis]
        }

    @classmethod
    def findy_by(cls, nome):
        site =  cls.query.filter_by(nome=nome).first()
        if site:
            return site
        return None

    @classmethod
    def findy_by_id(cls, id):
        site =  cls.query.filter_by(id=id).first()
        if site:
            return site
        return None

    def save(self):
        banco.session.add(self)
        banco.session.commit()

    def delete(self):
        if len(self.hoteis) > 0:
            [hotel.delete() for hotel in self.hoteis]
        banco.session.delete(self)
        banco.session.commit()