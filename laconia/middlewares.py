import logging
import typing
from http import HTTPStatus
from json import JSONDecodeError

from aiohttp import web
from marshmallow import UnmarshalResult, ValidationError

from laconia.schemas import CreateLinkSchema

logger = logging.getLogger(__name__)


@web.middleware  # noqa: Z110
async def deserializer_middleware(
        request: web.Request,
        handler: typing.Callable[[web.Request], typing.Awaitable[web.Response]],
) -> web.Response:
    """
    Deserialize request's json body if it has one.

    :param request: request object
    :param handler: handler function
    :return:
    """
    if request.method in ["GET", "HEAD", "OPTIONS"]:
        return await handler(request)
    try:
        body = await request.text()
        unmarshalled_body: UnmarshalResult = CreateLinkSchema(strict=True).loads(body)
        request_data = unmarshalled_body.data
    except JSONDecodeError:
        return web.json_response(
            {"ok": False, "errors": {"body": "Cannot deserialize JSON."}},
            status=HTTPStatus.UNPROCESSABLE_ENTITY.value,
        )
    except ValidationError as exc:
        logger.exception(exc)
        return web.json_response(
            {"ok": False, "errors": exc.messages},
            status=HTTPStatus.UNPROCESSABLE_ENTITY.value,
        )
    request["data"] = request_data

    return await handler(request)
