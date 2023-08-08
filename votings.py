from dataclasses import dataclass
import logging
from datetime import datetime

import aiosqlite

from users import _insert_user

logger = logging.getLogger(__name__)


@dataclass
class BookVoteResult:
    book_name: str
    score: int


@dataclass
class VoteResults:
    vote_start: str
    vote_finish: str
    leaders: list[BookVoteResult]

    def __post_init__(self):
        for curr_field in ('vote_start', 'vote_finish'):
            value = getattr(self, curr_field)
            if value is None:
                continue
            value = datetime.strptime(value, '%Y-%m-%d').strftime('%d.%m.%Y')
            setattr(self, curr_field, value)


@dataclass
class Voting:
    id: int
    voting_start: str
    voting_finish: str


async def get_actual_voting() -> Voting | None:
    query = """
        SELECT id, voting_start, voting_finish
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
            return Voting(
                id=row['id'],
                voting_start=row['voting_start'],
                voting_finish=row['voting_finish']
            )


async def save_vote(user_telegram_id: int, books_ids: list[int]):
    actual_voting = await get_actual_voting()
    if not actual_voting:
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
    params = [actual_voting.id, user_telegram_id, *books_ids]
    async with aiosqlite.connect('db/base.db') as db:
        await db.execute(query, params)
        await db.commit()


async def get_leaders() -> VoteResults | None:
    actual_voting = await get_actual_voting()
    if actual_voting is None:
        return None
    vote_results = VoteResults(
        vote_start=actual_voting.voting_start,
        vote_finish=actual_voting.voting_finish,
        leaders=list()
    )
    query = """
        WITH votes_by_id AS (
            SELECT first_book_id, second_book_id, third_book_id FROM vote WHERE voting_id=(:voting_id)
        ),combined_books AS (
            SELECT first_book_id AS book_id, COUNT(*)*3 AS score FROM votes_by_id
                GROUP BY book_id
            UNION
            SELECT second_book_id AS book_id, COUNT(*)*2 AS score FROM votes_by_id
                GROUP BY book_id
            UNION
            SELECT third_book_id AS book_id, COUNT(*) AS score FROM votes_by_id
                GROUP BY book_id
        )
        SELECT name, sum(score) AS score
        FROM combined_books
        JOIN book ON book_id = book.id
        GROUP BY book_id
        ORDER BY score DESC
        LIMIT 5;
    """
    async with aiosqlite.connect('db/base.db') as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(query, {"voting_id": actual_voting.id}) as cursor:
            rows = await cursor.fetchall()
            for row in rows:
                vote_results.leaders.append(
                    BookVoteResult(
                        book_name=row['name'],
                        score=row['score']
                    )
                )
    return vote_results
