from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from pop_fibras.models import Dio, User, Local

dio_get_parser = reqparse.RequestParser()
dio_get_parser.add_argument('id', help = 'This field cannot be blank', required=True, type=int)

dio_post_parser = reqparse.RequestParser()
dio_post_parser.add_argument('nome', help = 'This field cannot be blank', required=True)
dio_post_parser.add_argument('local_id', help = 'This field cannot be blank and must be int', required=True, type=int)
dio_post_parser.add_argument('observacao', help = 'This field cannot be blank', required=False)

dio_update_parser = dio_post_parser.copy()
dio_update_parser.add_argument('id', help = 'This field cannot be blank', required=True, type=int)
dio_update_parser.remove_argument('local_id')

dio_delete_parser = dio_get_parser.copy()
dio_delete_parser.add_argument('password', help = 'This field cannot be blank', required=True)
class DiosResource(Resource):
    @jwt_required
    def get(self):
        return Dio.all_to_json()

class DioResource(Resource):
    @jwt_required
    def get(self):
        data = dio_get_parser.parse_args()
        try:
            dio = Dio.query.filter_by(id=data['id']).first()
            if dio:
                dio_json = dio.to_json()
                dio_json.update(dio.portas_to_json())
                return dio_json
            return {'message': 'Invalid Dio ID'}
        except:
            return {'message': 'Something went wrong'}, 500

    @jwt_required
    def post(self):
        data = dio_post_parser.parse_args()
        if Dio.query.filter_by(nome=data['nome'], local_id=data['local_id']).first():
            return {'message': 'Dio {} already exists in this local.'.format(data['nome'])}
        local = Local.query.filter_by(id=data['local_id']).first()
        if not local:
            return {'message': 'Invalid Local Id'}
        dio = Dio(nome=data['nome'], observacao=data['observacao'], local=local)
        try:
            dio.save()
            return {
                'message': 'Dio {} was created'.format(data['nome']),
                }
        except:
            return {'message': 'Something went wrong'}, 500

    @jwt_required
    def patch(self):
        data = dio_update_parser.parse_args()
        dio = Dio.query.filter_by(id=data['id']).first()
        if not dio:
            return {'message': 'Invalid Dio Id'}
        if Dio.query.filter_by(nome=data['nome'], local_id=dio.local_id).first():
            return {'message': 'Dio {} already exists in this local.'.format(data['nome'])}
        dio.nome = data['nome']
        dio.observacao = data['observacao']
        try:
            dio.save()
            return {
                'message': 'Dio {} was Updated'.format(data['id']),
                }
        except:
            raise
            return {'message': 'Something went wrong'}, 500

        
    @jwt_required
    def delete(self):
        data = dio_delete_parser.parse_args()
        try:
            user = User.query.filter_by(username=get_jwt_identity()).first()
            if user.check_password(data['password']):
                dio = Dio.query.filter_by(id=data['id']).first()
                if dio:
                    dio.delete()
                    return {'message': 'Dio {} was deleted'.format(data['id'])}
                return {'message':'Invalid Dio ID'}
            return {'message':'Invalid password for current User.'}, 403
        except:
            return {'message': 'Something went wrong'}, 500