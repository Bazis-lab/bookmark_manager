from flask import Blueprint, Response
from ..services.export_service import ExportService

export_bp = Blueprint("export", __name__, url_prefix="/export")

@export_bp.route("/json")
def export_json():
    # отдаем json как файл
    data = ExportService.export_json()
    return Response(
        data,
        mimetype="application/json; charset=utf-8",
        headers={"Content-Disposition": "attachment; filename=bookmarks.json"},
    )

@export_bp.route("/csv")
def export_csv():
    # отдаем csv как файл
    data = ExportService.export_csv()
    return Response(
        data,
        mimetype="text/csv; charset=utf-8",
        headers={"Content-Disposition": "attachment; filename=bookmarks.csv"},
    )