import pymysql
from .config import settings

def init_database():
    """Verify database connection with application user"""
    try:
        conn = pymysql.connect(
            host=settings.MYSQL_HOST,
            port=settings.MYSQL_PORT,
            user=settings.MYSQL_USER,
            password=settings.MYSQL_PASSWORD,
            database=settings.MYSQL_DB
        )
        print("✓ Database connection verified")
        conn.close()
    except Exception as e:
        print(f"✗ Database connection failed: {e}")
        print("\nRun setup_db.py first to initialize the database:")
        print("python -m app.setup_db")
        raise e