from .templating import templating


def login_view(request, context = {}, status_code = 200):
    return templating.TemplateResponse(request, "login.html", context, status_code)