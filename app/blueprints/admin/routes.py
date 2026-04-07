"""admin/routes.py — Panel de administración completo."""
from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from sqlalchemy import func
from app.models import (db, User, Pet, Comment, AdoptionRequest, Donation,
                        UserRole, PetStatus, AdoptionStatus)
from app.utils import admin_required

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/")
@login_required
@admin_required
def dashboard():
    stats = {
        "users":     User.query.count(),
        "pets":      Pet.query.filter_by(is_active=True).count(),
        "lost":      Pet.query.filter_by(status=PetStatus.LOST, is_active=True).count(),
        "urgent":    Pet.query.filter_by(status=PetStatus.URGENT, is_active=True).count(),
        "adoption":  Pet.query.filter_by(status=PetStatus.ADOPTION, is_active=True).count(),
        "adopted":   Pet.query.filter_by(status=PetStatus.ADOPTED, is_active=True).count(),
        "found":     Pet.query.filter_by(status=PetStatus.FOUND, is_active=True).count(),
        "requests":  AdoptionRequest.query.count(),
        "pending":   AdoptionRequest.query.filter_by(status=AdoptionStatus.PENDING).count(),
        "rescuers":  User.query.filter_by(role=UserRole.RESCUER).count(),
    }
    recent_pets  = Pet.query.order_by(Pet.created_at.desc()).limit(6).all()
    recent_users = User.query.order_by(User.created_at.desc()).limit(6).all()
    return render_template("admin/dashboard.html", stats=stats,
                           recent_pets=recent_pets, recent_users=recent_users,
                           title="Panel de administración")


# ── Usuarios ─────────────────────────────────────────────────────────────────

@admin_bp.route("/usuarios")
@login_required
@admin_required
def list_users():
    page     = request.args.get("page", 1, type=int)
    role_f   = request.args.get("role", "")
    search   = request.args.get("q", "")
    query    = User.query
    if role_f:
        query = query.filter_by(role=role_f)
    if search:
        query = query.filter(
            User.full_name.ilike(f"%{search}%") | User.email.ilike(f"%{search}%")
        )
    users = query.order_by(User.created_at.desc()).paginate(page=page, per_page=20)
    return render_template("admin/users.html", users=users, role_f=role_f,
                           search=search, all_roles=UserRole.ALL, title="Usuarios")


@admin_bp.route("/usuarios/<int:user_id>/rol", methods=["POST"])
@login_required
@admin_required
def change_role(user_id):
    user     = User.query.get_or_404(user_id)
    new_role = request.form.get("role", "")
    if new_role not in UserRole.ALL:
        flash("Rol inválido.", "danger")
    elif user.id == current_user.id:
        flash("No puedes cambiar tu propio rol.", "warning")
    else:
        user.role = new_role
        db.session.commit()
        flash(f"Rol de {user.username} → '{new_role}'.", "success")
    return redirect(url_for("admin.list_users"))


@admin_bp.route("/usuarios/<int:user_id>/verificar", methods=["POST"])
@login_required
@admin_required
def verify_user(user_id):
    user = User.query.get_or_404(user_id)
    user.is_verified = not user.is_verified
    db.session.commit()
    state = "verificado ✓" if user.is_verified else "no verificado"
    flash(f"{user.username} marcado como {state}.", "success")
    return redirect(url_for("admin.list_users"))


@admin_bp.route("/usuarios/<int:user_id>/activar", methods=["POST"])
@login_required
@admin_required
def toggle_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash("No puedes desactivar tu propia cuenta.", "warning")
    else:
        user.is_active = not user.is_active
        db.session.commit()
        flash(f"Usuario {user.username} {'activado' if user.is_active else 'desactivado'}.", "info")
    return redirect(url_for("admin.list_users"))


# ── Mascotas ─────────────────────────────────────────────────────────────────

@admin_bp.route("/mascotas")
@login_required
@admin_required
def list_pets():
    page      = request.args.get("page", 1, type=int)
    status_f  = request.args.get("status", "")
    active_f  = request.args.get("active", "1")   # "1"=activas, "0"=eliminadas, ""=todas
    query     = Pet.query
    if status_f:
        query = query.filter_by(status=status_f)
    if active_f == "1":
        query = query.filter_by(is_active=True)
    elif active_f == "0":
        query = query.filter_by(is_active=False)
    pets = query.order_by(Pet.created_at.desc()).paginate(page=page, per_page=20)
    return render_template("admin/pets.html", pets=pets,
                           status_f=status_f, active_f=active_f,
                           statuses=PetStatus.ALL, title="Moderar mascotas")


@admin_bp.route("/mascotas/<int:pet_id>/restaurar", methods=["POST"])
@login_required
@admin_required
def restore_pet(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    pet.is_active = True
    db.session.commit()
    flash("Reporte restaurado.", "success")
    return redirect(url_for("admin.list_pets"))


@admin_bp.route("/mascotas/<int:pet_id>/eliminar-permanente", methods=["POST"])
@login_required
@admin_required
def hard_delete_pet(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    db.session.delete(pet)
    db.session.commit()
    flash("Mascota eliminada permanentemente.", "info")
    return redirect(url_for("admin.list_pets"))


# ── Solicitudes ──────────────────────────────────────────────────────────────

@admin_bp.route("/solicitudes")
@login_required
@admin_required
def list_requests():
    page     = request.args.get("page", 1, type=int)
    status_f = request.args.get("status", "")
    query    = AdoptionRequest.query
    if status_f:
        query = query.filter_by(status=status_f)
    reqs = query.order_by(AdoptionRequest.created_at.desc()).paginate(page=page, per_page=20)
    return render_template("admin/requests.html", requests=reqs,
                           status_f=status_f, statuses=AdoptionStatus.ALL,
                           title="Solicitudes de adopción")


# ── Donaciones ───────────────────────────────────────────────────────────────

@admin_bp.route("/donaciones")
@login_required
@admin_required
def list_donations():
    page = request.args.get("page", 1, type=int)
    donations = Donation.query.order_by(Donation.created_at.desc()).paginate(page=page, per_page=20)
    total_sum = db.session.query(func.sum(Donation.amount)).scalar() or 0
    return render_template("admin/donations.html", donations=donations,
                           total_sum=total_sum, title="Donaciones")
