from core import api
from datetime import timedelta
from flask import jsonify
from core.utils import get_horoscope_by_day, get_horoscope_by_week, get_horoscope_by_month
from flask_restx import Resource, reqparse
from flask_jwt_extended import jwt_required, create_access_token
from werkzeug.exceptions import BadRequest, NotFound
from datetime import datetime

horoscope_ns = api.namespace('horoscopes', description='Endpoints for retrieving horoscopes for zodiac signs')

auth_ns = api.namespace('auth', description='Authentication endpoints')

ZODIAC_SIGNS = {
    "Aries": 1,
    "Taurus": 2,
    "Gemini": 3,
    "Cancer": 4,
    "Leo": 5,
    "Virgo": 6,
    "Libra": 7,
    "Scorpio": 8,
    "Sagittarius": 9,
    "Capricorn": 10,
    "Aquarius": 11,
    "Pisces": 12
}

parser = reqparse.RequestParser()
parser.add_argument('sign', type=str, required=True, help='The zodiac sign for which the horoscope is requested')

parser_copy = parser.copy()
parser_copy.add_argument('day', type=str, required=True,
                         help='Date for the horoscope. Accepted values: format (yyyy-mm-dd), today, tomorrow, yesterday')

@auth_ns.route('/login')
class LoginAPI(Resource):
    '''Authenticate user and provide a JWT token'''
    @auth_ns.doc(
        description='Authenticate a user and generate a JWT token.',
        responses={
            200: 'Success. Returns the JWT token.',
            401: 'Unauthorized. Invalid credentials.'
        }
    )
    def post(self):
        expires = timedelta(days=365 * 10)
        access_token = create_access_token(identity='user_id', expires_delta=expires)
        return jsonify(access_token=access_token)

@auth_ns.route('/protected')
class ProtectedResourceAPI(Resource):
    @auth_ns.doc(
        description='Access protected data. Requires JWT authentication.',
        responses={
            200: 'Success. Returns the protected data.',
            401: 'Unauthorized. Invalid or missing JWT token.'
        }
    )
    @jwt_required()
    def get(self):
        return jsonify(message="This is a protected endpoint.")

@horoscope_ns.route('/daily')
class DailyHoroscopeAPI(Resource):
    @horoscope_ns.doc(
        description='Retrieve the daily horoscope for a specific zodiac sign.',
        params={
            'sign': 'The zodiac sign for which the daily horoscope is requested.',
            'day': 'The date for the horoscope. Accepted formats are: YYYY-MM-DD, today, tomorrow, or yesterday.'
        }
    )
    @jwt_required()
    def get(self):
        args = parser_copy.parse_args()
        day = args.get('day')
        zodiac_sign = args.get('sign')
        try:
            zodiac_num = ZODIAC_SIGNS[zodiac_sign.capitalize()]
            if "-" in day:
                datetime.strptime(day, '%Y-%m-%d')  # Validate date format
            horoscope_data = get_horoscope_by_day(zodiac_num, day)
            return jsonify(success=True, data=horoscope_data, status=200)
        except KeyError:
            raise NotFound('The specified zodiac sign does not exist')
        except AttributeError:
            raise BadRequest('An error occurred. Please check the URL and parameters.')
        except ValueError:
            raise BadRequest('Invalid date format. Please use YYYY-MM-DD')

@horoscope_ns.route('/weekly')
class WeeklyHoroscopeAPI(Resource):
    @horoscope_ns.doc(
        description='Retrieve the weekly horoscope for a specific zodiac sign.',
        params={
            'sign': 'The zodiac sign for which the weekly horoscope is requested.'
        }
    )
    @jwt_required()
    def get(self):
        args = parser.parse_args()
        zodiac_sign = args.get('sign')
        try:
            zodiac_num = ZODIAC_SIGNS[zodiac_sign.capitalize()]
            horoscope_data = get_horoscope_by_week(zodiac_num)
            return jsonify(success=True, data=horoscope_data, status=200)
        except KeyError:
            raise NotFound('The specified zodiac sign does not exist')
        except AttributeError:
            raise BadRequest('An error occurred. Please check the URL and parameters.')

@horoscope_ns.route('/monthly')
class MonthlyHoroscopeAPI(Resource):
    @horoscope_ns.doc(
        description='Retrieve the monthly horoscope for a specific zodiac sign.',
        params={
            'sign': 'The zodiac sign for which the monthly horoscope is requested.'
        }
    )
    @jwt_required()
    def get(self):
        """Get the monthly horoscope for the specified zodiac sign"""
        args = parser.parse_args()
        zodiac_sign = args.get('sign')
        try:
            zodiac_num = ZODIAC_SIGNS[zodiac_sign.capitalize()]
            horoscope_data = get_horoscope_by_month(zodiac_num)
            return jsonify(success=True, data=horoscope_data, status=200)
        except KeyError:
            raise NotFound('The specified zodiac sign does not exist')
        except AttributeError:
            raise BadRequest('An error occurred. Please check the URL and parameters.')
