import asyncpg


async def get_db_connection():
    return await asyncpg.connect(
        user="admin",
        password="admin404",
        database="memorify",
        host="localhost",
    )
