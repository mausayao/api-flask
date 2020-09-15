from connection_bd import banco


class UsuarioModel(banco.Model):
    __tablename__ = 'usuarios'

    user_id = banco.Column(banco.Integer, primary_key=True, autoincrement=True)
    login = banco.Column(banco.String(40))
    senha = banco.Column(banco.String(40))
    email = banco.Column(banco.String(40))
    ativado = banco.Column(banco.Boolean, default=False)

    def __init__(self, login, senha, email, ativado):
        self.login = login
        self.senha = senha
        self.email = email
        self.ativado = ativado

    def json(self):
        return {
            'login': self.login,
            'email': self.email,
            'ativado': self.ativado
        }

    @classmethod
    def find_by_id(cls, id):
        user = cls.query.filter_by(user_id=id).first()
        if user:
            return user
        return None

    @classmethod
    def find_by_login(cls, login):
        user = cls.query.filter_by(login=login).first()
        if user:
            return user
        return None

    def save(self):
        banco.session.add(self)
        banco.session.commit()
    
    def delete(self):
        banco.session.delete(self)
        banco.session.commit()