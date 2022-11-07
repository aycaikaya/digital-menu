from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from dmenu import db,login_manager
from flask_login import UserMixin
from flask import current_app

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    rest_name=db.Column(db.String(50),unique=True,nullable=False)
    rest_address=db.Column(db.String(60))
    table_count=db.Column(db.Integer,nullable=False)
    email=db.Column(db.String(120),unique=True,nullable=False)
    password=db.Column(db.String(60),nullable=False)
    terms_cond=db.Column(db.Boolean, nullable=False)
    menus = db.relationship('Menu',backref='author',lazy=True)

    def get_reset_token(self,expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'],expires_sec)
        return s.dumps({'user_id':self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id=s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.rest_name}','{self.rest_address}','{self.email}')"

class Menu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.String(80), nullable=False, default="default.jpg")
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Menu('{self.title}','{self.date_posted}','{self.content}')"