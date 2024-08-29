from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from app.models import (
    db,
    Users,
    Employee,
    Department,
    Position,
    Salary,
)  # Thay đổi từ 'User' thành 'Users'
from app.forms import (
    LoginForm,
    RegistrationForm,
    EmployeeForm,
    DepartmentForm,
    PositionForm,
    SalaryForm,
    AttendanceForm,
)
from .controllers import get_secret
import hvac
import os
from dotenv import load_dotenv

load_dotenv()

# Khởi tạo Vault client
vault_addr = os.getenv("VAULT_ADDR", "http://127.0.0.1:8200")
vault_token = os.getenv("VAULT_TOKEN", "s.vBZzrwXBqW0MpdJ1Oh57gKhK")
client = hvac.Client(url=vault_addr, token=vault_token)
main = Blueprint("main", __name__)


@main.route("/")
def index():
    if "username" in session:
        return render_template("index.html", username=session["username"])
    return redirect(url_for("main.login"))


@main.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = Users(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Congratulations, you are now a registered user!")
        return redirect(url_for("main.login"))
    return render_template("register.html", form=form)


@main.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("main.login"))
        session["username"] = user.username
        return redirect(url_for("main.index"))
    return render_template("login.html", form=form)


@main.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("main.index"))


@main.route("/employees", methods=["GET", "POST"])
def manage_employees():
    form = EmployeeForm()
    if form.validate_on_submit():
        # Xử lý thêm hoặc cập nhật thông tin nhân viên
        flash("Employee information saved successfully!")
        return redirect(url_for("main.index"))
    return render_template("employees.html", form=form)


@main.route("/add_employee", methods=["GET", "POST"])
def add_employee():
    form = EmployeeForm()
    if form.validate_on_submit():
        new_employee = Employee(
            employee_id=form.employee_id.data,
            name=form.name.data,
            gender=form.gender.data,
            date_of_birth=form.date_of_birth.data,
            address=form.address.data,
            status=form.status.data,
        )

        # Lưu dữ liệu nhạy cảm vào Vault
        new_employee.set_sensitive_data(
            phone_number=form.phone_number.data,
            email=form.email.data,
            position=form.position.data,
            department=form.department.data,
        )

        db.session.add(new_employee)
        db.session.commit()

        flash("Employee added successfully!")
        # Sử dụng đúng endpoint đã đăng ký
        return redirect(url_for("main.manage_employees"))

    return render_template("add_employee.html", form=form)


@main.route("/departments", methods=["GET", "POST"])
def manage_departments():
    form = DepartmentForm()
    if form.validate_on_submit():
        # Tạo một đối tượng Department mới với dữ liệu từ biểu mẫu
        new_department = Department(
            department_id=form.department_id.data,
            department_name=form.department_name.data,
            description=form.description.data,
            manager=form.manager.data,
        )

        # Thêm vào phiên làm việc và lưu vào cơ sở dữ liệu
        db.session.add(new_department)
        db.session.commit()

        flash("Department information saved successfully!")
        return redirect(url_for("main.index"))

    return render_template("departments.html", form=form)


@main.route("/positions", methods=["GET", "POST"])
def manage_positions():
    form = PositionForm()
    if form.validate_on_submit():
        # Tạo một đối tượng Position mới với dữ liệu từ biểu mẫu
        new_position = Position(
            position_id=form.position_id.data,
            position_name=form.position_name.data,
            description=form.description.data,
            salary_coefficient=form.salary_coefficient.data,
        )

        # Thêm vào phiên làm việc và lưu vào cơ sở dữ liệu
        db.session.add(new_position)
        db.session.commit()

        flash("Position information saved successfully!")
        return redirect(url_for("main.index"))

    return render_template("positions.html", form=form)


@main.route("/secrets")
def secret_view():
    try:
        secret_path = "my-secret"
        secret = client.secrets.kv.v2.read_secret_version(path=secret_path)
        secret_data = secret["data"]["data"]
        return render_template("secret.html", data=secret_data)
    except Exception as e:
        flash(f"Could not retrieve secret: {e}", "danger")
        return render_template("secret.html")


@main.route("/add_salary", methods=["GET", "POST"])
def add_salary():
    form = SalaryForm()
    if form.validate_on_submit():
        new_salary = Salary(
            salary_id=form.salary_id.data, employee_id=form.employee_id.data
        )

        # Lưu dữ liệu lương vào Vault
        new_salary.set_salary_data(
            basic_salary=form.basic_salary.data,
            salary_coefficient=form.salary_coefficient.data,
            total_salary=form.total_salary.data,
        )

        db.session.add(new_salary)
        db.session.commit()

        flash("Salary information added successfully!")
        return redirect(url_for("main.salary_list"))

    return render_template("add_salary.html", form=form)


@main.route("/attendances", methods=["GET", "POST"])
def manage_attendances():
    form = AttendanceForm()
    if form.validate_on_submit():
        # Xử lý logic lưu trữ hoặc cập nhật thông tin chấm công
        flash("Attendance information saved successfully!")
        return redirect(url_for("main.index"))
    return render_template("attendances.html", form=form)


@main.route("/employee_details/<int:employee_id>")
def employee_details(employee_id):
    # Lấy thông tin nhân viên từ cơ sở dữ liệu
    employee = Employee.query.get_or_404(employee_id)

    return render_template("employee_details.html", employee=employee)
