# import redis.asyncio as redis
# from app.core.config import settings


# redis_client = redis.Redis(host=settings.REDIS_HOST, port=6379, db=0)
# async def get_redis():
#     """
#     Dependency-injectable Redis client.
#     Usage: Depends(get_redis) in your routers/services.
#     """
#     yield redis_client