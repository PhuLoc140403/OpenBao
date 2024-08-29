import requests
from .vault_config import get_vault_addr, get_headers
import psycopg2

# Lấy địa chỉ Vault và headers từ cấu hình
vault_addr = get_vault_addr()
headers = get_headers()


def configure_postgresql():
    """
    Cấu hình plugin PostgreSQL trong OpenBao.
    """
    try:
        # Kiểm tra xem cấu hình PostgreSQL đã tồn tại hay chưa
        response = requests.get(
            f"{vault_addr}/v1/database/config/my-postgresql-database", headers=headers
        )
        if response.status_code == 200:
            print("PostgreSQL configuration already exists.")
            return
        else:
            print(f"Configuration not found. Status code: {response.status_code}")
            print(f"Response: {response.text}")

        # Dữ liệu cấu hình PostgreSQL
        data = {
            "plugin_name": "postgresql-database-plugin",
            "allowed_roles": ["my-role"],
            "connection_url": "postgresql://{{username}}:{{password}}@localhost:5432/openbao_db?sslmode=disable",
            "max_open_connections": 5,
            "max_connection_lifetime": "5s",
            "username": "postgres",
            "password": "postgres",
        }

        # Gửi yêu cầu cấu hình đến Vault
        response = requests.post(
            f"{vault_addr}/v1/database/config/my-postgresql-database",
            headers=headers,
            json=data,
        )
        if response.status_code == 204:
            print("PostgreSQL database configured successfully.")
        else:
            print(
                f"Error configuring PostgreSQL: {response.status_code} - {response.text}"
            )

    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")


def create_postgresql_role():
    """
    Tạo một role cho PostgreSQL trong OpenBao.
    """
    try:
        data = {
            "db_name": "my-postgresql-database",  # Tên của cấu hình cơ sở dữ liệu
            "creation_statements": [
                "CREATE ROLE \"{{name}}\" WITH LOGIN PASSWORD '{{password}}';",
                'GRANT SELECT ON ALL TABLES IN SCHEMA public TO "{{name}}";',
            ],
            "default_ttl": "1h",
            "max_ttl": "24h",
        }

        # Gửi yêu cầu tạo role đến Vault
        response = requests.post(
            f"{vault_addr}/v1/database/roles/my-role",
            headers=headers,
            json=data,
        )
        if response.status_code == 204:
            print("Role for PostgreSQL created successfully.")
        else:
            print(f"Error creating role: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")


def generate_postgresql_credentials():
    """
    Tạo thông tin đăng nhập tạm thời cho PostgreSQL.

    Returns:
        dict: Thông tin đăng nhập PostgreSQL hoặc None nếu có lỗi xảy ra.
    """
    try:
        # Gửi yêu cầu tạo thông tin đăng nhập đến Vault
        response = requests.get(
            f"{vault_addr}/v1/database/creds/my-role", headers=headers
        )
        if response.status_code == 200:
            credentials = response.json().get("data", {})
            print(f"Generated PostgreSQL credentials: {credentials}")
            return credentials
        else:
            print(
                f"Error generating credentials: {response.status_code} - {response.text}"
            )
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None


def query_postgresql(username, password):
    """
    Kết nối đến PostgreSQL và thực hiện truy vấn.

    Args:
        username (str): Tên người dùng PostgreSQL.
        password (str): Mật khẩu PostgreSQL.
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

        # Thực hiện truy vấn
        cursor.execute("SELECT * FROM users;")
        rows = cursor.fetchall()

        for row in rows:
            print(row)

    except Exception as error:
        print(f"Error while querying PostgreSQL: {error}")
    finally:
        if connection:
            cursor.close()
            connection.close()


# Cấu hình PostgreSQL khi khởi động
configure_postgresql()
create_postgresql_role()

# Tạo thông tin đăng nhập PostgreSQL và thực hiện truy vấn mẫu
credentials = generate_postgresql_credentials()
if credentials:
    query_postgresql(credentials["username"], credentials["password"])
