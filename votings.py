import logging
import aiosqlite

from users import _insert_user

logger = logging.getLogger(__name__)

async def get_actual_voting_id() -> int | None:
    query = """
        SELECT id
        FROM voting
        WHERE voting_start <= date('now') AND voting_finish >= date('now')
        ORDER BY voting_start
        LIMIT 1;
    """
    async with aiosqlite.connect('db/base.db') as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(query) as cursor:
            row = await cursor.fetchone()
            if row is None:
                return None
            return row['id']

async def save_vote(user_telegram_id: int, books_ids: list[int]):
    actual_voting_id = await get_actual_voting_id()
    if not actual_voting_id:
        logger.warning("There is no actual voting in save_vote()")
        return
    await _insert_user(user_telegram_id)
    query = """
        INSERT OR REPLACE INTO vote (
            voting_id,
            bot_user_telegram_id,
            first_book_id,
            second_book_id,
            third_book_id
        )
        VALUES (?, ?, ?, ?, ?);
    """
    params = [actual_voting_id, user_telegram_id, *books_ids]
    async with aiosqlite.connect('db/base.db') as db:
        await db.execute(query, params)
        await db.commit()
