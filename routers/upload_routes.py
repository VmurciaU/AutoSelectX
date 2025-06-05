# routers/upload_routes.py
from fastapi import APIRouter, Request, UploadFile, File, Form, Depends, status
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.templating import Jinja2Templates
import os, shutil
from utils.auth import get_current_user_id
from database.conection import SessionLocal
from models.user import User

router = APIRouter()
templates = Jinja2Templates(directory="templates")

UPLOAD_BASE_DIR = "outputs/session_files"

@router.get("/upload", response_class=HTMLResponse)
def show_upload_form(request: Request):
    user_id = get_current_user_id(request)
    if not user_id:
        return RedirectResponse(url="/login", status_code=302)

    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    user_name = user.nombre if user else None
    user_rol = user.rol if user else None
    db.close()

    user_folder = os.path.join(UPLOAD_BASE_DIR, str(user_id))
    files = os.listdir(user_folder) if os.path.exists(user_folder) else []

    return templates.TemplateResponse("upload.html", {
        "request": request,
        "files": files,
        "user_name": user_name,
        "user_rol": user_rol
    })

@router.post("/upload")
def handle_upload(
    request: Request,
    file: UploadFile = File(...)
):
    user_id = get_current_user_id(request)
    if not user_id:
        return RedirectResponse(url="/login", status_code=302)

    user_folder = os.path.join(UPLOAD_BASE_DIR, str(user_id))
    os.makedirs(user_folder, exist_ok=True)

    file_path = os.path.join(user_folder, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return RedirectResponse(url="/upload", status_code=status.HTTP_302_FOUND)

@router.post("/delete-file")
def delete_file(request: Request, filename: str = Form(...)):
    user_id = get_current_user_id(request)
    if not user_id:
        return RedirectResponse(url="/login", status_code=302)

    user_folder = os.path.join(UPLOAD_BASE_DIR, str(user_id))
    file_path = os.path.join(user_folder, filename)

    if os.path.exists(file_path):
        os.remove(file_path)

    return RedirectResponse(url="/upload", status_code=302)
