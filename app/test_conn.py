import pymysql
from tabulate import tabulate
from typing import List, Tuple

def test_connection():
    try:
        conn = pymysql.connect(
            host="127.0.0.1",
            port=3306,
            user="notes_user",
            password="notes_pass",
            db="notesdb",
            connect_timeout=5
        )
        print("✓ Database connection successful")
        return conn
    except Exception as e:
        print("✗ Connection error:", repr(e))
        return None

def print_table_data(cursor, table_name: str, columns: List[Tuple]):
    # Get column names
    headers = [col[0] for col in columns]
    
    # Get table contents
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    
    print(f"\n📋 Table: {table_name}")
    print(f"📊 Total rows: {len(rows)}")
    
    if rows:
        print(tabulate(rows, headers=headers, tablefmt="grid"))
    else:
        print("(empty table)")
    print("\n")

def print_database():
    conn = test_connection()
    if not conn:
        return
    
    try:
        with conn.cursor() as cursor:
            # Get all tables
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            
            print("\n=== 📚 Database Contents ===")
            for table in tables:
                table_name = table[0]
                
                # Get table structure
                cursor.execute(f"DESCRIBE {table_name}")
                columns = cursor.fetchall()
                
                # Print formatted table
                print_table_data(cursor, table_name, columns)
                
    except Exception as e:
        print(f"Error printing database: {repr(e)}")
    finally:
        conn.close()

if __name__ == "__main__":
    print_database()