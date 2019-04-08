from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from pop_fibras.models import DioPorta
from sqlalchemy.exc import IntegrityError
porta_get_parser = reqparse.RequestParser()
porta_get_parser.add_argument('id', help = 'This field cannot be blank', required=True, type=int)

porta_post_parser = reqparse.RequestParser()
porta_post_parser.add_argument('porta_destino_id', help = 'ID cannot be converted to integer', required=False, type=int)
porta_post_parser.add_argument('dio_id', help = 'This field cannot be blank', required=True, type=int)
porta_post_parser.add_argument('numero_porta', help = 'This field cannot be blank', required=True, type=int)
porta_post_parser.add_argument('estado_link_id', help = 'ID cannot be converted to integer', required=False, type=int)
porta_post_parser.add_argument('fibra_cabo_id', help = 'ID cannot be converted to integer', required=False, type=int)
porta_post_parser.add_argument('fibra_numero', help = 'Fibra Numero cannot be converted to integer', required=False, type=int)
porta_post_parser.add_argument('switch_porta', help = 'Identificação da porta do switch ao qual está conectada', required=False)
porta_post_parser.add_argument('observacao', required=False)
porta_post_parser.add_argument('porta_bypass_id', help = 'porta_bypass', required=False, type=int)

porta_update_parser = porta_post_parser.copy()
porta_update_parser.remove_argument('dio_id')
porta_update_parser.add_argument('id', help = 'This field cannot be blank', required=True, type=int)

porta_delete_parser = porta_get_parser.copy()

class PortaResource(Resource):
    @jwt_required
    def get(self):
        data = porta_get_parser.parse_args()
        try:
            porta = DioPorta.query.filter_by(id=data['id']).first()
            if porta:
                return porta.to_json()
            return {'message': 'Invalid Porta ID'}
        except:
            raise
            return {'message': 'Something went wrong'}, 500


    @jwt_required
    def post(self):
        data = porta_post_parser.parse_args()
        porta = DioPorta(porta_destino_id=data['porta_destino_id'], dio_id=data['dio_id'], 
                            numero_porta=data['numero_porta'], estado_link_id=data['estado_link_id'],
                            fibra_cabo_id=data['fibra_cabo_id'], fibra_numero=data['fibra_numero'], 
                            switch_porta=data['switch_porta'], observacao=data['observacao'], 
                            porta_bypass_id=data['porta_bypass_id'])
        try:
            porta.save()
            return {
                'message': 'Porta {} was created'.format(porta.id),
                }
        except IntegrityError as e:
            return {'message': '{}'.format(e.orig)}, 500
        except:
            raise
            return {'message': 'Something went wrong'}, 500
    
    @jwt_required
    def patch(self):
        data = porta_update_parser.parse_args()
        try:
            porta = DioPorta.query.filter_by(id=data['id']).first() 
            if porta:
                if data['porta_destino_id'] != porta.porta_destino_id:
                    porta2 = DioPorta.query.filter_by(id=data['porta_destino_id'])
                    porta2.porta_destino_id = porta.id
                    porta2.save()
                if data['porta_bypass_id'] != porta.porta_bypass_id:
                    porta2 = DioPorta.query.filter_by(id=data['porta_bypass_id'])
                    porta2.porta_bypass_id = porta.id
                    porta2.save()
                porta.porta_destino_id = data['porta_destino_id']
                porta.estado_link_id = data['estado_link_id']
                porta.fibra_cabo_id = data['fibra_cabo_id']
                porta.fibra_numero = data['fibra_numero']
                porta.switch_porta = data['switch_porta']
                porta.observacao = data['observacao']
                porta.porta_bypass_id = data['porta_bypass_id']
                porta.numero_porta = data['numero_porta']
                porta.save()
                return {
                    'message': 'Porta {} was updated'.format(data['id']),
                }
            return {'message':'Invalid Porta ID'}
        except IntegrityError as e:
            return {'message': '{}'.format(e.orig)}
        except:
            return {'message': 'Something went wrong'}, 500