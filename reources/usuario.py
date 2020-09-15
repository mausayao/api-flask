from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token, jwt_required, get_raw_jwt
from werkzeug.security import safe_str_cmp
from blacklist import BLACKLIST

from models.usuario import UsuarioModel

arg = reqparse.RequestParser()
arg.add_argument('login', type=str, required=True,
                 help='Usuário é obrigatório')
arg.add_argument('senha', type=str, required=True, help='Senha é obrigatório')
arg.add_argument('ativado', type=bool, default=False)


class Usuario(Resource):

    def get(self, id: int):
        usuario = UsuarioModel.find_by_id(id)
        if usuario:
            return usuario.json(), 200
        return {'message': 'Nenhum usuário foi encontrado'}, 404

    def delete(self, id: int):
        usuario = UsuarioModel.find_by_id(id)
        if usuario:
            try:
                usuario.delete()
                return 200
            except:
                return {'message', 'An internal error'}, 500

        return {'message': 'Nenhum usuário foi encontrado'}, 404


class UsuarioRegistro(Resource):

    def post(self):
        dados = arg.parse_args()

        if UsuarioModel.find_by_login(dados['login']):
            return {'message': 'Usuário já cadastrado'}, 400

        novo_usuario = UsuarioModel(**dados)
        novo_usuario.ativado = False
        try:
            novo_usuario.save()
        except:
            return {'message': 'An server error'}, 500

        return novo_usuario.json(), 201

class UserLogin(Resource):

    @classmethod
    def post(cls):
        dados = arg.parse_args()

        user = UsuarioModel.find_by_login(dados['login'])

        if user and safe_str_cmp(user.senha, dados['senha']):
            if not user.ativado:
                return {'message', 'Usuário não ativado'}, 401
            token = create_access_token(identity=user.user_id)
            return {'token': token}, 200
        return {'message', 'Usuário ou senha incorreto'}, 401


class UserLogout(Resource):

    @jwt_required
    def post(self):
        jwt_id = get_raw_jwt()['jti']
        BLACKLIST.add(jwt_id)
        return {'message': 'Logged out successfully'}, 200


class UserConfirm(Resource):

    @classmethod
    def get(csl, id):
        usuario = UsuarioModel.find_by_id(id)

        if not usuario:
            return {'message', 'user not found'}, 404
        
        usuario.ativado = True
        try:
            usuario.save()
        except:
            return {'message': 'An server error'}, 500

        return {'message', 'Usuário ativado com sucesso'}, 200


