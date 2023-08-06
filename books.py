from dataclasses import dataclass, field
from datetime import datetime
import aiosqlite


# def _chunk_list(lst, chunk_size):
#     for i in range(0, len(lst), chunk_size):
#         yield lst[i:i + chunk_size]


@dataclass(frozen=True, kw_only=True)
class Book:
    id: int
    name: str
    category_id: int
    category_name: str
    read_start: datetime
    read_finish: datetime


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




# async def get_all_books(chunk_size: int | None):
async def get_all_books() -> list[Category]:
    books = []
    query = """
        SELECT
            b.id AS book_id,
            b.name AS book_name,
            bc.id AS category_id,
            bc.name AS category_name,
            b.read_start,
            b.read_finish
        FROM book AS b
        LEFT JOIN book_category AS bc 
        ON b.category_id = bc.id
        ORDER BY bc."ordering", b."ordering";
    """
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
    # if chunk_size:
    #     return _chunk_list(books, chunk_size)
    return _group_books_by_categories(books)
