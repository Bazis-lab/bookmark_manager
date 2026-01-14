import os

# базовая конфигурация приложения
class Config:
    # секретный ключ нужен для форм
    SECRET_KEY = "dev-secret-key"

    # корень проекта (на уровень выше папки app)
    ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    # папка instance для базы sqlite
    INSTANCE_DIR = os.path.join(ROOT_DIR, "instance")
    DB_PATH = os.path.join(INSTANCE_DIR, "app.db")

    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DB_PATH}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False