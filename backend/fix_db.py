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
    for column in columns:
        conn.execute(
            text(
                f'ALTER TABLE datasets '
                f'ALTER COLUMN "{column}" DROP NOT NULL'
            )
        )

    conn.commit()

print("SUCCESS: optional dataset fields are now nullable")