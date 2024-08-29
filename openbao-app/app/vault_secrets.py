import requests
from .vault_config import get_vault_addr, get_headers

# Lấy địa chỉ Vault và headers từ cấu hình
vault_addr = get_vault_addr()
headers = get_headers()


def list_mounted_secrets():
    """
    Lấy danh sách các secret engines đã được kích hoạt trong OpenBao.

    Returns:
        dict: Danh sách các secret engines hoặc None nếu có lỗi xảy ra.
    """
    try:
        response = requests.get(f"{vault_addr}/v1/sys/mounts", headers=headers)
        if response.status_code == 200:
            mounts = response.json()
            # Lọc chỉ những mục có cấu trúc giống secret engine
            secret_engines = {
                k: v for k, v in mounts.items() if isinstance(v, dict) and "type" in v
            }
            return secret_engines
        else:
            print(f"Error listing mounts: {response.status_code} - {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None


def enable_secret_engine(engine_name, engine_type):
    """
    Kích hoạt một secret engine mới trong OpenBao.

    Args:
        engine_name (str): Tên của secret engine.
        engine_type (str): Loại của secret engine.

    Returns:
        bool: True nếu secret engine được kích hoạt thành công, ngược lại là False.
    """
    try:
        data = {"type": engine_type}
        response = requests.post(
            f"{vault_addr}/v1/sys/mounts/{engine_name}", headers=headers, json=data
        )
        if response.status_code == 204:
            print(
                f"Secret engine '{engine_name}' of type '{engine_type}' enabled successfully."
            )
            return True
        else:
            print(
                f"Error enabling secret engine: {response.status_code} - {response.text}"
            )
            return False
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return False


def read_secret(secret_path):
    """
    Đọc một secret từ OpenBao.

    Args:
        secret_path (str): Đường dẫn đến secret.

    Returns:
        dict: Dữ liệu của secret hoặc None nếu có lỗi xảy ra.
    """
    try:
        url = f"{vault_addr}/v1/secret/data/{secret_path}"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json().get("data", {}).get("data", None)
        else:
            print(f"Error retrieving secret: {response.status_code} - {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None


def write_secret(secret_path, secret_data):
    """
    Ghi một secret vào OpenBao.

    Args:
        secret_path (str): Đường dẫn đến secret.
        secret_data (dict): Dữ liệu của secret cần lưu.

    Returns:
        bool: True nếu ghi secret thành công, ngược lại là False.
    """
    try:
        url = f"{vault_addr}/v1/secret/data/{secret_path}"
        data = {"data": secret_data}
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200 or response.status_code == 204:
            print(f"Secret at '{secret_path}' written successfully.")
            return True
        else:
            print(f"Error writing secret: {response.status_code} - {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return False


# Kiểm tra các secret engines đã được kích hoạt
mounted_secrets = list_mounted_secrets()
if mounted_secrets:
    print("Mounted Secret Engines:")
    for mount, details in mounted_secrets.items():
        print(f"- Path: {mount}, Type: {details['type']}")
