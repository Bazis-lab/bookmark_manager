from ..models.db import db
from ..models.link import Link
from .tag_service import TagService

# операции со ссылками
class LinkService:
    @staticmethod
    def _validate_url(url: str) -> bool:
        # простая проверка url
        return url.startswith("http://") or url.startswith("https://")

    @staticmethod
    def create_link(url: str, title: str, description: str, category_id: int, raw_tags: str) -> Link:
        if not LinkService._validate_url(url):
            raise ValueError("Некорректный URL")

        link = Link(
            url=url.strip(),
            title=title.strip(),
            description=(description.strip() if description else None),
            category_id=category_id,
        )

        tag_names = TagService.parse_tags(raw_tags)
        link.tags = TagService.get_or_create_tags(tag_names)

        db.session.add(link)
        db.session.commit()
        return link

    @staticmethod
    def update_link(link: Link, url: str, title: str, description: str, category_id: int, raw_tags: str) -> Link:
        if not LinkService._validate_url(url):
            raise ValueError("Некорректный URL")

        link.url = url.strip()
        link.title = title.strip()
        link.description = (description.strip() if description else None)
        link.category_id = category_id

        tag_names = TagService.parse_tags(raw_tags)
        link.tags = TagService.get_or_create_tags(tag_names)

        db.session.commit()
        return link

    @staticmethod
    def delete_link(link: Link) -> None:
        db.session.delete(link)
        db.session.commit()