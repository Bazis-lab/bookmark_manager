import os
from flask import Flask
from .config import Config
from .models.db import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # создаем папку instance если ее нет
    os.makedirs(app.config["INSTANCE_DIR"], exist_ok=True)

    # подключаем базу
    db.init_app(app)

    # создаем таблицы
    with app.app_context():
        db.create_all()

    # маршруты
    from .routes.links import links_bp
    from .routes.categories import categories_bp
    from .routes.tags import tags_bp
    from .routes.export import export_bp

    app.register_blueprint(links_bp)
    app.register_blueprint(categories_bp)
    app.register_blueprint(tags_bp)
    app.register_blueprint(export_bp)
    return app