from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from pop_fibras.models import EstadoLink
import re

estado_get_parser = reqparse.RequestParser()
estado_get_parser.add_argument('id', help = 'This field cannot be blank', required=True, type=int)

estado_post_parser = reqparse.RequestParser()
estado_post_parser.add_argument('nome', help = 'This field cannot be blank', required=True)
estado_post_parser.add_argument('cor', help = 'This field cannot be blank', required=True)
estado_post_parser.add_argument('observacao', help = 'This field cannot be blank', required=True)

estado_update_parser = estado_post_parser.copy()
estado_update_parser.add_argument('id', help = 'This field cannot be blank', required=True, type=int)

estado_delete_parser = estado_get_parser.copy()

def is_hex_color(str):
    return re.search(r'(^#[0-9a-f]{6}$)|(^#[0-9a-f]{3}$)', str)
    
class EstadosResource(Resource):
    @jwt_required
    def get(self):
        return EstadoLink.all_to_json()

class EstadoResource(Resource):
    @jwt_required
    def get(self):
        data = estado_get_parser.parse_args()
        try:
            estado = EstadoLink.query.filter_by(id=data['id']).first()
            if estado:
                return estado.to_json()
            return {'message': 'Invalid Estado ID'}
        except:
            return {'message': 'Something went wrong'}, 500


    @jwt_required
    def post(self):
        data = estado_post_parser.parse_args()
        if EstadoLink.find_by_nome(data['nome']):
            return {'message': 'Estado {} already exists.'.format(data['nome'])}
        if not is_hex_color(data['cor']):
            return {'message': '{} is not a valid hex color code.'.format(data['cor'])}
        
        estado = EstadoLink(nome=data['nome'], cor=data['cor'], observacao=data['observacao'])
        try:
            estado.save()
            return {
                'message': 'Estado {} was created'.format(data['nome']),
                }
        except:
            return {'message': 'Something went wrong'}, 500
    
    @jwt_required
    def patch(self):
        data = estado_update_parser.parse_args()
        try:
            if not is_hex_color(data['cor']):
                return {'message': '{} is not a valid hex color code.'.format(data['cor'])}
            estado = EstadoLink.query.filter_by(id=data['id']).first() 
            if estado:
                estado.nome = data['nome']
                estado.cor = data['cor']
                estado.observacao = data['observacao']
                estado.save()
                return {
                    'message': 'Estado {} was updated'.format(data['id']),
                }
            return {'message':'Invalid Estado ID'}
        except:
            return {'message': 'Something went wrong'}, 500
    
    @jwt_required
    def delete(self):
        data = estado_delete_parser.parse_args()
        try:
            estado = EstadoLink.query.filter_by(id=data['id']).first()
            if estado:
                estado.delete()
                return {'message': 'Estado {} was deleted'.format(data['id'])}
            return {'message':'Invalid Estado ID'}
        except:
            return {'message': 'Something went wrong'}, 500
