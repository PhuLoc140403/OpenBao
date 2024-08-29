import requests
from .vault_config import get_vault_addr, get_headers

# Lấy địa chỉ Vault và headers từ cấu hình
vault_addr = get_vault_addr()
headers = get_headers()


def store_password_in_vault(username, password):
    """
    Lưu trữ mật khẩu của người dùng vào Vault.

    Args:
        username (str): Tên người dùng.
        password (str): Mật khẩu của người dùng.

    Returns:
        bool: True nếu lưu trữ thành công, ngược lại là False.
    """
    try:
        url = f"{vault_addr}/v1/secret/data/{username}"
        data = {"data": {"password": password}}
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200 or response.status_code == 204:
            return True
        else:
            print(
                f"Error storing password in Vault: {response.status_code} - {response.text}"
            )
            return False
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return False


def retrieve_password_from_vault(username):
    """
    Truy xuất mật khẩu của người dùng từ Vault.

    Args:
        username (str): Tên người dùng.

    Returns:
        str: Mật khẩu của người dùng nếu truy xuất thành công, ngược lại là None.
    """
    try:
        url = f"{vault_addr}/v1/secret/data/{username}"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            secret_data = response.json().get("data", {}).get("data", {})
            return secret_data.get("password")
        else:
            print(
                f"Error retrieving password from Vault: {response.status_code} - {response.text}"
            )
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None


def update_password_in_vault(username, new_password):
    """
    Cập nhật mật khẩu của người dùng trong Vault.

    Args:
        username (str): Tên người dùng.
        new_password (str): Mật khẩu mới của người dùng.

    Returns:
        bool: True nếu cập nhật thành công, ngược lại là False.
    """
    return store_password_in_vault(username, new_password)


def delete_password_from_vault(username):
    """
    Xóa mật khẩu của người dùng khỏi Vault.

    Args:
        username (str): Tên người dùng.

    Returns:
        bool: True nếu xóa thành công, ngược lại là False.
    """
    try:
        url = f"{vault_addr}/v1/secret/data/{username}"
        response = requests.delete(url, headers=headers)
        if response.status_code == 204:
            return True
        else:
            print(
                f"Error deleting password from Vault: {response.status_code} - {response.text}"
            )
            return False
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return False


def store_secret_in_vault(secret_path, secret_value):
    """Lưu trữ giá trị bí mật vào Vault."""
    url = f"{vault_addr}/v1/secret/data/{secret_path}"
    data = {"data": {"value": secret_value}}
    response = requests.post(url, headers=headers, json=data)
    if response.status_code in [200, 204]:
        return secret_path  # Trả về đường dẫn bí mật làm khóa tham chiếu
    else:
        print(
            f"Error storing secret in Vault: {response.status_code} - {response.text}"
        )
        return None


def retrieve_secret_from_vault(secret_path):
    """Lấy giá trị bí mật từ Vault."""
    url = f"{vault_addr}/v1/secret/data/{secret_path}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get("data", {}).get("data", {}).get("value")
    else:
        print(
            f"Error retrieving secret from Vault: {response.status_code} - {response.text}"
        )
        return None


def store_secret_in_vault(secret_path, secret_value):
    """Lưu trữ giá trị bí mật vào Vault."""
    url = f"{vault_addr}/v1/secret/data/{secret_path}"
    data = {"data": {"value": secret_value}}
    response = requests.post(url, headers=headers, json=data)
    if response.status_code in [200, 204]:
        return secret_path  # Trả về đường dẫn bí mật làm khóa tham chiếu
    else:
        print(
            f"Error storing secret in Vault: {response.status_code} - {response.text}"
        )
        return None


def retrieve_secret_from_vault(secret_path):
    """Lấy giá trị bí mật từ Vault."""
    url = f"{vault_addr}/v1/secret/data/{secret_path}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get("data", {}).get("data", {}).get("value")
    else:
        print(
            f"Error retrieving secret from Vault: {response.status_code} - {response.text}"
        )
        return None
