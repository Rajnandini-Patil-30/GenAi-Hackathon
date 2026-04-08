import os
import sys
import uuid
import datetime
from decimal import Decimal
from sqlalchemy import create_engine, text

def get_engine():
    engine = create_engine(
        "postgresql+pg8000://{}:{}@{}:{}/{}".format(
            os.getenv("DB_USER", "postgres"),
            os.getenv("DB_PASS", "studyplanner123"),
            os.getenv("DB_HOST", "localhost"),
            os.getenv("DB_PORT", "5432"),
            os.getenv("DB_NAME", "postgres"),
        )
    )
    return engine

def serialize(value):
    """Convert non-JSON-serializable types to strings."""
    if isinstance(value, uuid.UUID):
        return str(value)
    if isinstance(value, (datetime.date, datetime.datetime)):
        return value.isoformat()
    if isinstance(value, datetime.timedelta):
        return str(value)
    if isinstance(value, Decimal):
        return float(value)
    return value

def run_query(sql: str, params: dict = None):
    """Execute a query and return results as list of dicts."""
    engine = get_engine()
    with engine.connect() as conn:
        result = conn.execute(text(sql), params or {})
        if result.returns_rows:
            columns = result.keys()
            rows = []
            for row in result.fetchall():
                rows.append({
                    col: serialize(val)
                    for col, val in zip(columns, row)
                })
            return rows
        conn.commit()
        return {"status": "success", "rows_affected": result.rowcount}
