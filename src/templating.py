import os
from fastapi.templating import Jinja2Templates


templating = Jinja2Templates(
    os.path.join(os.path.dirname(__file__), 'templates')
)
