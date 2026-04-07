"""pets/forms.py"""
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, SelectField, DateField, DateTimeField, SubmitField
from wtforms.validators import DataRequired, Length, Optional
from app.models import PetStatus, PetSpecies
from app.utils import DOLORES_ZONES


def _zone_choices():
    return [("", "Selecciona una zona…")] + [(z, z) for z in DOLORES_ZONES]


class PetForm(FlaskForm):
    name              = StringField("Nombre", validators=[Optional(), Length(max=100)])
    species           = SelectField("Especie", choices=[(s, s) for s in PetSpecies.ALL], validators=[DataRequired()])
    breed             = StringField("Raza aproximada", validators=[Optional(), Length(max=100)])
    approximate_age   = StringField("Edad aproximada", validators=[Optional(), Length(max=50)])
    color             = StringField("Color / marcas físicas", validators=[DataRequired(), Length(max=100)])
    description       = TextAreaField("Señas particulares", validators=[DataRequired(), Length(min=10, max=1000)])
    status            = SelectField("Estado", choices=[(s, s) for s in PetStatus.ALL], validators=[DataRequired()])
    location_zone     = SelectField("Zona de la ciudad", choices=_zone_choices(), validators=[DataRequired()])
    location_reference= StringField("Referencia exacta", validators=[Optional(), Length(max=255)])
    last_seen_date    = DateField("Fecha de avistamiento", validators=[Optional()])
    image             = FileField("Foto", validators=[FileAllowed(["jpg","jpeg","png","gif","webp"], "Solo imágenes.")])
    submit            = SubmitField("Guardar")


class CommentForm(FlaskForm):
    content = TextAreaField("Comentario", validators=[DataRequired(), Length(min=2, max=500)])
    submit  = SubmitField("Comentar")


class StatusUpdateForm(FlaskForm):
    status = SelectField("Nuevo estado", choices=[(s, s) for s in PetStatus.ALL], validators=[DataRequired()])
    note   = StringField("Nota", validators=[Optional(), Length(max=255)])
    submit = SubmitField("Actualizar")


class SightingForm(FlaskForm):
    zone        = SelectField("Zona del avistamiento", choices=_zone_choices(), validators=[DataRequired()])
    reference   = StringField("Referencia / lugar exacto", validators=[Optional(), Length(max=255)])
    description = TextAreaField("¿Qué viste? ¿Cómo estaba?", validators=[DataRequired(), Length(min=10, max=500)])
    seen_at     = DateTimeField("Cuándo lo viste", format="%Y-%m-%dT%H:%M", validators=[DataRequired()])
    submit      = SubmitField("Reportar avistamiento")
