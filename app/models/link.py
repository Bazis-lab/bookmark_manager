from datetime import datetime
from .db import db
from .link_tag import link_tags

# модель ссылки (закладки)
class Link(db.Model):
    __tablename__ = "links"

    id = db.Column(db.Integer, primary_key=True)

    # url обязательный
    url = db.Column(db.String(2048), nullable=False)

    # название обязательное
    title = db.Column(db.String(255), nullable=False)

    # описание необязательное
    description = db.Column(db.Text, nullable=True)

    # дата добавления ставится автоматически
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # у ссылки должна быть ровно одна категория по заданию
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)

    # связь с категорией
    category = db.relationship("Category", back_populates="links")

    # связь с тегами (много тегов у одной ссылки)
    tags = db.relationship("Tag", secondary=link_tags, backref=db.backref("links", lazy="dynamic"))

    def __repr__(self):
        return f"<Link id={self.id} title={self.title}>"