"""Formulario de solicitud de adopción."""
from flask_wtf import FlaskForm
from wtforms import (StringField, TextAreaField, SelectField,
                     BooleanField, SubmitField)
from wtforms.validators import DataRequired, Length, Optional


HOUSING_CHOICES = [
    ("", "Selecciona..."),
    ("Casa propia", "Casa propia"),
    ("Casa rentada", "Casa rentada"),
    ("Departamento propio", "Departamento propio"),
    ("Departamento rentado", "Departamento rentado"),
    ("Con familiares", "Con familiares"),
]

HOME_SIZE_CHOICES = [
    ("", "Selecciona..."),
    ("Pequeña (< 50 m²)", "Pequeña (< 50 m²)"),
    ("Mediana (50–100 m²)", "Mediana (50–100 m²)"),
    ("Grande (> 100 m²)", "Grande (> 100 m²)"),
]


class AdoptionRequestForm(FlaskForm):
    # Vivienda
    housing_type = SelectField("Tipo de vivienda", choices=HOUSING_CHOICES,
                               validators=[DataRequired()])
    home_size    = SelectField("Tamaño del hogar", choices=HOME_SIZE_CHOICES,
                               validators=[Optional()])
    has_yard     = BooleanField("Mi hogar tiene patio o jardín")

    # Convivencia
    has_children    = BooleanField("Hay niños en el hogar")
    children_ages   = StringField("Edades de los niños", validators=[Optional(), Length(max=100)])
    has_other_pets  = BooleanField("Tengo otras mascotas")
    other_pets_desc = StringField("Describe tus otras mascotas", validators=[Optional(), Length(max=255)])

    # Experiencia
    previous_pets    = BooleanField("He tenido mascotas antes")
    experience_desc  = TextAreaField("Cuéntanos sobre tu experiencia", validators=[Optional(), Length(max=500)])

    # Compromiso
    reason           = TextAreaField("¿Por qué quieres adoptar a esta mascota?",
                                     validators=[DataRequired(), Length(min=20, max=800)])
    aware_of_cost    = BooleanField("Entiendo que tendré gastos veterinarios, alimentación y cuidado",
                                   validators=[DataRequired(message="Debes aceptar este punto.")])
    accepts_home_visit = BooleanField("Acepto que un rescatista pueda visitar mi hogar")
    contact_address  = StringField("Dirección de contacto (colonia / zona)", validators=[Optional(), Length(max=255)])

    submit = SubmitField("Enviar solicitud de adopción")
