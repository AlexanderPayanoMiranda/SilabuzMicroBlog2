import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = 'mysql://root:jV#%rh5ujnX3kSnBg#xYEP7L@localhost/blog'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
