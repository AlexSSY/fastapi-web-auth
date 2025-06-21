from fastapi import Form, Request, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
import secrets

from .app import app
from .templating import templating
from .depends import user_dependency, session_token_dep
from .db import get_session
from . import config, storage, helpers, views


@app.get("/")
def root(request: Request, user = user_dependency):
    return templating.TemplateResponse(request, "root.html", {'user': user})


@app.get("/login", name="login")
def login(request: Request):
    return views.login_view(request)


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
        response = RedirectResponse(url="/", status_code=302)
        response.set_cookie(key=config.COOKIE_NAME, value=session_token, httponly=True, secure=False)
        storage.store(session_token, user.id)
        return response
    return views.login_view(request, {'username_error': 'invalid_credentials'}, 422)


@app.post('/logout', name='logout')
async def logout(request: Request, session_token: str = session_token_dep):
    if session_token:
        storage.delete(session_token)
    response = RedirectResponse(url="/login", status_code=302)
    response.delete_cookie(key=config.COOKIE_NAME)
    return response
