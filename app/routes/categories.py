from flask import Blueprint, redirect, render_template, request, url_for, flash
from ..models.db import db
from ..models.category import Category

categories_bp = Blueprint("categories", __name__, url_prefix="/categories")

@categories_bp.route("/", methods=["GET", "POST"])
def list_create():
    # список категорий + создание новой
    if request.method == "POST":
        name = (request.form.get("name") or "").strip()
        if not name:
            flash("введи название категории")
            return redirect(url_for("categories.list_create"))

        exists = Category.query.filter_by(name=name).first()
        if exists:
            flash("такая категория уже есть")
            return redirect(url_for("categories.list_create"))

        c = Category(name=name)
        db.session.add(c)
        db.session.commit()
        flash("категория создана")
        return redirect(url_for("categories.list_create"))

    categories = Category.query.order_by(Category.name.asc()).all()
    return render_template("categories/list.html", categories=categories)

@categories_bp.route("/<int:category_id>/rename", methods=["POST"])
def rename(category_id: int):
    # переименование категории
    c = Category.query.get_or_404(category_id)
    new_name = (request.form.get("name") or "").strip()
    if not new_name:
        flash("новое имя пустое")
        return redirect(url_for("categories.list_create"))

    exists = Category.query.filter(Category.name == new_name, Category.id != c.id).first()
    if exists:
        flash("категория с таким именем уже есть")
        return redirect(url_for("categories.list_create"))

    c.name = new_name
    db.session.commit()
    flash("категория переименована")
    return redirect(url_for("categories.list_create"))

@categories_bp.route("/<int:category_id>/delete", methods=["POST"])
def delete(category_id: int):
    # удаление категории 
    c = Category.query.get_or_404(category_id)
    db.session.delete(c)
    db.session.commit()
    flash("категория удалена")
    return redirect(url_for("categories.list_create"))