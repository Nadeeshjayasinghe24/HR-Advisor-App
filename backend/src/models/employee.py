from src.database import db
from datetime import datetime, date
import uuid

class Employee(db.Model):
    __tablename__ = 'employees'
    __table_args__ = {'extend_existing': True}
    
    employee_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.user_id'), nullable=False)
    full_name = db.Column(db.String(255), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(50), nullable=False)
    nationality = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(50), unique=True)
    email_address = db.Column(db.String(255), unique=True, nullable=False)
    residential_address = db.Column(db.Text)
    photo_url = db.Column(db.String(255))
    
    # Relationships
    user = db.relationship('User', back_populates='employees')
    emergency_contacts = db.relationship('EmergencyContact', backref='employee', lazy=True, cascade='all, delete-orphan')
    employment_details = db.relationship('EmploymentDetails', back_populates='employee', uselist=False, cascade='all, delete-orphan')
    payroll_compensation = db.relationship('PayrollCompensation', backref='employee', uselist=False, cascade='all, delete-orphan')
    attendance_records = db.relationship('AttendanceTimeTracking', backref='employee', lazy=True, cascade='all, delete-orphan')
    leave_records = db.relationship('LeaveManagement', backref='employee', lazy=True, cascade='all, delete-orphan')
    performance_records = db.relationship('PerformanceDevelopment', backref='employee', lazy=True, cascade='all, delete-orphan')
    compliance_records = db.relationship('ComplianceLegal', backref='employee', lazy=True, cascade='all, delete-orphan')
    system_access = db.relationship('SystemITAccess', backref='employee', uselist=False, cascade='all, delete-orphan')
    exit_details = db.relationship('ExitOffboarding', backref='employee', uselist=False, cascade='all, delete-orphan')
    optional_features = db.relationship('OptionalFeatures', backref='employee', uselist=False, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Employee {self.full_name}>'

    def to_dict(self):
        return {
            'employee_id': self.employee_id,
            'user_id': self.user_id,
            'full_name': self.full_name,
            'date_of_birth': self.date_of_birth.isoformat() if self.date_of_birth else None,
            'gender': self.gender,
            'nationality': self.nationality,
            'phone_number': self.phone_number,
            'email_address': self.email_address,
            'residential_address': self.residential_address,
            'photo_url': self.photo_url
        }

class EmergencyContact(db.Model):
    __tablename__ = 'emergency_contacts'
    __table_args__ = {'extend_existing': True}
    
    contact_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    employee_id = db.Column(db.String(36), db.ForeignKey('employees.employee_id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    relationship = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(50), nullable=False)

    def to_dict(self):
        return {
            'contact_id': self.contact_id,
            'employee_id': self.employee_id,
            'name': self.name,
            'relationship': self.relationship,
            'phone_number': self.phone_number
        }

class EmploymentDetails(db.Model):
    __tablename__ = 'employment_details'
    __table_args__ = {'extend_existing': True}
    
    employment_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    employee_id = db.Column(db.String(36), db.ForeignKey('employees.employee_id'), unique=True, nullable=False)
    job_title = db.Column(db.String(255), nullable=False)
    department = db.Column(db.String(255), nullable=False)
    manager_id = db.Column(db.String(36), db.ForeignKey('employees.employee_id'))
    employment_type = db.Column(db.String(50), nullable=False)
    employment_status = db.Column(db.String(50), nullable=False)
    date_of_joining = db.Column(db.Date, nullable=False)
    date_of_exit = db.Column(db.Date)
    work_location = db.Column(db.String(100), nullable=False)
    employee_grade = db.Column(db.String(50))
    work_shift_details = db.Column(db.Text)

    employee = db.relationship('Employee', back_populates='employment_details', foreign_keys=[employee_id])

    def to_dict(self):
        return {
            'employment_id': self.employment_id,
            'employee_id': self.employee_id,
            'job_title': self.job_title,
            'department': self.department,
            'manager_id': self.manager_id,
            'employment_type': self.employment_type,
            'employment_status': self.employment_status,
            'date_of_joining': self.date_of_joining.isoformat() if self.date_of_joining else None,
            'date_of_exit': self.date_of_exit.isoformat() if self.date_of_exit else None,
            'work_location': self.work_location,
            'employee_grade': self.employee_grade,
            'work_shift_details': self.work_shift_details
        }

class PayrollCompensation(db.Model):
    __tablename__ = 'payroll_compensation'
    __table_args__ = {'extend_existing': True}
    
    payroll_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    employee_id = db.Column(db.String(36), db.ForeignKey('employees.employee_id'), unique=True, nullable=False)
    salary_structure = db.Column(db.JSON, nullable=False)
    pay_frequency = db.Column(db.String(50), nullable=False)
    bank_account_details = db.Column(db.JSON, nullable=False)
    tax_id_number = db.Column(db.String(100), unique=True, nullable=False)
    social_security_details = db.Column(db.JSON)
    insurance_details = db.Column(db.JSON)
    overtime_rules_rates = db.Column(db.Text)
    deductions_contributions = db.Column(db.JSON)

    def to_dict(self):
        return {
            'payroll_id': self.payroll_id,
            'employee_id': self.employee_id,
            'salary_structure': self.salary_structure,
            'pay_frequency': self.pay_frequency,
            'bank_account_details': self.bank_account_details,
            'tax_id_number': self.tax_id_number,
            'social_security_details': self.social_security_details,
            'insurance_details': self.insurance_details,
            'overtime_rules_rates': self.overtime_rules_rates,
            'deductions_contributions': self.deductions_contributions
        }

class AttendanceTimeTracking(db.Model):
    __tablename__ = 'attendance_time_tracking'
    __table_args__ = {'extend_existing': True}
    
    attendance_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    employee_id = db.Column(db.String(36), db.ForeignKey('employees.employee_id'), nullable=False)
    record_date = db.Column(db.Date, nullable=False)
    clock_in_time = db.Column(db.DateTime)
    clock_out_time = db.Column(db.DateTime)
    work_hours = db.Column(db.Numeric(5, 2))
    remote_work_log = db.Column(db.Text)
    overtime_hours = db.Column(db.Numeric(5, 2))

    def to_dict(self):
        return {
            'attendance_id': self.attendance_id,
            'employee_id': self.employee_id,
            'record_date': self.record_date.isoformat() if self.record_date else None,
            'clock_in_time': self.clock_in_time.isoformat() if self.clock_in_time else None,
            'clock_out_time': self.clock_out_time.isoformat() if self.clock_out_time else None,
            'work_hours': float(self.work_hours) if self.work_hours else None,
            'remote_work_log': self.remote_work_log,
            'overtime_hours': float(self.overtime_hours) if self.overtime_hours else None
        }

class LeaveManagement(db.Model):
    __tablename__ = 'leave_management'
    __table_args__ = {'extend_existing': True}
    
    leave_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    employee_id = db.Column(db.String(36), db.ForeignKey('employees.employee_id'), nullable=False)
    leave_type = db.Column(db.String(50), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(50), nullable=False)
    approver_id = db.Column(db.String(36), db.ForeignKey('employees.employee_id'))
    approval_date = db.Column(db.Date)
    reason = db.Column(db.Text)

    def to_dict(self):
        return {
            'leave_id': self.leave_id,
            'employee_id': self.employee_id,
            'leave_type': self.leave_type,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'status': self.status,
            'approver_id': self.approver_id,
            'approval_date': self.approval_date.isoformat() if self.approval_date else None,
            'reason': self.reason
        }

class PerformanceDevelopment(db.Model):
    __tablename__ = 'performance_development'
    __table_args__ = {'extend_existing': True}
    
    performance_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    employee_id = db.Column(db.String(36), db.ForeignKey('employees.employee_id'), nullable=False)
    review_date = db.Column(db.Date, nullable=False)
    reviewer_id = db.Column(db.String(36), db.ForeignKey('employees.employee_id'))
    scores = db.Column(db.JSON)
    comments = db.Column(db.Text)
    kpis_okrs = db.Column(db.JSON)
    training_certifications = db.Column(db.Text)
    promotions_role_changes = db.Column(db.Text)
    employee_goals = db.Column(db.Text)
    awards_recognitions = db.Column(db.Text)

    def to_dict(self):
        return {
            'performance_id': self.performance_id,
            'employee_id': self.employee_id,
            'review_date': self.review_date.isoformat() if self.review_date else None,
            'reviewer_id': self.reviewer_id,
            'scores': self.scores,
            'comments': self.comments,
            'kpis_okrs': self.kpis_okrs,
            'training_certifications': self.training_certifications,
            'promotions_role_changes': self.promotions_role_changes,
            'employee_goals': self.employee_goals,
            'awards_recognitions': self.awards_recognitions
        }

class ComplianceLegal(db.Model):
    __tablename__ = 'compliance_legal'
    __table_args__ = {'extend_existing': True}
    
    compliance_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    employee_id = db.Column(db.String(36), db.ForeignKey('employees.employee_id'), nullable=False)
    document_type = db.Column(db.String(100), nullable=False)
    document_url = db.Column(db.String(255), nullable=False)
    issue_date = db.Column(db.Date)
    expiry_date = db.Column(db.Date)
    status = db.Column(db.String(50))
    disciplinary_actions = db.Column(db.Text)
    grievance_records = db.Column(db.Text)
    health_safety_compliance = db.Column(db.Text)

    def to_dict(self):
        return {
            'compliance_id': self.compliance_id,
            'employee_id': self.employee_id,
            'document_type': self.document_type,
            'document_url': self.document_url,
            'issue_date': self.issue_date.isoformat() if self.issue_date else None,
            'expiry_date': self.expiry_date.isoformat() if self.expiry_date else None,
            'status': self.status,
            'disciplinary_actions': self.disciplinary_actions,
            'grievance_records': self.grievance_records,
            'health_safety_compliance': self.health_safety_compliance
        }

class SystemITAccess(db.Model):
    __tablename__ = 'system_it_access'
    __table_args__ = {'extend_existing': True}
    
    access_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    employee_id = db.Column(db.String(36), db.ForeignKey('employees.employee_id'), unique=True, nullable=False)
    company_email = db.Column(db.String(255), unique=True, nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    role_based_access_level = db.Column(db.String(100), nullable=False)
    assigned_equipment = db.Column(db.JSON)
    software_licenses = db.Column(db.JSON)

    def to_dict(self):
        return {
            'access_id': self.access_id,
            'employee_id': self.employee_id,
            'company_email': self.company_email,
            'username': self.username,
            'role_based_access_level': self.role_based_access_level,
            'assigned_equipment': self.assigned_equipment,
            'software_licenses': self.software_licenses
        }

class ExitOffboarding(db.Model):
    __tablename__ = 'exit_offboarding'
    __table_args__ = {'extend_existing': True}
    
    exit_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    employee_id = db.Column(db.String(36), db.ForeignKey('employees.employee_id'), unique=True, nullable=False)
    resignation_reason = db.Column(db.Text)
    exit_interview_feedback = db.Column(db.Text)
    asset_return_status = db.Column(db.JSON)
    final_settlement_details = db.Column(db.JSON)
    exit_date = db.Column(db.Date, nullable=False)

    def to_dict(self):
        return {
            'exit_id': self.exit_id,
            'employee_id': self.employee_id,
            'resignation_reason': self.resignation_reason,
            'exit_interview_feedback': self.exit_interview_feedback,
            'asset_return_status': self.asset_return_status,
            'final_settlement_details': self.final_settlement_details,
            'exit_date': self.exit_date.isoformat() if self.exit_date else None
        }

class OptionalFeatures(db.Model):
    __tablename__ = 'optional_features'
    __table_args__ = {'extend_existing': True}
    
    optional_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    employee_id = db.Column(db.String(36), db.ForeignKey('employees.employee_id'), unique=True, nullable=False)
    skills_competencies = db.Column(db.JSON)
    career_pathing_preferences = db.Column(db.Text)
    employee_engagement_data = db.Column(db.JSON)
    wellness_support_usage = db.Column(db.JSON)
    internal_mobility_history = db.Column(db.JSON)

    def to_dict(self):
        return {
            'optional_id': self.optional_id,
            'employee_id': self.employee_id,
            'skills_competencies': self.skills_competencies,
            'career_pathing_preferences': self.career_pathing_preferences,
            'employee_engagement_data': self.employee_engagement_data,
            'wellness_support_usage': self.wellness_support_usage,
            'internal_mobility_history': self.internal_mobility_history
        }


