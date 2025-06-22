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
def root(request: Request, user=user_dependency):
    return templating.TemplateResponse(request, "root.html", {"user": user})


@app.get("/login", name="login")
def login(request: Request):
    return views.login_view(request)


@app.post("/login")
async def create_auth(
    request: Request, password: str = Form(...)
):
    form_data = await request.form()
    username = form_data.get(config.USERNAME_FIELD_NAME)
    user, session_token = helpers.authenticate(username, password)
    if user is not None:
        response = RedirectResponse(url="/", status_code=302)
        response.set_cookie(
            key=config.COOKIE_NAME, value=session_token, httponly=True, secure=False
        )
        storage.store(session_token, user.id)
        return response
    return views.login_view(request, {"username_error": "invalid_credentials"}, 422)


@app.post("/logout", name="logout")
async def logout(session_token: str = session_token_dep):
    storage.delete(session_token)
    response = RedirectResponse(url="/login", status_code=302)
    response.delete_cookie(key=config.COOKIE_NAME)
    return response
