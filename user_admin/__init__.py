from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_jwt_extended import JWTManager
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)

db_username = 'root'
db_password = 'root'
db_host= 'localhost'
db_port='3306'
db_name='pythonadvance'
mysql_uri = f'mysql+mysqlconnector://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}'
app.config['SQLALCHEMY_DATABASE_URI'] = mysql_uri
app.config['SECRET_KEY'] = 'e40ad44dd967df3ab659133e'
app.config['JWT_SECRET_KEY'] = '4d03d355e1864a7ead290a4d02af180e'
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_COOKIE_CSRF_PROTECT'] = True  

csrf = CSRFProtect(app)
jwt = JWTManager(app)
db = SQLAlchemy(app)
hashing = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "employee_login"
login_manager.login_message_category = 'info'


    

from user_admin import routes
from user_admin.employee_search import employee_search_bp

app.register_blueprint(employee_search_bp,url_prefix = "/admin/employee/search")