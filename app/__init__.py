from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_moment import Moment

from app.config import Config

from app.models.posts import Post
from app.models.usuarios import User
from app.models.roles import Role

from app.routes.index import bp_index
from app.routes.admin import bp_admin
from app.routes.user import bp_user
from app.routes.mod import bp_mod
from app.routes.post import bp_post

moment = Moment()


def create_app():
    app = Flask(__name__)
    Bootstrap(app)
    moment.init_app(app)
    app.config.from_object(Config)

    app.register_blueprint(bp_index)
    app.register_blueprint(bp_admin)
    app.register_blueprint(bp_user)
    app.register_blueprint(bp_mod)
    app.register_blueprint(bp_post)

    db = SQLAlchemy(app)
    migrate = Migrate(app, db)

    return app
