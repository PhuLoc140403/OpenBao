import requests
import os
from dotenv import load_dotenv

# Tải các biến môi trường từ file .env nếu có
load_dotenv()

# Cấu hình OpenBao
vault_addr = os.getenv("VAULT_ADDR", "http://127.0.0.1:8200")
vault_token = os.getenv("VAULT_TOKEN", "s.vBZzrwXBqW0MpdJ1Oh57gKhK")
headers = {"X-Vault-Token": vault_token}


def get_vault_addr():
    """
    Trả về địa chỉ Vault hiện tại.
    """
    return vault_addr


def get_headers():
    """
    Trả về headers cần thiết để xác thực với Vault.
    """
    return headers


def get_secret(secret_name):
    """
    Truy xuất một secret từ Vault.

    Args:
        secret_name (str): Tên của secret cần truy xuất.

    Returns:
        dict: Dữ liệu của secret hoặc None nếu không tìm thấy.
    """
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
    Lưu trữ một secret vào Vault.

    Args:
        secret_name (str): Tên của secret.
        secret_data (dict): Dữ liệu của secret cần lưu trữ.

    Returns:
        bool: True nếu lưu trữ thành công, ngược lại là False.
    """
    try:
        url = f"{vault_addr}/v1/secret/data/{secret_name}"
        data = {"data": secret_data}
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200 or response.status_code == 204:
            return True
        else:
            print(f"Error storing secret: {response.status_code} - {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return False


def delete_secret(secret_name):
    """
    Xóa một secret từ Vault.

    Args:
        secret_name (str): Tên của secret cần xóa.

    Returns:
        bool: True nếu xóa thành công, ngược lại là False.
    """
    try:
        url = f"{vault_addr}/v1/secret/data/{secret_name}"
        response = requests.delete(url, headers=headers)
        if response.status_code == 204:
            return True
        else:
            print(f"Error deleting secret: {response.status_code} - {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return False
