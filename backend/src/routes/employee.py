from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.user import db
from src.models.employee import (
    Employee, EmergencyContact, EmploymentDetails, PayrollCompensation,
    AttendanceTimeTracking, LeaveManagement, PerformanceDevelopment,
    ComplianceLegal, SystemITAccess, ExitOffboarding, OptionalFeatures
)
from datetime import datetime

employee_bp = Blueprint('employee', __name__)

@employee_bp.route('/employees', methods=['POST'])
@jwt_required()
def add_employee():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['full_name', 'date_of_birth', 'gender', 'nationality', 'email_address']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        # Check if email already exists
        if Employee.query.filter_by(email_address=data['email_address']).first():
            return jsonify({'error': 'Email address already exists'}), 400
        
        # Parse date
        try:
            date_of_birth = datetime.strptime(data['date_of_birth'], '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
        
        # Create new employee
        new_employee = Employee(
            full_name=data['full_name'],
            date_of_birth=date_of_birth,
            gender=data['gender'],
            nationality=data['nationality'],
            phone_number=data.get('phone_number'),
            email_address=data['email_address'],
            residential_address=data.get('residential_address'),
            photo_url=data.get('photo_url')
        )
        
        db.session.add(new_employee)
        db.session.commit()
        
        return jsonify({
            'message': 'Employee added successfully',
            'employee_id': new_employee.employee_id,
            'employee': new_employee.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@employee_bp.route('/employees', methods=['GET'])
@jwt_required()
def get_employees():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        employees = Employee.query.paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'employees': [emp.to_dict() for emp in employees.items],
            'total': employees.total,
            'pages': employees.pages,
            'current_page': page
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@employee_bp.route('/employees/<employee_id>', methods=['GET'])
@jwt_required()
def get_employee(employee_id):
    try:
        employee = Employee.query.get_or_404(employee_id)
        
        # Get all related data
        employee_data = employee.to_dict()
        
        # Add related data
        employee_data['emergency_contacts'] = [contact.to_dict() for contact in employee.emergency_contacts]
        employee_data['employment_details'] = employee.employment_details.to_dict() if employee.employment_details else None
        employee_data['payroll_compensation'] = employee.payroll_compensation.to_dict() if employee.payroll_compensation else None
        employee_data['system_access'] = employee.system_access.to_dict() if employee.system_access else None
        employee_data['exit_details'] = employee.exit_details.to_dict() if employee.exit_details else None
        employee_data['optional_features'] = employee.optional_features.to_dict() if employee.optional_features else None
        
        # Add recent attendance, leave, performance records (last 5)
        employee_data['recent_attendance'] = [record.to_dict() for record in 
                                            employee.attendance_records[-5:]]
        employee_data['recent_leave'] = [record.to_dict() for record in 
                                       employee.leave_records[-5:]]
        employee_data['recent_performance'] = [record.to_dict() for record in 
                                             employee.performance_records[-5:]]
        employee_data['compliance_records'] = [record.to_dict() for record in 
                                             employee.compliance_records]
        
        return jsonify(employee_data), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@employee_bp.route('/employees/<employee_id>', methods=['PUT'])
@jwt_required()
def update_employee(employee_id):
    try:
        employee = Employee.query.get_or_404(employee_id)
        data = request.get_json()
        
        # Update basic employee fields
        if 'full_name' in data:
            employee.full_name = data['full_name']
        if 'date_of_birth' in data:
            try:
                employee.date_of_birth = datetime.strptime(data['date_of_birth'], '%Y-%m-%d').date()
            except ValueError:
                return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
        if 'gender' in data:
            employee.gender = data['gender']
        if 'nationality' in data:
            employee.nationality = data['nationality']
        if 'phone_number' in data:
            employee.phone_number = data['phone_number']
        if 'email_address' in data:
            # Check if new email already exists for another employee
            existing = Employee.query.filter_by(email_address=data['email_address']).first()
            if existing and existing.employee_id != employee_id:
                return jsonify({'error': 'Email address already exists'}), 400
            employee.email_address = data['email_address']
        if 'residential_address' in data:
            employee.residential_address = data['residential_address']
        if 'photo_url' in data:
            employee.photo_url = data['photo_url']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Employee updated successfully',
            'employee': employee.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@employee_bp.route('/employees/<employee_id>', methods=['DELETE'])
@jwt_required()
def delete_employee(employee_id):
    try:
        employee = Employee.query.get_or_404(employee_id)
        
        db.session.delete(employee)
        db.session.commit()
        
        return jsonify({'message': 'Employee deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Employment Details Routes
@employee_bp.route('/employees/<employee_id>/employment', methods=['POST', 'PUT'])
@jwt_required()
def manage_employment_details(employee_id):
    try:
        employee = Employee.query.get_or_404(employee_id)
        data = request.get_json()
        
        required_fields = ['job_title', 'department', 'employment_type', 'employment_status', 'date_of_joining', 'work_location']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        # Parse date
        try:
            date_of_joining = datetime.strptime(data['date_of_joining'], '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
        
        date_of_exit = None
        if data.get('date_of_exit'):
            try:
                date_of_exit = datetime.strptime(data['date_of_exit'], '%Y-%m-%d').date()
            except ValueError:
                return jsonify({'error': 'Invalid exit date format. Use YYYY-MM-DD'}), 400
        
        if employee.employment_details:
            # Update existing
            employment = employee.employment_details
            employment.job_title = data['job_title']
            employment.department = data['department']
            employment.manager_id = data.get('manager_id')
            employment.employment_type = data['employment_type']
            employment.employment_status = data['employment_status']
            employment.date_of_joining = date_of_joining
            employment.date_of_exit = date_of_exit
            employment.work_location = data['work_location']
            employment.employee_grade = data.get('employee_grade')
            employment.work_shift_details = data.get('work_shift_details')
        else:
            # Create new
            employment = EmploymentDetails(
                employee_id=employee_id,
                job_title=data['job_title'],
                department=data['department'],
                manager_id=data.get('manager_id'),
                employment_type=data['employment_type'],
                employment_status=data['employment_status'],
                date_of_joining=date_of_joining,
                date_of_exit=date_of_exit,
                work_location=data['work_location'],
                employee_grade=data.get('employee_grade'),
                work_shift_details=data.get('work_shift_details')
            )
            db.session.add(employment)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Employment details saved successfully',
            'employment_details': employment.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Emergency Contact Routes
@employee_bp.route('/employees/<employee_id>/emergency_contacts', methods=['POST'])
@jwt_required()
def add_emergency_contact(employee_id):
    try:
        employee = Employee.query.get_or_404(employee_id)
        data = request.get_json()
        
        required_fields = ['name', 'relationship', 'phone_number']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        contact = EmergencyContact(
            employee_id=employee_id,
            name=data['name'],
            relationship=data['relationship'],
            phone_number=data['phone_number']
        )
        
        db.session.add(contact)
        db.session.commit()
        
        return jsonify({
            'message': 'Emergency contact added successfully',
            'contact': contact.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@employee_bp.route('/employees/<employee_id>/emergency_contacts/<contact_id>', methods=['DELETE'])
@jwt_required()
def delete_emergency_contact(employee_id, contact_id):
    try:
        contact = EmergencyContact.query.filter_by(
            contact_id=contact_id, 
            employee_id=employee_id
        ).first_or_404()
        
        db.session.delete(contact)
        db.session.commit()
        
        return jsonify({'message': 'Emergency contact deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

