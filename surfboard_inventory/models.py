from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate
import uuid 
from datetime import datetime

# adding flask security for passwords
from werkzeug.security import generate_password_hash, check_password_hash

# import for secrets module (given by python)
import secrets 
# Imports for Flask_Login
from flask_login import UserMixin, LoginManager

# Import for Flask-Marshmallow
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model):
    id = db.Column(db.String, primary_key = True)
    first_name = db.Column(db.String(150), nullable = True, default = '')
    last_name = db.Column(db.String(150), nullable = True, default = '')
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String, nullable = True, default = '')
    g_auth_verify = db.Column(db.Boolean,default = False) 
    token = db.Column(db.String, default = '', unique = True)
    date_create = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    surfboard = db.relationship('Surfboard', backref = 'owner', lazy = True)
    

    def __init__(self, email, first_name = '', last_name = '', id = '', password = '', token = '',   g_auth_verify = False):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token(24)
        self.g_auth_verify = g_auth_verify
    def set_token(self, length):
        return secrets.token_hex(length)
    
    def set_id(self):
        return str(uuid.uuid4()) # the number 4 reps a different version. 1,3,4,5 do different things
    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash
    
    def __repr__(self):
        return f"User {self.email} has been added to the database"
    

class Surfboard(db.Model, UserMixin):
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(150))
    description = db.Column(db.String(200))
    price = db.Column(db.Numeric(precision=10, scale=2))
    included_accessories = db.Column(db.String(150), nullable = True)
    base_color = db.Column(db.String(100), nullable = True)
    material = db.Column(db.String(100))
    dimensions = db.Column(db.String(100))
    weight = db.Column(db.String(100))
    cost_of_production = db.Column(db.Numeric(precision=10, scale=2))
    series = db.Column(db.String(150))
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)

    def __init__(self, name, description, price, included_accessories, base_color, material, dimensions, weight, cost_of_production, series, user_token, id = ''):
            self.id = self.set_id()
            self.name = name
            self.description = description 
            self.price = price
            self.included_accessories = included_accessories
            self.base_color = base_color
            self.material = material 
            self.dimensions = dimensions
            self.weight = weight
            self.cost_of_production = cost_of_production
            self.series = series
            self.user_token = user_token

    def __repr__(self):
            return f"The following Surfboard has been added: {self.name}"
    
    def set_id(self):
        return secrets.token_urlsafe()

class SurfboardSchema(ma.Schema):
    class Meta: 
        fields = ['id', 'name', 'description', 'price', 'included_accessories', 'base_color', 'material', 'dimensions', 'weight', 'cost_of_production', 'series']

surfboard_schema = SurfboardSchema()
surfboards_schema= SurfboardSchema(many = True)