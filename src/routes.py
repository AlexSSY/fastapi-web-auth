from fastapi import Request

from .app import app
from .templating import templating
from .depends import user_dependency


@app.get('/')
def root(request: Request):
    return templating.TemplateResponse(request, 'root.html')


@app.get('/protected', name='protected')
def protected(request: Request, user = user_dependency):
    return user


@app.get('/login')
def login(request: Request):
    return 0
