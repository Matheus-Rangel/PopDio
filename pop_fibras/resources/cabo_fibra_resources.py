from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from pop_fibras.models import CaboFibra

cabo_get_parser = reqparse.RequestParser()
cabo_get_parser.add_argument('id', help = 'This field cannot be blank', required=True, type=int)

cabo_post_parser = reqparse.RequestParser()
cabo_post_parser.add_argument('nome', help = 'This field cannot be blank', required=True)
cabo_post_parser.add_argument('quantidade_fibras', help = 'This field cannot be blank', required=True, type=int)
cabo_post_parser.add_argument('observacao', help = 'This field cannot be blank', required=True)

cabo_update_parser = cabo_post_parser.copy()
cabo_update_parser.add_argument('id', help = 'This field cannot be blank', required=True, type=int)
cabo_update_parser.remove_argument('quantidade_fibras')

cabo_delete_parser = cabo_get_parser.copy()
class CabosResource(Resource):
    @jwt_required
    def get(self):
        return CaboFibra.all_to_json()

class CaboResource(Resource):
    @jwt_required
    def get(self):
        data = cabo_get_parser.parse_args()
        try:
            cabo = CaboFibra.query.filter_by(id=data['id']).first()
            if cabo:
                return cabo.to_json()
            return {'message': 'Invalid Cabo ID'}
        except:
            return {'message': 'Something went wrong'}, 500


    @jwt_required
    def post(self):
        data = cabo_post_parser.parse_args()
        if CaboFibra.find_by_nome(data['nome']):
            return {'message': 'Cabo {} already exists.'.format(data['nome'])}
        cabo = CaboFibra(nome=data['nome'], quantidade_fibras=data['quantidade_fibras'], observacao=data['observacao'])
        try:
            cabo.save()
            return {
                'message': 'Cabo {} was created'.format(data['nome']),
                }
        except:
            return {'message': 'Something went wrong'}, 500
    
    @jwt_required
    def patch(self):
        data = cabo_update_parser.parse_args()
        try:
            cabo = CaboFibra.query.filter_by(id=data['id']).first() 
            if cabo:
                cabo.nome = data['nome']
                cabo.observacao = data['observacao']
                cabo.save()
                return {
                    'message': 'Cabo {} was updated'.format(data['id']),
                }
            return {'message':'Invalid Cabo ID'}
        except:
            return {'message': 'Something went wrong'}, 500
    
    @jwt_required
    def delete(self):
        data = cabo_delete_parser.parse_args()
        try:
            cabo = CaboFibra.query.filter_by(id=data['id']).first()
            if cabo:
                cabo.delete()
                return {'message': 'Cabo {} was deleted'.format(data['id'])}
            return {'message':'Invalid Cabo ID'}
        except:
            return {'message': 'Something went wrong'}, 500
