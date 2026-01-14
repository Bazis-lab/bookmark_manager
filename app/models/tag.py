from .db import db

# модель тега
class Tag(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)

    # имя тега уникальное
    name = db.Column(db.String(80), nullable=False, unique=True)

    def __repr__(self):
        return f"<Tag id={self.id} name={self.name}>"