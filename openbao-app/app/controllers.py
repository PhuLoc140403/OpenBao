import requests
from .vault_postgresql import (
    configure_postgresql,
    create_postgresql_role,
    generate_postgresql_credentials,
)
from .vault_secrets import list_mounted_secrets
from .vault_config import get_vault_addr, get_headers

# Cấu hình OpenBao và thiết lập PostgreSQL nếu cần
configure_postgresql()
create_postgresql_role()
generate_postgresql_credentials()
mounted_secrets = list_mounted_secrets()


def get_secret(secret_name):
    """
    Lấy một bí mật từ OpenBao.

    Args:
        secret_name (str): Tên của bí mật cần lấy.

    Returns:
        dict: Dữ liệu bí mật hoặc None nếu có lỗi.
    """
    vault_addr = get_vault_addr()
    headers = get_headers()

    try:
        url = f"{vault_addr}/v1/secret/data/{secret_name}"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json().get("data", {}).get("data", None)
        else:
            print(f"Error retrieving secret: {response.status_code} - {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None


def store_secret(secret_name, secret_data):
    """
    Lưu trữ một bí mật vào OpenBao.

    Args:
        secret_name (str): Tên của bí mật.
        secret_data (dict): Dữ liệu bí mật cần lưu.

    Returns:
        bool: True nếu lưu thành công, False nếu thất bại.
    """
    vault_addr = get_vault_addr()
    headers = get_headers()

    try:
        url = f"{vault_addr}/v1/secret/data/{secret_name}"
        data = {"data": secret_data}
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200 or response.status_code == 204:
            print(f"Secret {secret_name} stored successfully.")
            return True
        else:
            print(f"Error storing secret: {response.status_code} - {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return False
