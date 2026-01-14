import sys

from app import create_app

try:
    from app.models import db, Category, Tag, Link
except Exception:
    try:
        from app.models.db import db
        from app.models.category import Category
        from app.models.tag import Tag
        from app.models.link import Link
    except Exception as e:
        print("не получилось импортировать db/модели. проверь структуру app/models")
        print("ошибка:", e)
        sys.exit(1)


def reset_db(seed: bool) -> None:
    app = create_app()

    with app.app_context():
        db.drop_all()
        db.create_all()

        if seed:
            c1 = Category(name="Учёба")
            c2 = Category(name="Работа")
            c3 = Category(name="Развлечения")

            db.session.add_all([c1, c2, c3])
            db.session.flush()

            # в базе храним теги без символа '#'
            t_python = Tag(name="python")
            t_flask = Tag(name="flask")
            t_sql = Tag(name="sql")
            t_video = Tag(name="video")
            t_read = Tag(name="статья")

            db.session.add_all([t_python, t_flask, t_sql, t_video, t_read])
            db.session.flush()

            l1 = Link(
                url="https://docs.python.org/3/",
                title="Документация Python",
                description="официальная документация по python",
                category_id=c1.id,
            )
            l2 = Link(
                url="https://flask.palletsprojects.com/",
                title="Flask Документация",
                description="основные разделы по flask и примеры",
                category_id=c1.id,
            )
            l3 = Link(
                url="https://sqlite.org/index.html",
                title="SQLite",
                description="страница проекта sqlite и описание возможностей",
                category_id=c2.id,
            )
            l4 = Link(
                url="https://www.youtube.com/watch?v=rfscVS0vtbw",
                title="Python Для Начинающих (Видео)",
                description="длинное видео с базой по python",
                category_id=c3.id,
            )

            db.session.add_all([l1, l2, l3, l4])
            db.session.flush()

            try:
                l1.tags.extend([t_python, t_read])
                l2.tags.extend([t_python, t_flask, t_read])
                l3.tags.extend([t_sql, t_read])
                l4.tags.extend([t_python, t_video])
            except Exception as e:
                print("не получилось привязать теги к ссылкам (relationship tags).")
                print("ошибка:", e)
                print("база создана, но без связей link<->tag.")
                db.session.commit()
                return

            db.session.commit()


def main() -> None:
    if len(sys.argv) < 2:
        print("использование: python manage_db.py empty|seed")
        sys.exit(1)

    mode = sys.argv[1].strip().lower()
    if mode == "empty":
        reset_db(seed=False)
        print("готово: создана пустая база")
        return

    if mode == "seed":
        reset_db(seed=True)
        print("готово: создана база с примерами")
        return

    print("неизвестный режим:", mode)
    print("использование: python manage_db.py empty|seed")
    sys.exit(1)


if __name__ == "__main__":
    main()