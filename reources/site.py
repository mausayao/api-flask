from flask_restful import Resource, reqparse
from models.site import SiteModel
from flask_jwt_extended import jwt_required


arg = reqparse.RequestParser()
arg.add_argument('nome', type=str, required=True, help='Nome é obrigatório')

class Sites(Resource):

    def get(self):
        return [site.json() for site in SiteModel.query.all()]

    @jwt_required
    def post(self):
        dados = arg.parse_args()
        if SiteModel.query.filter_by(nome=dados['nome']):
            return {'message', 'Site já cadastrado'}, 400

        site = SiteModel(dados['nome'])

        try:
            site.save()
        except:
            return {'message': 'Internal error'}, 500
        return site.json(), 201


class Site(Resource):

    def get(self, id:int):
        site = SiteModel.findy_by(id)
        if site is None:
            return 404
        return site.json(), 200

    @jwt_required
    def put(self, id:int):
        site = SiteModel.findy_by(id)
        if site is None:
            return 404

        try:
            site.save()
        except:
            return {'message': 'Internal error'}, 500
        return site.json(), 200

    @jwt_required
    def delete(self, id:int):
        site = SiteModel.findy_by(id)
        if site is None:
            return 404
        try:
            site.delete()
        except:
            return {'message': 'Internal error'}, 500
        return 200
