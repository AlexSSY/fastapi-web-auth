from fastapi import Request

from .app import app
from .templating import templating


@app.get('/')
def root(request: Request):
    return templating.TemplateResponse(request, 'root.html')
