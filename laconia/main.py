import logging
import sys

from aiohttp import web

from laconia.config import config
from laconia.middlewares import deserializer_middleware
from laconia.redis import redis_client
from laconia.routes import register_routes

logger = logging.getLogger(__name__)


async def init_app(argv=None):
    """
    Create an application instance.

    During initialization we create an app, provide it with config object,
    initialize db and register routes
    :param argv: command line arguments
    :return: application instance
    """
    app = web.Application(middlewares=[deserializer_middleware], logger=logger)
    app["config"] = config
    app.cleanup_ctx.append(redis_client)
    register_routes(app)

    return app


def main(argv):
    """
    Initialize and serve application.

    Function is called when the module is run directly
    :param argv: command line arguments
    """
    app = init_app(argv)
    web.run_app(app, host=config["host"], port=config["port"])


if __name__ == "__main__":
    main(sys.argv[1:])
