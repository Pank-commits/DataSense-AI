from app.db.database import engine
from sqlalchemy import text

columns = [
    "difficulty",
    "license",
    "rows",
    "columns",
    "file_size",
    "target_column",
    "language",
    "thumbnail",
    "rating",
]

with engine.connect() as conn:
    result = conn.execute(
        text("""
            SELECT column_name, is_nullable
            FROM information_schema.columns
            WHERE table_name = 'datasets'
            ORDER BY ordinal_position
        """)
    )

    for row in result:
        if row[0] in columns:
            print(row)