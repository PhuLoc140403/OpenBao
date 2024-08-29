# Backend lưu trữ
storage "file" {
  path = "C:/openbao/openbao-app/vault"  # Đường dẫn lưu trữ trên hệ thống của bạn
}

# Cấu hình địa chỉ và cổng
listener "tcp" {
  address     = "127.0.0.1:8200"
  tls_disable = 1
}

# API address
api_addr = "http://127.0.0.1:8200"

# Thiết lập Shamir Seal
seal "shamir" {
  secret_shares    = 5
  secret_threshold = 3
}
