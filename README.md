# 🐾 Huellitas Unidas DH

Aplicación web Full Stack para centralizar el rescate, adopción y localización de mascotas en **Dolores Hidalgo, Guanajuato**. Desarrollada por el equipo **DUBS**.

---

## 📋 Tabla de Contenidos

- [Descripción](#descripción)
- [Stack Tecnológico](#stack-tecnológico)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Instalación y Configuración](#instalación-y-configuración)
- [Migraciones de Base de Datos](#migraciones-de-base-de-datos)
- [Ejecutar la Aplicación](#ejecutar-la-aplicación)
- [Roles y Permisos](#roles-y-permisos)
- [Funcionalidades](#funcionalidades)
- [Despliegue en Render](#despliegue-en-render)
- [Extras Implementados](#extras-implementados)

---

## Descripción

Sustituye la desorganización de los grupos de Facebook por una base de datos estructurada donde cada mascota perdida, en adopción o en situación urgente tiene un **expediente digital** con seguimiento real hasta que regresa a casa o es adoptada.

---

## Stack Tecnológico

| Capa | Tecnología |
|------|-----------|
| Backend | Python 3.11+ · Flask 3.0 con Blueprints |
| ORM | SQLAlchemy · Flask-Migrate (Alembic) |
| Base de datos | PostgreSQL (SQLite para pruebas) |
| Autenticación | Flask-Login (sesiones) · Flask-Bcrypt · PyJWT (API) |
| Formularios | Flask-WTF · WTForms |
| Frontend | Jinja2 · Tailwind CSS (CDN) |
| Imágenes | Pillow (redimensionado local) |

---

## Estructura del Proyecto

```
huellitas_unidas/
├── app/
│   ├── __init__.py              # Application Factory
│   ├── models.py                # Todos los modelos SQLAlchemy
│   ├── utils.py                 # Helpers: imágenes, decoradores, zonas
│   ├── blueprints/
│   │   ├── main/                # Landing, búsqueda, errores
│   │   │   └── routes.py
│   │   ├── auth/                # Registro, login, perfil
│   │   │   ├── routes.py
│   │   │   └── forms.py
│   │   ├── pets/                # CRUD mascotas + comentarios
│   │   │   ├── routes.py
│   │   │   └── forms.py
│   │   ├── adoptions/           # Solicitudes de adopción
│   │   │   ├── routes.py
│   │   │   └── forms.py
│   │   └── admin/               # Panel de administración
│   │       └── routes.py
│   ├── templates/
│   │   ├── base.html            # Layout base con Navbar + Footer
│   │   ├── _macros.html         # Macros reutilizables de formularios
│   │   ├── main/
│   │   ├── auth/
│   │   ├── pets/
│   │   │   └── _card.html       # Partial: tarjeta de mascota
│   │   ├── adoptions/
│   │   ├── admin/
│   │   └── errors/              # 404, 500
│   └── static/
│       └── uploads/pets/        # Fotos de mascotas (local)
├── migrations/                  # Generado por Flask-Migrate
├── config.py                    # Configuraciones por entorno
├── run.py                       # Punto de entrada
├── requirements.txt
├── .env.example
└── README.md
```

---

## Instalación y Configuración

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/huellitas_unidas.git
cd huellitas_unidas
```

### 2. Crear y activar el entorno virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

```bash
cp .env.example .env
```

Edita el archivo `.env` con tus valores:

```env
SECRET_KEY=genera_una_clave_segura_con_python_secrets
FLASK_ENV=development
DATABASE_URL=postgresql://usuario:contraseña@localhost:5432/huellitas_db
JWT_SECRET_KEY=otro_secreto_seguro
```

> **Generar una clave secreta segura:**
> ```python
> python -c "import secrets; print(secrets.token_hex(32))"
> ```

### 5. Crear la base de datos PostgreSQL

```sql
CREATE DATABASE huellitas_db;
```

---

## Migraciones de Base de Datos

Flask-Migrate (basado en Alembic) te da un flujo de trabajo similar a Prisma:

```bash
# 1. Inicializar el sistema de migraciones (solo la primera vez)
flask db init

# 2. Generar una migración al detectar cambios en models.py
flask db migrate -m "descripción del cambio"

# 3. Aplicar la migración a la base de datos
flask db upgrade

# Otros comandos útiles:
flask db downgrade        # Revertir la última migración
flask db history          # Ver historial de migraciones
flask db current          # Ver migración activa
```

> **Nota:** Cada vez que modifiques `models.py`, ejecuta `flask db migrate` y `flask db upgrade`.

---

## Ejecutar la Aplicación

```bash
# Modo desarrollo (con recarga automática)
flask run

# O directamente:
python run.py
```

La app estará disponible en: **http://localhost:5000**

### Crear el primer administrador

Después de registrarte en la web, puedes promoverte a admin desde la consola Flask:

```bash
flask shell
```

```python
from app.models import db, User, UserRole
u = User.query.filter_by(email="tu@correo.com").first()
u.role = UserRole.ADMIN
db.session.commit()
print(f"Usuario {u.username} ahora es administrador.")
exit()
```

---

## Roles y Permisos

| Rol | Permisos |
|-----|---------|
| **Usuario General** | Registrarse, reportar mascotas, comentar, solicitar adopciones |
| **Rescatista Verificado** | Todo lo anterior + revisar/aprobar solicitudes de adopción, actualizar estados |
| **Administrador** | Control total: moderar contenido, cambiar roles, gestionar usuarios |

---

## Funcionalidades

### Módulo de Mascotas
- ✅ CRUD completo con soft-delete
- ✅ Estados: Perdido, En Adopción, Urgente, Encontrado, Adoptado
- ✅ Validación: una mascota no puede estar Perdida y En Adopción simultáneamente
- ✅ Filtros: por estado, zona, especie y búsqueda de texto
- ✅ Subida y redimensionado automático de fotos (Pillow, máx. 800×800)
- ✅ Historial completo de cambios de estado (PetStatusLog)
- ✅ Botón de contacto por WhatsApp directo

### Módulo de Adopciones
- ✅ Formulario digital de evaluación de candidatos
- ✅ Secciones: vivienda, convivencia, experiencia, compromiso
- ✅ Un solo flujo por usuario/mascota (sin duplicados)
- ✅ Revisión por rescatistas: aprobar o rechazar con notas
- ✅ Al aprobar → estado de la mascota cambia automáticamente a "Adoptado"

### Autenticación y Usuarios
- ✅ Registro con validación de correo/usuario únicos
- ✅ Login con "Recordarme"
- ✅ Perfil editable + cambio de contraseña
- ✅ WhatsApp de contacto por usuario

### Panel de Administración
- ✅ Dashboard con estadísticas en tiempo real
- ✅ Gestión de usuarios: cambiar rol, verificar, activar/desactivar
- ✅ Moderación de mascotas con restauración
- ✅ Registro de donaciones

### Seguridad
- ✅ Contraseñas hasheadas con bcrypt
- ✅ Protección CSRF en todos los formularios (Flask-WTF)
- ✅ Variables de entorno para credenciales
- ✅ Soft-delete (datos nunca se borran físicamente)
- ✅ Decoradores `@role_required` para rutas protegidas

---

## Despliegue en Render

1. Sube el proyecto a GitHub.
2. Crea un nuevo **Web Service** en [render.com](https://render.com).
3. Configura:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `flask db upgrade && gunicorn run:app`
4. Añade las variables de entorno en el panel de Render:
   - `SECRET_KEY`, `DATABASE_URL` (PostgreSQL de Render), `JWT_SECRET_KEY`, `FLASK_ENV=production`

> **Instalar Gunicorn** (para producción):
> ```bash
> pip install gunicorn
> pip freeze > requirements.txt
> ```

---

## Extras Implementados

Los siguientes módulos fueron añadidos más allá de los requisitos originales porque **tienen lógica directa con el dominio del problema**:

| Extra | Justificación |
|-------|--------------|
| **`PetStatusLog`** | El documento menciona "expediente con seguimiento real". Cada cambio de estado queda auditado con fecha, usuario y nota. |
| **`Donation`** | El documento menciona "seguimiento de apoyos económicos para animales heridos" y "gestión de fondos". Se registra monto, destinatario y si es anónima. |
| **`PetStatus.FOUND`** | Una mascota reportada como Perdida puede encontrarse sin necesariamente ser adoptada. Es un estado lógicamente necesario. |
| **Botón WhatsApp** | La app reemplaza a los grupos de Facebook donde el contacto era por mensajería. El botón genera el URL de WhatsApp con mensaje pre-llenado. |
| **Soft-delete** | Los reportes no se borran físicamente, solo se ocultan. Permite al admin restaurarlos y mantiene la integridad referencial. |
| **Zonas de DH** | Lista predefinida de colonias y zonas de Dolores Hidalgo para filtrado consistente y geolocalización. |

---

## Equipo DUBS

| Integrante | Rol |
|-----------|-----|
| Samae & Diego | Backend · Arquitectura de BD |
| Uriel | Frontend · UI/UX |
| Brayan | Seguridad · QA |
"# Huellitas-DH" 
