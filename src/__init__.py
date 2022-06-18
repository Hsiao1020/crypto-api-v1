from flask import Flask, jsonify
import os
from src.constants.http_status_code import HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
from src.auth import auth
from src.btc import btc
from src.database import db, ma
from src.config.swagger import template, swagger_config
from flask_jwt_extended import JWTManager
from flasgger import Swagger, swag_from
from flask_migrate import Migrate


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.environ.get("SECRET_KEY"),
            SQLALCHEMY_DATABASE_URI=os.getenv(
                "CLEARDB_DATABASE_URL",
                default="mysql+pymysql://root:password@localhost:3306/crypto"  # For local development
            ),
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            JWT_SECRET_KEY=os.environ.get("JWT_SECRET_KEY"),

            SWAGGER={
                "title": "Crypto API",
                "universion": 3
            }
        )
    else:
        app.config.from_mapping(test_config)

    db.app = app
    db.init_app(app)
    ma.app = app
    ma.init_app(app)

    migrate = Migrate(compare_type=True)
    migrate.init_app(app, db)

    JWTManager(app)

    app.register_blueprint(auth)
    app.register_blueprint(btc)

    Swagger(app, config=swagger_config, template=template)

    @app.errorhandler(HTTP_404_NOT_FOUND)
    def handle_404(e):
        return jsonify({"error": "Not found"}), HTTP_404_NOT_FOUND

    @app.errorhandler(HTTP_500_INTERNAL_SERVER_ERROR)
    def handle_500(e):
        return jsonify({"error": "Something went wrong, we are working on it"}), HTTP_500_INTERNAL_SERVER_ERROR

    return app
