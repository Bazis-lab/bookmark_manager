import re
from ..models.db import db
from ..models.tag import Tag

# сервис для работы с тегами
class TagService:
    @staticmethod
    def parse_tags(raw: str) -> list[str]:
        if not raw:
            return []

        parts = re.split(r"[,\s]+", raw.strip())
        cleaned = []
        for p in parts:
            p = p.strip()
            if not p:
                continue
            if p.startswith("#"):
                p = p[1:]
            p = p.strip().lower()
            if p and p not in cleaned:
                cleaned.append(p)
        return cleaned

    @staticmethod
    def get_or_create_tags(tag_names: list[str]) -> list[Tag]:
        tags = []
        for name in tag_names:
            existing = Tag.query.filter_by(name=name).first()
            if existing:
                tags.append(existing)
            else:
                t = Tag(name=name)
                db.session.add(t)
                tags.append(t)
        return tags