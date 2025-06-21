import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.exception_handlers import http_exception_handler
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException

from .models import create_all_tables, seed


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_all_tables()
    seed()
    yield


app = FastAPI(lifespan=lifespan)
static_files = StaticFiles(directory=os.path.join(os.path.dirname(__file__), 'static'))
app.mount('/static', static_files, 'static')


@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 401 and "session_token" in str(exc.detail):
        return RedirectResponse(url="/login")
    return await http_exception_handler(request, exc)  # fallback
