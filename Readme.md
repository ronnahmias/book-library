# Book Library API

- Run App `uvicorn app.main:app --reload`

alembic revision --autogenerate -m "book_book_rep_tables"

alembic upgrade head
