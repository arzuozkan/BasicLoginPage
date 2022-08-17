from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
# python -c 'import secrets; print(secrets.token_hex())'
app.secret_key = '83059b825f5265d8f289ad09c3c5d8155eb6b6f60f0b5dcf762ae8982fce4bf4'
app.session_cookie_name="mycookie"
#app.secret_key = 'easy'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user_db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)
