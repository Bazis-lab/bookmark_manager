from .db import db

# промежуточная таблица для связи многие-ко-многим между ссылками и тегами
link_tags = db.Table(
    "link_tags",
    db.Column("link_id", db.Integer, db.ForeignKey("links.id"), primary_key=True),
    db.Column("tag_id", db.Integer, db.ForeignKey("tags.id"), primary_key=True),
)