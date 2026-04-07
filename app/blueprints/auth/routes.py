"""Blueprint de autenticación: registro, login, logout, perfil."""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.models import db, User
from .forms import RegisterForm, LoginForm, EditProfileForm, ChangePasswordForm

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/registro", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
            full_name=form.full_name.data,
            username=form.username.data,
            email=form.email.data.lower(),
            phone_whatsapp=form.phone_whatsapp.data or None,
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("¡Cuenta creada exitosamente! Ya puedes iniciar sesión.", "success")
        return redirect(url_for("auth.login"))
    return render_template("auth/register.html", form=form, title="Registro")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user and user.check_password(form.password.data) and user.is_active:
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            flash(f"¡Bienvenido, {user.full_name}!", "success")
            return redirect(next_page or url_for("main.index"))
        flash("Correo o contraseña incorrectos.", "danger")
    return render_template("auth/login.html", form=form, title="Iniciar sesión")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Sesión cerrada.", "info")
    return redirect(url_for("main.index"))


@auth_bp.route("/perfil")
@login_required
def profile():
    pets_reported = current_user.reported_pets.filter_by(is_active=True).all()
    return render_template("auth/profile.html", title="Mi perfil", pets=pets_reported)


@auth_bp.route("/perfil/editar", methods=["GET", "POST"])
@login_required
def edit_profile():
    form = EditProfileForm(obj=current_user)
    if form.validate_on_submit():
        current_user.full_name = form.full_name.data
        current_user.phone_whatsapp = form.phone_whatsapp.data or None
        current_user.bio = form.bio.data or None
        db.session.commit()
        flash("Perfil actualizado.", "success")
        return redirect(url_for("auth.profile"))
    return render_template("auth/edit_profile.html", form=form, title="Editar perfil")


@auth_bp.route("/perfil/contrasena", methods=["GET", "POST"])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if not current_user.check_password(form.current.data):
            flash("La contraseña actual es incorrecta.", "danger")
        else:
            current_user.set_password(form.new_pass.data)
            db.session.commit()
            flash("Contraseña actualizada correctamente.", "success")
            return redirect(url_for("auth.profile"))
    return render_template("auth/change_password.html", form=form, title="Cambiar contraseña")
