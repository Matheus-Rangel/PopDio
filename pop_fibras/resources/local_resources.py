from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from pop_fibras.models import Local, User

local_get_parser = reqparse.RequestParser()
local_get_parser.add_argument('id', help = 'This field cannot be blank', required=True, type=int)

local_post_parser = reqparse.RequestParser()
local_post_parser.add_argument('nome', help = 'This field cannot be blank', required=True)
local_post_parser.add_argument('observacao', help = 'This field cannot be blank', required=True)

local_update_parser = local_post_parser.copy()
local_update_parser.add_argument('id', help = 'This field cannot be blank', required=True, type=int)

local_delete_parser = local_get_parser.copy()
local_delete_parser.add_argument('password', help = 'This field cannot be blank', required=True)
class LocaisResource(Resource):
    @jwt_required
    def get(self):
        return Local.all_to_json()

class LocalResource(Resource):
    @jwt_required
    def get(self):
        data = local_get_parser.parse_args()
        try:
            local = Local.query.filter_by(id=data['id']).first()
            if local:
                local_json = local.to_json()
                local_json.update(local.dios_to_json())
                return local_json
            return {'message': 'Invalid Local ID'}, 400
        except:
            return {'message': 'Something went wrong'}, 500


    @jwt_required
    def post(self):
        data = local_post_parser.parse_args()
        if Local.find_by_nome(data['nome']):
            return {'message': 'Local {} already exists.'.format(data['nome'])}, 400
        local = Local(nome=data['nome'], observacao=data['observacao'])
        try:
            local.save()
            return local.to_json()
        except:
            return {'message': 'Something went wrong'}, 500
    
    @jwt_required
    def patch(self):
        data = local_update_parser.parse_args()
        try:
            local = Local.query.filter_by(id=data['id']).first() 
            if local:
                local.nome = data['nome']
                local.observacao = data['observacao']
                local.save()
                return local.to_json()
            return {'message':'Invalid Local ID'}, 400
        except:
            return {'message': 'Something went wrong'}, 500
    
    @jwt_required
    def delete(self):
        data = local_delete_parser.parse_args()
        try:
            user = User.query.filter_by(username=get_jwt_identity()).first()
            if user.check_password(data['password']):
                local = Local.query.filter_by(id=data['id']).first()
                if local:
                    local.delete()
                    return {'message': 'Local {} was deleted'.format(data['id'])}
                return {'message':'Invalid Local ID'}
            return {'message':'Invalid password for current User.'}, 412
        except:
            raise
            return {'message': 'Something went wrong'}, 500
