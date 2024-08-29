import requests
from psycopg2 import connect, sql
from .vault_postgresql import (
    configure_postgresql,
    create_postgresql_role,
    generate_postgresql_credentials,
)
from .vault_config import get_vault_addr, get_headers
import psycopg2

# Lấy địa chỉ Vault và headers từ cấu hình
vault_addr = get_vault_addr()
headers = get_headers()


def query_postgresql(username, password):
    """
    Kết nối và thực hiện truy vấn PostgreSQL bằng thông tin đăng nhập từ OpenBao.

    Args:
        username (str): Tên đăng nhập PostgreSQL.
        password (str): Mật khẩu PostgreSQL.

    Returns:
        None
    """
    try:
        # Kết nối đến cơ sở dữ liệu PostgreSQL sử dụng thông tin đăng nhập từ OpenBao
        connection = psycopg2.connect(
            dbname="openbao_db",
            user=username,
            password=password,
            host="localhost",
            port="5432",
        )
        cursor = connection.cursor()

        # Thực hiện truy vấn để lấy tất cả các nhân viên
        cursor.execute("SELECT * FROM employees;")
        rows = cursor.fetchall()

        print("Danh sách nhân viên:")
        for row in rows:
            print(row)

    except Exception as error:
        print(f"Error while querying PostgreSQL: {error}")
    finally:
        if connection:
            cursor.close()
            connection.close()


def main():
    # Cấu hình PostgreSQL trong OpenBao nếu cần
    configure_postgresql()
    # Tạo role PostgreSQL trong OpenBao nếu cần
    create_postgresql_role()

    # Lấy thông tin đăng nhập PostgreSQL từ OpenBao
    credentials = generate_postgresql_credentials()
    if credentials:
        username = credentials.get("username")
        password = credentials.get("password")

        # Sử dụng thông tin đăng nhập để truy vấn PostgreSQL
        query_postgresql(username, password)
    else:
        print("Failed to generate PostgreSQL credentials.")


if __name__ == "__main__":
    main()
