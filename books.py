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


async def _execute_query_get_books(query) -> list[Book]:
    books = []
    async with aiosqlite.connect('db/base.db') as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(query) as cursor:
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
    query = """
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
        ORDER BY bc."ordering", b."ordering";
    """
    return _group_books_by_categories(
        await _execute_query_get_books(query)
    )


async def get_not_started_books() -> list[Category]:
    query = """
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
        WHERE b.read_start IS NULL
        ORDER BY bc."ordering", b."ordering";
    """
    return _group_books_by_categories(
        await _execute_query_get_books(query)
    )


async def get_already_read_books() -> list[Book]:
    query = """
        SELECT
            b.id AS book_id,
            b.name AS book_name,
            b.category_id,
            bc.name as category_name,
            b.read_start,
            b.read_finish
        FROM book AS b
        JOIN book_category AS bc
            ON b.category_id = bc.id
        WHERE b.read_finish <= date('now')
        ORDER BY b.read_start;
        """
    return await _execute_query_get_books(query)


async def get_now_reading_book() -> list[Book]:
    query = """
        SELECT
            b.id AS book_id,
            b.name AS book_name,
            b.category_id,
            bc.name as category_name,
            b.read_start,
            b.read_finish
        FROM book as b
        JOIN book_category AS bc
            ON b.category_id = bc.id
        WHERE read_start <= date('now') AND read_finish >= date('now')
        ORDER BY b.read_start;
        """
    return await _execute_query_get_books(query)
