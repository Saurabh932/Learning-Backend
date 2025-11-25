from redis.asyncio import Redis
from src.config import config

JTI_EXPIRY = 3600

token_block_list = Redis.from_url(config.REDIS_URL)


async def add_jti_to_blocklist(jti : str) -> None:
    """Store JTI in Redis for blacklist"""
    await token_block_list.set(name=jti,
                               value="",
                               ex=JTI_EXPIRY)
    
    
async def token_in_blocklist(jti:str) -> bool:
    """Check if the JTI exists in Redis"""
    jti = await token_block_list.get(jti)
    
    return jti is not None