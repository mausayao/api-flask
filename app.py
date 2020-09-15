from flask import Flask
from flask.json import jsonify
from flask_jwt_extended import JWTManager
from flask_restful import Api

from blacklist import BLACKLIST
from reources.hotel import Hoteis, Hotel
from reources.usuario import UserLogin, UserLogout, Usuario, UsuarioRegistro, UserConfirm
from reources.site import Site, Sites

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = "teste"
app.config['JWT_BLACKLIST_ENABLED'] = True

api = Api(app)
jwt = JWTManager(app)

@app.before_first_request
def cria_banco():
    banco.create_all()

@jwt.token_in_blacklist_loader
def verifica_black_list(token):
    return token['jti'] in BLACKLIST

@jwt.revoked_token_loader
def token_de_acesso_invalidado():
    return jsonify({'message': 'You have been logged out'}), 401

api.add_resource(Hoteis, '/hoteis')
api.add_resource(Hotel, '/hoteis/<string:hotel_id>')

api.add_resource(UsuarioRegistro, '/usuarios')
api.add_resource(Usuario, '/usuarios/<int:id>')

api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')

api.add_resource(Sites, '/sites')
api.add_resource(Site, '/sites/<int:id>')

api.add_resource(UserConfirm, '/confirm/<int:id>')

if __name__ == '__main__':
    from connection_bd import banco
    banco.init_app(app)
    app.run(host='0.0.0.0', debug=True)