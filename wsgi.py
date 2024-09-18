import sys
import os

path = '/home/Zodiacle/mysite'
if path not in sys.path:
    sys.path.append(path)

os.environ['FLASK_APP'] = 'app.py'
os.environ['FLASK_ENV'] = 'production'

from app import app as application

if __name__ == "__main__":
    application.run()
