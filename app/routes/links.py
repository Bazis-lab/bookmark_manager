from flask import Blueprint, redirect, render_template, request, url_for, flash
from ..models.link import Link
from ..models.category import Category
from ..models.tag import Tag
from ..services.link_service import LinkService
from ..services.tag_service import TagService
from ..services.query_service import QueryService

# для страниц со ссылками
links_bp = Blueprint("links", __name__)

@links_bp.route("/", methods=["GET"])
def index():
    # главная страница список ссылок + поиск + фильтры
    q = request.args.get("q", "")
    category_id_raw = request.args.get("category_id", "")
    raw_tags = request.args.get("tags", "")

    category_id = int(category_id_raw) if category_id_raw.isdigit() else None
    tag_names = TagService.parse_tags(raw_tags)

    query = Link.query.order_by(Link.created_at.desc())
    query = QueryService.apply_filters(query, q=q, category_id=category_id, tag_names=tag_names)

    links = query.all()

    # данные для интерфейса
    categories = Category.query.order_by(Category.name.asc()).all()
    tags = Tag.query.order_by(Tag.name.asc()).all()

    filters = {
        "q": q,
        "category_id": category_id_raw,
        "tags": raw_tags,
    }

    return render_template(
        "links/list.html",
        links=links,
        categories=categories,
        tags=tags,
        filters=filters,
    )

@links_bp.route("/links/new", methods=["GET", "POST"])
def create():
    # добавление новой ссылки
    categories = Category.query.order_by(Category.name.asc()).all()

    if request.method == "POST":
        url = request.form.get("url") or ""
        title = request.form.get("title") or ""
        description = request.form.get("description") or ""
        raw_tags = request.form.get("tags") or ""
        category_id = request.form.get("category_id") or ""

        # простая валидация
        if not url.strip():
            flash("url обязателен")
            return render_template("links/form.html", categories=categories, mode="create", form=request.form)
        if not title.strip():
            flash("название обязательно")
            return render_template("links/form.html", categories=categories, mode="create", form=request.form)
        if not category_id:
            flash("нужно выбрать категорию")
            return render_template("links/form.html", categories=categories, mode="create", form=request.form)

        LinkService.create_link(
            url=url,
            title=title,
            description=description,
            category_id=int(category_id),
            raw_tags=raw_tags,
        )
        flash("ссылка добавлена")
        return redirect(url_for("links.index"))

    return render_template("links/form.html", categories=categories, mode="create", form={})

@links_bp.route("/links/<int:link_id>/edit", methods=["GET", "POST"])
def edit(link_id: int):
    # редактирование ссылки
    link = Link.query.get_or_404(link_id)
    categories = Category.query.order_by(Category.name.asc()).all()

    if request.method == "POST":
        url = request.form.get("url") or ""
        title = request.form.get("title") or ""
        description = request.form.get("description") or ""
        raw_tags = request.form.get("tags") or ""
        category_id = request.form.get("category_id") or ""

        if not url.strip():
            flash("url обязателен")
            return render_template("links/form.html", categories=categories, mode="edit", link=link, form=request.form)
        if not title.strip():
            flash("название обязательно")
            return render_template("links/form.html", categories=categories, mode="edit", link=link, form=request.form)
        if not category_id:
            flash("нужно выбрать категорию")
            return render_template("links/form.html", categories=categories, mode="edit", link=link, form=request.form)

        LinkService.update_link(
            link=link,
            url=url,
            title=title,
            description=description,
            category_id=int(category_id),
            raw_tags=raw_tags,
        )
        flash("ссылка обновлена")
        return redirect(url_for("links.index"))

    # теги в строку для формы
    tags_str = " ".join([f"#{t.name}" for t in link.tags])
    form = {
        "url": link.url,
        "title": link.title,
        "description": link.description or "",
        "category_id": str(link.category_id),
        "tags": tags_str,
    }
    return render_template("links/form.html", categories=categories, mode="edit", link=link, form=form)

@links_bp.route("/links/<int:link_id>/delete", methods=["POST"])
def delete(link_id: int):
    # удаление ссылки
    link = Link.query.get_or_404(link_id)
    LinkService.delete_link(link)
    flash("ссылка удалена")
    return redirect(url_for("links.index"))