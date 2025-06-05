#  Comando Para Arrancarlo Por consola      ./venv/bin/uvicorn scripts.main:app --reload
from fastapi import FastAPI, Request # type: ignore
from fastapi.staticfiles import StaticFiles # type: ignore
from fastapi.templating import Jinja2Templates # type: ignore
from routers import user_routes

from utils.auth import get_current_user_id
from database.conection import SessionLocal
from models.user import User
from routers import upload_routes
from fastapi.responses import HTMLResponse

from routers import admin_routes



app = FastAPI()

app.include_router(user_routes.router)

app.include_router(upload_routes.router)

app.include_router(admin_routes.router)


# Montar archivos estáticos (ej: imágenes, CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Directorio de las plantillas Jinja2
templates = Jinja2Templates(directory="templates")

# Ruta principal que muestra la página de inicio
@app.get("/", response_class=HTMLResponse)
async def mostrar_inicio(request: Request):
    user_id = get_current_user_id(request)
    user_name = None
    user_rol = None

    if user_id:
        db = SessionLocal()
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            user_name = user.nombre
            user_rol = user.rol
        db.close()

    return templates.TemplateResponse("index.html", {
        "request": request,
        "user_name": user_name,
        "user_rol": user_rol
    })

@app.get("/caracteristicas", response_class=HTMLResponse)
async def mostrar_caracteristicas(request: Request):
    user_id = get_current_user_id(request)
    user_name = None
    user_rol = None

    if user_id:
        db = SessionLocal()
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            user_name = user.nombre
            user_rol = user.rol
        db.close()

    return templates.TemplateResponse("caracteristicas.html", {
        "request": request,
        "user_name": user_name,
        "user_rol": user_rol
    })
