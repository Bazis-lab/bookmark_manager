from ..models.db import db
from ..models.category import Category
from ..models.link import Link
from ..models.tag import Tag

# сервис для заполнения базы демонстрационными данными
class SeedService:
    @staticmethod
    def seed():
        # если данные уже есть, повторно не заполняем
        if Category.query.first():
            return False

        # категории
        study = Category(name="обучение")
        work = Category(name="работа")
        fun = Category(name="разное")

        db.session.add_all([study, work, fun])
        db.session.flush()

        # теги
        t_python = Tag(name="python")
        t_flask = Tag(name="flask")
        t_article = Tag(name="статья")
        t_video = Tag(name="видео")

        db.session.add_all([t_python, t_flask, t_article, t_video])
        db.session.flush()

        # ссылки
        l1 = Link(
            url="https://docs.python.org/3/",
            title="официальная документация python",
            description="документация по языку python",
            category_id=study.id,
            tags=[t_python, t_article],
        )

        l2 = Link(
            url="https://flask.palletsprojects.com/",
            title="flask documentation",
            description="официальная документация flask",
            category_id=study.id,
            tags=[t_python, t_flask],
        )

        l3 = Link(
            url="https://www.youtube.com/",
            title="youtube",
            description="видеохостинг",
            category_id=fun.id,
            tags=[t_video],
        )

        db.session.add_all([l1, l2, l3])
        db.session.commit()

        return True