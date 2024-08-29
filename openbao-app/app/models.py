from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from .vault_integration import (
    store_password_in_vault,
    retrieve_password_from_vault,
    store_secret_in_vault,
    retrieve_secret_from_vault,
)

db = SQLAlchemy()


class Employee(db.Model):
    __tablename__ = "employees"

    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.String(10), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(10))
    date_of_birth = db.Column(db.Date)
    address = db.Column(db.String(200))
    phone_number_key = db.Column(db.String(50))  # Chứa khóa tham chiếu đến Vault
    email_key = db.Column(db.String(50))  # Chứa khóa tham chiếu đến Vault
    position_key = db.Column(db.String(50))  # Chứa khóa tham chiếu đến Vault
    department_key = db.Column(db.String(50))  #
    status = db.Column(db.String(20))

    def set_sensitive_data(self, phone_number, email, position, department):
        """Lưu trữ dữ liệu nhạy cảm trong Vault."""
        self.phone_number_key = store_secret_in_vault(
            f"employee/{self.employee_id}/phone_number", phone_number
        )
        self.email_key = store_secret_in_vault(
            f"employee/{self.employee_id}/email", email
        )
        self.position_key = store_secret_in_vault(
            f"employee/{self.employee_id}/position", position
        )
        self.department_key = store_secret_in_vault(
            f"employee/{self.employee_id}/department", department
        )

    def get_sensitive_data(self):
        """Lấy dữ liệu nhạy cảm từ Vault."""
        phone_number = retrieve_secret_from_vault(self.phone_number_key)
        email = retrieve_secret_from_vault(self.email_key)
        position = retrieve_secret_from_vault(self.position_key)
        department = retrieve_secret_from_vault(self.department_key)
        return phone_number, email, position, department

    def __repr__(self):
        return f"<Employee {self.name}>"


class Department(db.Model):
    __tablename__ = "departments"

    id = db.Column(db.Integer, primary_key=True)
    department_id = db.Column(db.String(10), unique=True, nullable=False)
    department_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    manager = db.Column(db.String(100))

    def __repr__(self):
        return f"<Department {self.department_name}>"


class Position(db.Model):
    __tablename__ = "positions"

    id = db.Column(db.Integer, primary_key=True)
    position_id = db.Column(db.String(10), unique=True, nullable=False)
    position_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    salary_coefficient = db.Column(db.Float)

    def __repr__(self):
        return f"<Position {self.position_name}>"


class Attendance(db.Model):
    __tablename__ = "attendances"

    id = db.Column(db.Integer, primary_key=True)
    attendance_id = db.Column(db.String(10), unique=True, nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey("employees.id"))
    date = db.Column(db.Date)
    check_in_time = db.Column(db.Time)
    check_out_time = db.Column(db.Time)

    def __repr__(self):
        return f"<Attendance {self.attendance_id}>"


class Salary(db.Model):
    __tablename__ = "salaries"

    id = db.Column(db.Integer, primary_key=True)
    salary_id = db.Column(db.String(10), unique=True, nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey("employees.id"))
    basic_salary_key = db.Column(db.String(50))  # Chứa khóa tham chiếu đến Vault
    salary_coefficient_key = db.Column(db.String(50))  # Chứa khóa tham chiếu đến Vault
    total_salary_key = db.Column(db.String(50))  # Chứa khóa tham chiếu đến Vault

    def set_salary_data(self, basic_salary, salary_coefficient, total_salary):
        """Lưu trữ dữ liệu lương trong Vault."""
        self.basic_salary_key = store_secret_in_vault(
            f"salary/{self.salary_id}/basic_salary", basic_salary
        )
        self.salary_coefficient_key = store_secret_in_vault(
            f"salary/{self.salary_id}/salary_coefficient", salary_coefficient
        )
        self.total_salary_key = store_secret_in_vault(
            f"salary/{self.salary_id}/total_salary", total_salary
        )

    def get_salary_data(self):
        """Lấy dữ liệu lương từ Vault."""
        basic_salary = retrieve_secret_from_vault(self.basic_salary_key)
        salary_coefficient = retrieve_secret_from_vault(self.salary_coefficient_key)
        total_salary = retrieve_secret_from_vault(self.total_salary_key)
        return basic_salary, salary_coefficient, total_salary

    def __repr__(self):
        return f"<Salary {self.salary_id}>"


class Role(db.Model):
    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.String(10), unique=True, nullable=False)
    role_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))

    def __repr__(self):
        return f"<Role {self.role_name}>"


class Users(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)

    def set_password(self, password):
        # Lưu mật khẩu vào OpenBao thay vì lưu trong cơ sở dữ liệu
        success = store_password_in_vault(self.username, password)
        if not success:
            raise Exception("Failed to store password in Vault.")

    def check_password(self, password):
        # Truy xuất mật khẩu từ OpenBao và so sánh với mật khẩu nhập vào
        stored_password = retrieve_password_from_vault(self.username)
        if stored_password is None:
            raise Exception("Failed to retrieve password from Vault.")
        return stored_password == password

    def __repr__(self):
        return f"<User {self.username}>"
