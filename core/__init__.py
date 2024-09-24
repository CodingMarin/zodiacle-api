from flask import Flask
from decouple import config
from flask_restx import Api
from flask_cors import CORS
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config.from_object(config("APP_SETTINGS"))

# Configuración de CORS
CORS(app, resources={r"/*": {"origins": "*"}})

# Configuración de JWT
jwt = JWTManager(app)

# Configuración de autorizaciones para Swagger
authorizations = {
    'Bearer Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': 'Token JWT de tipo Bearer (e.g., Bearer TOKEN_BEARER)'
    }
}

api = Api(
    app,
    version='1.0',
    title='Zodiacle API',
    description='La API para gestionar las funcionalidades de Zodiacle. Proporciona acceso a los recursos principales de Zodiacle.',
    terms_url='https://zodiacle.com/terminos',
    license='MIT',
    license_url='https://opensource.org/licenses/MIT',
    contact='Zodiacle support',
    contact_url='https://zodiacle.com/contacto',
    contact_email='soporte@zodiacle.com',
    doc='/',
    default='default',
    default_label='Default namespace',
    prefix='/api/v1',
    default_mediatype='application/json',
    catch_all_404s=True,
    serve_challenge_on_401=True,
    ordered=True,
    tags=['Zodiacle'],
    security=[{'Bearer Auth': []}],
    authorizations=authorizations
)

from core import routes
