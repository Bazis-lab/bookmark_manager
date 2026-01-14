from .db import db

# модель категории
class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)

    # имя категории уникальное, чтобы не было дублей
    name = db.Column(db.String(120), nullable=False, unique=True)

    # одна категория -> много ссылок
    links = db.relationship("Link", back_populates="category", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Category id={self.id} name={self.name}>"