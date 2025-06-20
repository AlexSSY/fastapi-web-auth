from fastapi import Request

from .app import app
from .models import User
from .db import SessionLocal


@app.middleware('http')
async def auth_middleware(request: Request, call_next):
    user_id_cookie = request.cookies.get('user_id')
    if user_id_cookie:
        user_id = int(user_id_cookie)
        with SessionLocal() as db:
            user = db.get(User, user_id)
            if user:
                request.user = user

    return await call_next(request)
