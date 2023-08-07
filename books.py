from dataclasses import dataclass, field
from datetime import datetime
import aiosqlite


@dataclass(frozen=False, kw_only=True)
class Book:
    id: int
    name: str
    category_id: int
    category_name: str
    read_start: datetime
    read_finish: datetime

    def __post_init__(self):
        for curr_field in ('read_start', 'read_finish'):
            value = getattr(self, curr_field)
            if value is None:
                continue
            value = datetime.strptime(value, '%Y-%m-%d')
            setattr(self, curr_field, value)


@dataclass
class Category:
    id: int
    name: str
    books: list[Book] = field(default_factory=list)


def _group_books_by_categories(books: list[Book]) -> list[Category]:
    categories = []
    category_id = None
    for book in books:
        if category_id != book.category_id:
            categories.append(
                Category(
                    id=book.category_id,
                    name=book.category_name,
                    books=[book]
                )
            )
            category_id = book.category_id
            continue
        categories[-1].books.append(book)
    return categories


def select_from_books_join_on_category():
    return """
        SELECT
            b.id AS book_id,
            b.name AS book_name,
            b.category_id,
            bc.name AS category_name,
            b.read_start,
            b.read_finish
        FROM book AS b
        JOIN book_category AS bc
            ON b.category_id = bc.id
    """


async def _execute_query_get_books(query, params=None) -> list[Book]:
    books = []
    async with aiosqlite.connect('db/base.db') as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(query, params) as cursor:
            async for row in cursor:
                books.append(Book(
                    id=row["book_id"],
                    name=row["book_name"],
                    category_id=row["category_id"],
                    category_name=row["category_name"],
                    read_start=row["read_start"],
                    read_finish=row["read_finish"]
                ))
    return books


async def get_all_books() -> list[Category]:
    query = select_from_books_join_on_category()
    query += """
        ORDER BY bc."ordering", b."ordering";
    """
    return _group_books_by_categories(
        await _execute_query_get_books(query)
    )


async def get_not_started_books() -> list[Category]:
    query = select_from_books_join_on_category()
    query += """
        WHERE b.read_start IS NULL
        ORDER BY bc."ordering", b."ordering";
    """
    return _group_books_by_categories(
        await _execute_query_get_books(query)
    )


async def get_already_read_books() -> list[Book]:
    query = select_from_books_join_on_category()
    query += """
        WHERE b.read_finish <= date('now')
        ORDER BY b.read_start;
    """
    return await _execute_query_get_books(query)


async def get_now_reading_book() -> list[Book]:
    query = select_from_books_join_on_category()
    query += """
        WHERE read_start <= date('now') AND read_finish >= date('now')
        ORDER BY b.read_start;
    """
    return await _execute_query_get_books(query)

async def get_books_by_ids(book_ids: list[str]) -> list[Book]:
    query = select_from_books_join_on_category()
    query += """
        WHERE
            read_start IS NULL AND b.id IN (?, ?, ?)
        ORDER BY
            CASE b.id
                WHEN ? THEN 1
                WHEN ? THEN 2
                WHEN ? THEN 3
            END;
    """
    return await _execute_query_get_books(query, (*book_ids, *book_ids))

