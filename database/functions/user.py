from database.config import get_db_connection
from utils.creator import create_table_if_not_exists


async def get_all_users():
    conn = await get_db_connection()

    try:
        rows = await conn.fetch(
            """
            SELECT id, username, first_name
            FROM users
            """
        )
        return rows
    finally:
        await conn.close()


async def insert_user_data(user_data):
    """
    Insert user data into the `users` table, avoiding duplicates.
    Args:
        user_data (dict): A dictionary containing user id, username, and first_name.
    """
    conn = await get_db_connection()

    await create_table_if_not_exists(
        conn,
        "users",
        """
        id BIGINT PRIMARY KEY,
        username TEXT,
        first_name TEXT
        """,
    )

    # Insert user data
    await conn.execute(
        """
        INSERT INTO users (id, username, first_name)
        VALUES ($1, $2, $3)
        ON CONFLICT (id) DO NOTHING
        """,
        user_data["id"],
        user_data["username"],
        user_data["first_name"],
    )

    await conn.close()


async def update_user_data(user_id, update_fields):
    conn = await get_db_connection()
    await conn.execute(
        """
        UPDATE users
        SET latest_data_id = $2
        WHERE id = $1
        """,
        user_id,
        update_fields.get("latest_data_id"),
    )
    await conn.close()
