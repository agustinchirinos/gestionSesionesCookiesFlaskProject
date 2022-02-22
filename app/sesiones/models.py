from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


# class User(UserMixin):
#     def __init__(self, id, username):
#         self.id = id
#         self.username = username
#
#
#     def __repr__(self):
#         return '<User {}>'.format(self.username)



from app import db


class Usuario(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), unique=True,nullable=False)
    password = db.Column(db.String())
    passwordcifrada = db.Column(db.LargeBinary)
    dni = db.Column(db.String(10),nullable=False,unique=True)
    nombre = db.Column(db.String(20),nullable=False)
    apellidos = db.Column(db.String(50),nullable=False)

    def __repr__(self):
        return f'<Usuario {self.apellidos}, {self.nombre}>'

    def __str__(self):
        return f"{self.apellidos}, {self.nombre}"

    def create(self):
        try:
            db.session.add(self)
            db.session.commit()
        except:
            raise

    def update(self):
        try:
            db.session.commit()
        except:
            raise

    @staticmethod
    def get_by_id(id):
        return Usuario.query.get(id)

    @staticmethod
    def get_by_username(username):
        return Usuario.query.filter_by(username=username).first()

    def set_password(self, password):
        # self.password = generate_password_hash(password, method='pbkdf2:sha512')
        method = "pbkdf2:sha256:260000"
        # method = "plain"
        # method = "pbkdf2:sha512:1000000"
        self.password = generate_password_hash(password, method=method)  # Por defecto sha256
        # self.password = password.split("$", 1)[1]

    def check_password(self, password):
        # passHash = 'pbkdf2:sha256:260000$' + self.password
        return check_password_hash(self.password, password)