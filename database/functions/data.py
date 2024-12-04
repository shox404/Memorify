from database.config import get_db_connection
from utils.creator import create_table_if_not_exists

async def save_simple_data(data):
    """
    Save simple data (id, image, text) into the `user_data` table.
    Args:
        data (dict): A dictionary containing id, image, and text.
    """
    conn = await get_db_connection()

    await create_table_if_not_exists(
        conn,
        "user_data",
        """
        id UUID PRIMARY KEY,
        image TEXT NOT NULL,
        text TEXT NOT NULL
        """,
    )

    await conn.execute(
        """
        INSERT INTO user_data (id, image, text)
        VALUES ($1, $2, $3)
        """,
        data["id"],
        data["image"],
        data["text"],
    )
    await conn.close()
