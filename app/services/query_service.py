from sqlalchemy import or_
from ..models.link import Link
from ..models.tag import Tag

# фильтры для списка ссылок
class QueryService:
    @staticmethod
    def apply_filters(base_query, q: str | None, category_id: int | None, tag_names: list[str]):
        # поиск по названию и описанию
        if q:
            q = q.strip()
            if q:
                like = f"%{q}%"
                base_query = base_query.filter(or_(Link.title.ilike(like), Link.description.ilike(like)))

        # фильтр по категории
        if category_id:
            base_query = base_query.filter(Link.category_id == category_id)

        # фильтр по тегам 
        for name in tag_names:
            base_query = base_query.filter(Link.tags.any(Tag.name == name))

        return base_query