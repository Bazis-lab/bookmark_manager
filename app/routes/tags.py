from flask import Blueprint, redirect, render_template, request, url_for, flash
from ..models.db import db
from ..models.tag import Tag

# для тегов
tags_bp = Blueprint("tags", __name__, url_prefix="/tags")

@tags_bp.route("/")
def list_tags():
    # список тегов
    tags = Tag.query.order_by(Tag.name.asc()).all()

    # делаем простую статистику сколько ссылок у тега
    items = []
    for t in tags:
        count_links = t.links.count()  
        items.append({"tag": t, "count": count_links})

    return render_template("tags/list.html", items=items)

@tags_bp.route("/<int:tag_id>/delete", methods=["POST"])
def delete(tag_id: int):
    # удаление тега
    t = Tag.query.get_or_404(tag_id)
    db.session.delete(t)
    db.session.commit()
    flash("тег удален")
    return redirect(url_for("tags.list_tags"))

@tags_bp.route("/merge", methods=["GET", "POST"])
def merge():
    # объединение тегов дебильное
    tags = Tag.query.order_by(Tag.name.asc()).all()

    if request.method == "POST":
        source_id = request.form.get("source_id") or ""
        target_id = request.form.get("target_id") or ""

        if not source_id or not target_id:
            flash("нужно выбрать оба тега")
            return redirect(url_for("tags.merge"))

        if source_id == target_id:
            flash("нельзя объединить тег сам в себя")
            return redirect(url_for("tags.merge"))

        source = Tag.query.get_or_404(int(source_id))
        target = Tag.query.get_or_404(int(target_id))

        # переносим связи
        for link in source.links.all():
            # если у ссылки нет target, добавляем
            if target not in link.tags:
                link.tags.append(target)
            # убираем source
            if source in link.tags:
                link.tags.remove(source)

        # удаляем source
        db.session.delete(source)
        db.session.commit()

        flash("теги объединены")
        return redirect(url_for("tags.list_tags"))

    return render_template("tags/merge.html", tags=tags)

# объединение хрень полная