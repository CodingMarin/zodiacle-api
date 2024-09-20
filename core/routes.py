from core import api
from datetime import timedelta
from flask import jsonify
from core.utils import get_horoscope_by_day, get_horoscope_by_week, get_horoscope_by_month, normalize_string
from flask_restx import Resource, reqparse
from flask_jwt_extended import jwt_required, create_access_token
from werkzeug.exceptions import BadRequest, NotFound

horoscope_ns = api.namespace('horoscopos', description='Puntos finales para obtener horóscopos para signos zodiacales')

auth_ns = api.namespace('auth', description='Puntos finales de autenticación')

parser = reqparse.RequestParser()
parser.add_argument('sign', type=str, required=True, help='El signo zodiacal para el cual se solicita el horóscopo')

parser_copy = parser.copy()
parser_copy.add_argument('day', type=str, required=True,
                         help='Fecha para el horóscopo. Valores aceptados: Hoy, Mañana, Semanal')

@auth_ns.route('/login')
class LoginAPI(Resource):
    '''Autentica al usuario y proporciona un token JWT'''
    @auth_ns.doc(
        description='Autentica a un usuario y genera un token JWT.',
        responses={
            200: 'Éxito. Devuelve el token JWT.',
            401: 'No autorizado. Credenciales inválidas.'
        }
    )
    def post(self):
        expires = timedelta(days=365 * 10)
        access_token = create_access_token(identity='user_id', expires_delta=expires)
        return jsonify(access_token=access_token)

@auth_ns.route('/protected')
class ProtectedResourceAPI(Resource):
    @auth_ns.doc(
        description='Accede a datos protegidos. Requiere autenticación JWT.',
        responses={
            200: 'Éxito. Devuelve los datos protegidos.',
            401: 'No autorizado. Token JWT inválido o faltante.'
        }
    )
    @jwt_required()
    def get(self):
        return jsonify(message="Este es un punto final protegido.")

@horoscope_ns.route('/daily')
class DailyHoroscopeAPI(Resource):
    @horoscope_ns.doc(
        description='Obtén el horóscopo diario para un signo zodiacal específico.',
        params={
            'sign': 'El signo zodiacal para el cual se solicita el horóscopo diario.',
            'day': 'La fecha para el horóscopo. Los valores aceptados son: hoy, mañana, semanal'
        }
    )
    @jwt_required()
    def get(self):
        """Obtén el horóscopo del dia actual, de mañana y semanal para el signo zodiacal especificado"""
        args = parser_copy.parse_args()
        day = args.get('day')
        day_formated = normalize_string(day)
        zodiac_sign = args.get('sign')
        zodiac_sign_formated = normalize_string(zodiac_sign)
        try:
            horoscope_data = get_horoscope_by_day(zodiac_sign_formated, day_formated)
            return jsonify(success=True, data=horoscope_data, status=200)

        except KeyError:
            raise NotFound('El signo zodiacal especificado no existe.')
        except Exception as e:
            raise BadRequest(f'Ocurrió un error: {str(e)}')

@horoscope_ns.route('/weekly')
class WeeklyHoroscopeAPI(Resource):
    @horoscope_ns.doc(
        description='Obtén el horóscopo semanal para un signo zodiacal específico.',
        params={
            'sign': 'El signo zodiacal para el cual se solicita el horóscopo semanal.'
        }
    )
    @jwt_required()
    def get(self):
        """Obtén el horóscopo semanal para el signo zodiacal especificado"""
        args = parser.parse_args()
        zodiac_sign = args.get('sign')
        zodiac_sign_formated = normalize_string(zodiac_sign)
        try:
            horoscope_data = get_horoscope_by_week(zodiac_sign_formated)
            return jsonify(success=True, data=horoscope_data, status=200)
        except KeyError:
            raise NotFound('El signo zodiacal especificado no existe')
        except AttributeError:
            raise BadRequest('Ocurrió un error. Por favor, verifica la URL y los parámetros.')

@horoscope_ns.route('/monthly')
class MonthlyHoroscopeAPI(Resource):
    @horoscope_ns.doc(
        description='Obtén el horóscopo mensual para un signo zodiacal específico.',
        params={
            'sign': 'El signo zodiacal para el cual se solicita el horóscopo mensual.'
        }
    )
    @jwt_required()
    def get(self):
        """Obtén el horóscopo mensual para el signo zodiacal especificado"""
        args = parser.parse_args()
        zodiac_sign = args.get('sign')
        zodiac_sign_formated = normalize_string(zodiac_sign)
        try:
            horoscope_data = get_horoscope_by_month(zodiac_sign_formated)
            return jsonify(success=True, data=horoscope_data, status=200)
        except KeyError:
            raise NotFound('El signo zodiacal especificado no existe')
        except AttributeError:
            raise BadRequest('Ocurrió un error. Por favor, verifica la URL y los parámetros.')
