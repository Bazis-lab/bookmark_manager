import csv
import io
import json
from ..models.link import Link

# сервис для экспорта данных
class ExportService:
    @staticmethod
    def export_json() -> str:
        # json со ссылками, категорией и тегами
        links = Link.query.order_by(Link.created_at.desc()).all()
        data = []
        for l in links:
            data.append({
                "id": l.id,
                "url": l.url,
                "title": l.title,
                "description": l.description,
                "created_at": l.created_at.isoformat(),
                "category": {"id": l.category.id, "name": l.category.name},
                "tags": [{"id": t.id, "name": t.name} for t in l.tags],
            })
        return json.dumps(data, ensure_ascii=False, indent=2)

    @staticmethod
    def export_csv() -> str:
        # csv, теги кладем одной строкой через пробел
        links = Link.query.order_by(Link.created_at.desc()).all()
        output = io.StringIO()
        writer = csv.writer(output)

        writer.writerow(["id", "url", "title", "description", "created_at", "category", "tags"])

        for l in links:
            tags_str = " ".join([f"#{t.name}" for t in l.tags])
            writer.writerow([
                l.id,
                l.url,
                l.title,
                l.description or "",
                l.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                l.category.name,
                tags_str,
            ])

        return output.getvalue()