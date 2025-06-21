from fastapi import Form, Request, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
import secrets

from .app import app
from .templating import templating
from .depends import user_dependency
from .db import get_session
from . import config, storage, helpers


@app.get("/")
def root(request: Request, user = user_dependency):
    return templating.TemplateResponse(request, "root.html", {'user': user})


@app.get("/protected", name="protected")
def protected(request: Request, user=user_dependency):
    return user


@app.get("/login", name="login")
def login(request: Request):
    return templating.TemplateResponse(request, "login.html")


@app.post("/login")
async def create_auth(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    session: Session = Depends(get_session),
):
    user_class = config.get_user_class()
    username_field = getattr(user_class, "email")  # ! hardcoded
    user = session.query(user_class).where(username_field == username).first()
    if user is not None and helpers.verify_password(password, user.password_hash):
        session_token = secrets.token_hex(16)
        response = RedirectResponse(url="/protected", status_code=302)
        response.set_cookie(key=config.COOKIE_NAME, value=session_token, httponly=True, secure=False)
        storage.store(session_token, user.id)
        return response
    return HTTPException(status_code=403, detail='invalid credentials')
