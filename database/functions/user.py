from database.config import get_db_connection
from utils.creator import create_table_if_not_exists


async def get_all_users():
    """Read users from 'users' table"""

    db = await get_db_connection()

    try:
        return await db.fetch(
            """
            SELECT id, username, first_name
            FROM users
            """
        )
    finally:
        await db.close()


async def insert_user_data(user_data):
    """Insert user data into the 'users' table, avoiding duplicates"""

    db = await get_db_connection()

    await create_table_if_not_exists(
        db,
        "users",
        """
        id BIGINT PRIMARY KEY,
        username TEXT,
        first_name TEXT
        """,
    )

    await db.execute(
        """
        INSERT INTO users (id, username, first_name)
        VALUES ($1, $2, $3)
        ON CONFLICT (id) DO NOTHING
        """,
        user_data["id"],
        user_data["username"],
        user_data["first_name"],
    )

    await db.close()


async def update_user_data(user_id, update_fields):
    """Update user into 'users' by id"""

    db = await get_db_connection()
    await db.execute(
        """
        UPDATE users
        SET latest_data_id = $2
        WHERE id = $1
        """,
        user_id,
        update_fields.get("latest_data_id"),
    )
    await db.close()
