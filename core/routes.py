from core import api
from datetime import timedelta
from flask import jsonify
from core.utils import get_horoscope_by_day, get_horoscope_by_week, get_horoscope_by_month, normalize_string, get_compatibility_sign
from flask_restx import Resource, reqparse
from flask_jwt_extended import jwt_required, create_access_token
from werkzeug.exceptions import BadRequest, NotFound

horoscope_ns = api.namespace('horoscopos', description='Puntos finales para obtener horóscopos para signos zodiacales')
auth_ns = api.namespace('auth', description='Puntos finales de autenticación')
compatibility_ns = api.namespace('compatibilidad', description='Puntos finales para obtener la compatibilidad entre signos zodiacales')

parser = reqparse.RequestParser()
parser.add_argument('sign', type=str, required=True, help='El signo zodiacal para el cual se solicita el horóscopo')

parser_copy = parser.copy()
parser_copy.add_argument('day', type=str, required=True, help='Fecha para el horóscopo. Valores aceptados: Hoy, Manana, Semanal')

# Parser para compatibilidad de signos zodiacales
compatibility_parser = reqparse.RequestParser()
compatibility_parser.add_argument('sign_a', type=str, required=True, help='Primer signo zodiacal')
compatibility_parser.add_argument('sign_b', type=str, required=True, help='Segundo signo zodiacal')

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
            'day': 'La fecha para el horóscopo. Los valores aceptados son: hoy, manana, semanal'
        }
    )
    @jwt_required()
    def get(self):
        """Obtén el horóscopo del dia actual, de manana y semanal para el signo zodiacal especificado"""
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

@compatibility_ns.route('/signs')
class CompatibilitySignsAPI(Resource):
    @compatibility_ns.doc(
        description='Obtén la compatibilidad entre dos signos zodiacales.',
        params={
            'sign_a': 'El primer signo zodiacal para verificar compatibilidad.',
            'sign_b': 'El segundo signo zodiacal para verificar compatibilidad.'
        }
    )
    @jwt_required()
    def get(self):
        """Obtén la compatibilidad entre dos signos zodiacales especificados"""
        args = compatibility_parser.parse_args()
        sign_a = args.get('sign_a')
        sign_b = args.get('sign_b')

        sign_a_formatted = normalize_string(sign_a)
        sign_b_formatted = normalize_string(sign_b)

        try:
            compatibility_data = get_compatibility_sign(sign_a_formatted, sign_b_formatted)
            return jsonify(success=True, compatibility=compatibility_data, status=200)
        except Exception as e:
            raise BadRequest(f'Ocurrió un error: {str(e)}')