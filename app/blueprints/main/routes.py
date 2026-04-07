"""main/routes.py — Landing, búsqueda, error handlers."""
from flask import Blueprint, render_template, request
from app.models import Pet, PetStatus, User, AdoptionRequest

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    urgent   = Pet.query.filter_by(status=PetStatus.URGENT,   is_active=True).order_by(Pet.created_at.desc()).limit(4).all()
    lost     = Pet.query.filter_by(status=PetStatus.LOST,     is_active=True).order_by(Pet.created_at.desc()).limit(4).all()
    adoption = Pet.query.filter_by(status=PetStatus.ADOPTION, is_active=True).order_by(Pet.created_at.desc()).limit(4).all()
    stats = {
        "total":    Pet.query.filter_by(is_active=True).count(),
        "lost":     Pet.query.filter_by(status=PetStatus.LOST,     is_active=True).count(),
        "adoption": Pet.query.filter_by(status=PetStatus.ADOPTION, is_active=True).count(),
        "urgent":   Pet.query.filter_by(status=PetStatus.URGENT,   is_active=True).count(),
        "adopted":  Pet.query.filter_by(status=PetStatus.ADOPTED,  is_active=True).count(),
    }
    return render_template("main/index.html",
                           urgent=urgent, lost=lost, adoption=adoption,
                           stats=stats, title="Inicio")


@main_bp.route("/buscar")
def search():
    q    = request.args.get("q", "").strip()
    page = request.args.get("page", 1, type=int)
    pets = None
    if q:
        pets = Pet.query.filter(
            Pet.is_active == True,
            (Pet.name.ilike(f"%{q}%") | Pet.description.ilike(f"%{q}%") |
             Pet.color.ilike(f"%{q}%") | Pet.location_zone.ilike(f"%{q}%"))
        ).order_by(Pet.created_at.desc()).paginate(page=page, per_page=12)
    return render_template("main/search.html", pets=pets, q=q, title=f"Búsqueda: {q}")


@main_bp.route("/acerca")
def about():
    stats = {
        "total":   Pet.query.filter_by(is_active=True).count(),
        "adopted": Pet.query.filter_by(status=PetStatus.ADOPTED, is_active=True).count(),
        "users":   User.query.filter_by(is_active=True).count(),
    }
    return render_template("main/about.html", stats=stats, title="Acerca del proyecto")


# ── Error handlers ────────────────────────────────────────────────────────────
def page_not_found(e):
    return render_template("errors/404.html", title="Página no encontrada"), 404

def server_error(e):
    return render_template("errors/500.html", title="Error del servidor"), 500

def forbidden(e):
    return render_template("errors/403.html", title="Acceso denegado"), 403
