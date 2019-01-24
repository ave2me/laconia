import logging
from http import HTTPStatus

from aiohttp import web

from laconia.helpers import construct_url
from laconia.redis import create_link, get_link

logger = logging.getLogger(__name__)


class RedisClientView(web.View):
    """
    Custom View class to provide a convinient way to access redis client.
    """

    @property
    def client(self):
        """
        Return redis client from a request instance. Makes code cleaner.

        :return: redis client
        """
        return self.request.app["redis_client"]  # type: ignore


class RedirectView(RedisClientView):
    """
    Handle redirect requests.
    """

    async def get(self):
        """
        Return redirect to a URL specified by a key.
        """
        key: str = self.request.match_info.get("key")
        if key is None:
            return web.json_response(
                {"ok": False, "errors": "A link with a given key was not found."},
                status=HTTPStatus.NOT_FOUND.value,
            )

        link = await get_link(self.client, key)

        raise web.HTTPMovedPermanently(link)


class CreateLinkView(RedisClientView):
    """
    Handle creation of short links.
    """

    async def post(self):
        """
        Create and return a short link.
        """
        link: str = self.request["data"]["link"]

        key = await create_link(self.client, link)
        url = construct_url(key)

        return web.json_response(
            {"ok": True, "url": url}, status=HTTPStatus.CREATED.value
        )
