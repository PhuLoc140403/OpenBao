from flask_wtf import FlaskForm
from flask_wtf.form import _Auto
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    DateField,
    SelectField,
    TextAreaField,
)
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from email_validator import validate_email, EmailNotValidError
from app.models import Users, Employee


class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField(
        "Repeat Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Register")

    def validate_username(self, username):
        user = Users.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError("Please use a different username.")

    def validate_email(self, email):
        user = Users.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError("Please use a different email address.")


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Sign In")


class EmployeeForm(FlaskForm):
    employee_id = StringField("Employee ID", validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired()])
    gender = SelectField(
        "Gender",
        choices=[("Male", "Male"), ("Female", "Female")],
        validators=[DataRequired()],
    )
    date_of_birth = DateField(
        "Date of Birth", format="%Y-%m-%d", validators=[DataRequired()]
    )
    address = StringField("Address", validators=[DataRequired()])
    phone_number = StringField("Phone Number", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    position = StringField("Position", validators=[DataRequired()])
    department = StringField("Department", validators=[DataRequired()])
    status = SelectField(
        "Status",
        choices=[("Active", "Active"), ("Inactive", "Inactive")],
        validators=[DataRequired()],
    )
    submit = SubmitField("Submit")

    def validate_email(self, email):
        user = Users.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError("Please use a different email address.")


class DepartmentForm(FlaskForm):
    department_id = StringField("Department ID", validators=[DataRequired()])
    department_name = StringField("Department Name", validators=[DataRequired()])
    description = TextAreaField("Description")
    manager = StringField("Manager", validators=[DataRequired()])
    submit = SubmitField("Submit")


class PositionForm(FlaskForm):
    position_id = StringField("Position ID", validators=[DataRequired()])
    position_name = StringField("Position Name", validators=[DataRequired()])
    description = TextAreaField("Description")
    salary_coefficient = StringField("Salary Coefficient", validators=[DataRequired()])
    submit = SubmitField("Submit")

    def validate_salary_coefficient(self, salary_coefficient):
        try:
            float(salary_coefficient.data)
        except ValueError:
            raise ValidationError("Salary coefficient must be a number.")

    def __init__(self, *args, **kwargs):
        super(PositionForm, self).__init__(*args, **kwargs)


class SalaryForm(FlaskForm):
    employee_id = StringField("Employee ID", validators=[DataRequired()])
    month = StringField("Month", validators=[DataRequired()])
    year = StringField("Year", validators=[DataRequired()])
    basic_salary = StringField("Basic Salary", validators=[DataRequired()])
    bonus = StringField("Bonus", validators=[DataRequired()])
    deduction = StringField("Deduction", validators=[DataRequired()])
    submit = SubmitField("Submit")

    def validate_basic_salary(self, basic_salary):
        try:
            float(basic_salary.data)
        except ValueError:
            raise ValidationError("Basic salary must be a number.")

    def validate_bonus(self, bonus):
        try:
            float(bonus.data)
        except ValueError:
            raise ValidationError("Bonus must be a number.")

    def validate_deduction(self, deduction):
        try:
            float(deduction.data)
        except ValueError:
            raise ValidationError("Deduction must be a number.")

    def __init__(self, *args, **kwargs):
        super(SalaryForm, self).__init__(*args, **kwargs)
        self.employee_id.choices = [(e.id, e.name) for e in Employee.query.all()]


class AttendanceForm(FlaskForm):
    employee_id = StringField("Employee ID", validators=[DataRequired()])
    date = DateField("Date", format="%Y-%m-%d", validators=[DataRequired()])
    check_in_time = StringField("Check In Time", validators=[DataRequired()])
    check_out_time = StringField("Check Out Time", validators=[DataRequired()])
    submit = SubmitField("Submit")

    def __init__(self, *args, **kwargs):
        super(AttendanceForm, self).__init__(*args, **kwargs)
        self.employee_id.choices = [(e.id, e.name) for e in Employee.query.all()]

    def validate_check_in_time(self, check_in_time):
        try:
            _Auto(check_in_time.data)
        except ValueError:
            raise ValidationError("Check in time must be a time.")

    def validate_check_out_time(self, check_out_time):
        try:
            _Auto(check_out_time.data)
        except ValueError:
            raise ValidationError("Check out time must be a time.")


class SearchForm(FlaskForm):
    search = StringField("Search", validators=[DataRequired()])
    submit = SubmitField("Search")
