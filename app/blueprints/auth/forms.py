"""Formularios de autenticación."""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Regexp, Optional
from app.models import User


class RegisterForm(FlaskForm):
    full_name  = StringField("Nombre completo", validators=[DataRequired(), Length(3, 150)])
    username   = StringField("Usuario", validators=[
        DataRequired(), Length(3, 80),
        Regexp(r'^[A-Za-z0-9_.]+$', message="Solo letras, números, puntos y guiones bajos.")
    ])
    email      = StringField("Correo electrónico", validators=[DataRequired(), Email()])
    phone_whatsapp = StringField("WhatsApp (opcional, con lada)", validators=[Optional(), Length(max=20)])
    password   = PasswordField("Contraseña", validators=[DataRequired(), Length(min=8)])
    confirm    = PasswordField("Confirmar contraseña", validators=[DataRequired(), EqualTo("password")])
    submit     = SubmitField("Crear cuenta")

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValueError("Este nombre de usuario ya está en uso.")

    def validate_email(self, field):
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValueError("Este correo ya está registrado.")


class LoginForm(FlaskForm):
    email    = StringField("Correo electrónico", validators=[DataRequired(), Email()])
    password = PasswordField("Contraseña", validators=[DataRequired()])
    remember = BooleanField("Recordarme")
    submit   = SubmitField("Iniciar sesión")


class EditProfileForm(FlaskForm):
    full_name      = StringField("Nombre completo", validators=[DataRequired(), Length(3, 150)])
    phone_whatsapp = StringField("WhatsApp", validators=[Optional(), Length(max=20)])
    bio            = StringField("Bio", validators=[Optional(), Length(max=300)])
    submit         = SubmitField("Guardar cambios")


class ChangePasswordForm(FlaskForm):
    current  = PasswordField("Contraseña actual", validators=[DataRequired()])
    new_pass = PasswordField("Nueva contraseña", validators=[DataRequired(), Length(min=8)])
    confirm  = PasswordField("Confirmar nueva", validators=[DataRequired(), EqualTo("new_pass")])
    submit   = SubmitField("Cambiar contraseña")
