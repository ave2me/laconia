from aioredis import create_redis
from aioredis.commands import Redis

from laconia.helpers import generate_key


async def redis_client(app):
    """
    Handle redis set up and tear down.

    :param app: application instance
    """
    redis_config = app["config"]["redis"]
    address = (redis_config["host"], redis_config["port"])
    redis = await create_redis(address=address)
    app["redis_client"]: Redis = redis
    yield
    redis.close()
    await redis.wait_closed()


async def create_link(client: Redis, link: str) -> str:
    key = generate_key()
    await client.set(key, link)

    return key


async def get_link(client: Redis, key: str) -> str:
    link = await client.get(key, encoding="ascii")

    return link
