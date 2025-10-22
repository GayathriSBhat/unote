import subprocess
import pymysql
from .config import settings

def setup_database():
    """One-time setup script to initialize database and user"""
    try:
        # Create SQL commands
        sql_commands = f"""
        CREATE DATABASE IF NOT EXISTS {settings.MYSQL_DB};
        CREATE USER IF NOT EXISTS '{settings.MYSQL_USER}'@'localhost' IDENTIFIED BY '{settings.MYSQL_PASSWORD}';
        GRANT ALL PRIVILEGES ON {settings.MYSQL_DB}.* TO '{settings.MYSQL_USER}'@'localhost';
        FLUSH PRIVILEGES;
        """
        
        # Execute commands through sudo
        process = subprocess.Popen(
            ['sudo', 'mysql', '-u', 'root'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Send commands to mysql
        stdout, stderr = process.communicate(input=sql_commands.encode())
        
        if process.returncode == 0:
            print(f"✓ Database '{settings.MYSQL_DB}' created")
            print(f"✓ User '{settings.MYSQL_USER}' created")
            print(f"✓ Privileges granted to '{settings.MYSQL_USER}'")
        else:
            print(f"✗ Setup failed: {stderr.decode()}")
            
    except Exception as e:
        print(f"✗ Setup failed: {e}")
        print("\nTo setup manually, run:")
        print("sudo mysql -u root")
        print("Then in MySQL prompt, run:")
        print(f"""
        CREATE DATABASE IF NOT EXISTS {settings.MYSQL_DB};
        CREATE USER '{settings.MYSQL_USER}'@'localhost' IDENTIFIED BY '{settings.MYSQL_PASSWORD}';
        GRANT ALL PRIVILEGES ON {settings.MYSQL_DB}.* TO '{settings.MYSQL_USER}'@'localhost';
        FLUSH PRIVILEGES;
        """)

if __name__ == "__main__":
    setup_database()