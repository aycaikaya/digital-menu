import os
class Config:
    SECRET_KEY = os.urandom(32)
    SECRET_KEY = SECRET_KEY

    SQLALCHEMY_DATABASE_URI = "sqlite:///site.db"

    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    MAIL_USERNAME = 'getdigitalmenu@gmail.com'
    MAIL_PASSWORD = 'mCi.250699'