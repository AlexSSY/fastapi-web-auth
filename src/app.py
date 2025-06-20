import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .models import create_all_tables, seed


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_all_tables()
    seed()
    yield


app = FastAPI(lifespan=lifespan)
static_files = StaticFiles(directory=os.path.join(os.path.dirname(__file__), 'static'))
app.mount('/static', static_files, 'static-files')
