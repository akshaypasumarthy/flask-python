from flask import session
from user_admin import db,LoginManager,login_manager
from user_admin import hashing
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    user = None
    role = session.get('role')  
    if role == 'employee':
        user = Employee.query.get(user_id)
    elif role == 'admin':
        user = Admin.query.get(user_id)
    return user

class Role(db.Model):
    __tablename__ = "role"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(length=20), nullable=False, unique=True)

class Employee(db.Model,UserMixin):
    __tablename__="employee"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(length=30), nullable=False)
    last_name = db.Column(db.String(length=30), nullable=False)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    address = db.Column(db.String(length=500), nullable=False)
    phone_number = db.Column(db.String(length=10), nullable=False, unique=True)
    DOB = db.Column(db.String(length=10), nullable=False)
    password_hash = db.Column(db.String(length=512), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    
    role = db.relationship('Role', backref=db.backref('employee', lazy=True))

    @property
    def password(self):
        return self.password
    
    @password.setter
    def password(self, plain_text_password):
        self.password_hash = hashing.generate_password_hash(plain_text_password).decode('utf-8')
        
    def check_password_correction(self,attempted_password):
        return hashing.check_password_hash(self.password_hash,attempted_password)
            

    def __repr__(self):
        return '<Employee %r>' % (self.first_name + self.last_name)

class Admin(db.Model,UserMixin):
    __tablename__ = "admin"
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(length=30), nullable=False)
    last_name = db.Column(db.String(length=30), nullable=False)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    address = db.Column(db.String(length=500), nullable=False)
    phone_number = db.Column(db.String(length=10), nullable=False, unique=True)
    DOB = db.Column(db.String(length=10), nullable=False)
    password_hash = db.Column(db.String(length=512), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)

    role = db.relationship('Role', backref=db.backref('admin', lazy=True))
    
    @property
    def password(self):
        return self.password
    
    @password.setter
    def password(self, plain_text_password):
        self.password_hash = hashing.generate_password_hash(plain_text_password).decode('utf-8')
        
    def check_password_correction(self,attempted_password):
        return hashing.check_password_hash(self.password_hash,attempted_password)

    def __repr__(self):
        return '<Admin %r>' % (self.first_name + self.last_name)
