from .templating import templating
from . import config


def login_view(request, context = {}, status_code = 200):
    default_context = {'username_field': config.USERNAME_FIELD_NAME}
    default_context.update(context)
    return templating.TemplateResponse(request, "login.html", default_context, status_code)