import aiosqlite

async def _insert_user(user_telegram_id: int) -> None:
    query = """
        INSERT OR IGNORE INTO bot_user (telegram_id) VALUES (?);
    """
    async with aiosqlite.connect('db/base.db') as db:
        await db.execute(query, [user_telegram_id])
        await db.commit()
