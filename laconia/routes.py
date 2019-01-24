from aiohttp import web

from laconia.views import CreateLinkView, RedirectView


def register_routes(app: web.Application):
    """
    Register existing routes in the app instance.

    :param app: application instance
    """
    app.router.add_view("/create", CreateLinkView)
    app.router.add_view(r"/{key}", RedirectView)
