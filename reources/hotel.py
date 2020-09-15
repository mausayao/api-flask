
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from filtros import normalize_path, consulta_com_cidade, consulta_sem_cidade
from models.hotel import HotelModel
from models.site import SiteModel
import sqlite3

args = reqparse.RequestParser()
args.add_argument('nome', type=str, required=True, help='Nome is required')
args.add_argument('estrelas', type=float, required=True,
                  help='Estrelas is required')
args.add_argument('diaria', type=float, required=True,
                  help='Diaria is required')
args.add_argument('cidade', type=str, required=True, help='Cidade is required')
args.add_argument('site_id', type=int, required=True, help='Site é um campo obrigatório')

#pesquisa
path_params = reqparse.RequestParser()
path_params.add_argument('cidade', type=str)
path_params.add_argument('estrelas_min', type=float)
path_params.add_argument('estrelas_max', type=float)
path_params.add_argument('diaria_min', type=float)
path_params.add_argument('diaria_max', type=float)
path_params.add_argument('limit', type=int)
path_params.add_argument('offset', type=int)


class Hoteis(Resource):

    def get(self):
        connection = sqlite3.connect('banco.db')
        cursor = connection.cursor()

        dados = path_params.parse_args()
        dados_validos = {chave:dados[chave] for chave in dados if dados[chave] is not None}
        parametros = normalize_path(**dados_validos)
        valores = tuple([parametros[chave] for chave in parametros])
        
        if not parametros.get('cidade'):
            resultado = cursor.execute(consulta_sem_cidade, valores)
        else:
            resultado = cursor.execute(consulta_com_cidade, valores)

        hoteis = []

        for linha in resultado:
            hoteis.append(
                {
                'hotel_id': linha[0],
                'nome': linha[1],
                'estrelas': linha[2],
                'diaria': linha[3],
                'cidade': linha[4]
                }
            )

        return {'hoteis': hoteis}

    @jwt_required
    def post(self):

        dados = args.parse_args()

        if SiteModel.findy_by_id(dados['site_id']) is None:
            return {'message': 'error'}, 404

        novo_hotel = HotelModel(
                                dados['nome'],
                                dados['estrelas'],
                                dados['diaria'],
                                dados['cidade'],
                                dados['site_id']
                                )
        try:
            novo_hotel.save()
        except:
            return {'message' : 'An internal server error'}, 500
        return novo_hotel.json(), 201


class Hotel(Resource):

    def get(self, hotel_id: int):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel is not None:
            return hotel.json()
        return {'message': 'Hotel not found'}, 404

    @jwt_required
    def delete(self, hotel_id:int):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel is None:
            return {'message': 'The Hotel doesn\'t exist'}, 404

        try:
            hotel.delete()
        except:
            return {'message' : 'An internal server error'}, 500
        return 200

    @jwt_required
    def put(self, hotel_id: int):
        hotel = HotelModel.find_hotel(hotel_id)

        if hotel is None:
            return {'message': 'The Hotel doesn\'t exist'}, 404

        dados = args.parse_args()

        hotel.nome = dados['nome']
        hotel.estrelas = dados['estrelas']
        hotel.diaria = dados['diaria']
        hotel.cidade = dados['cidade']

        try:
            hotel.save()
        except:
            return {'message' : 'An internal server error'}, 500

        return hotel.json(), 200

