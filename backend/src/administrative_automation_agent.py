"""
Administrative Automation Agent for AnNi AI

Implements G-P requirements for automated administrative tasks:
- Automated contract generation
- Benefits administration automation  
- Payroll processing integration
- Document template auto-population
- Administrative workflow automation

G-P Insight: "Automate admin tasks" and "people work, not paperwork"
"""

import asyncio
import json
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import sqlite3
from pathlib import Path
import jinja2
import os

class DocumentType(Enum):
    EMPLOYMENT_CONTRACT = "employment_contract"
    OFFER_LETTER = "offer_letter"
    PERFORMANCE_REVIEW = "performance_review"
    POLICY_DOCUMENT = "policy_document"
    TRAINING_MATERIAL = "training_material"
    TERMINATION_LETTER = "termination_letter"
    BENEFITS_ENROLLMENT = "benefits_enrollment"
    PAYROLL_SUMMARY = "payroll_summary"

class AutomationStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    REQUIRES_REVIEW = "requires_review"

class Priority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

@dataclass
class AutomationTask:
    task_id: str
    task_type: str
    employee_id: Optional[str]
    user_id: str
    priority: Priority
    status: AutomationStatus
    parameters: Dict[str, Any]
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime]
    result: Optional[Dict[str, Any]]
    error_message: Optional[str]

@dataclass
class DocumentTemplate:
    template_id: str
    document_type: DocumentType
    country: str
    language: str
    template_content: str
    required_fields: List[str]
    legal_compliance: Dict[str, Any]
    version: str
    created_at: datetime
    updated_at: datetime

class AdministrativeAutomationAgent:
    """
    Handles automated administrative tasks for HR operations.
    
    Key capabilities:
    - Contract generation with legal compliance
    - Benefits administration automation
    - Document template management
    - Workflow automation
    - Integration with payroll systems
    """
    
    def __init__(self, project_root: str = None):
        # Auto-detect project root based on current file location
        if project_root is None:
            current_file = Path(__file__).resolve()
            # Go up from backend/src/administrative_automation_agent.py to project root
            self.project_root = current_file.parent.parent.parent
        else:
            self.project_root = Path(project_root)
            
        self.db_path = self.project_root / "backend" / "hr_advisor.db"
        self.templates_dir = self.project_root / "backend" / "templates"
        self.output_dir = self.project_root / "backend" / "generated_documents"
        
        # Create directories if they don't exist (including parent directories)
        self.templates_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize Jinja2 template engine
        self.jinja_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(str(self.templates_dir)),
            autoescape=jinja2.select_autoescape(['html', 'xml'])
        )
        
        # Country-specific legal requirements
        self.legal_requirements = {
            'singapore': {
                'employment_act': 'Employment Act (Chapter 91)',
                'minimum_wage': None,
                'probation_period': '6 months maximum',
                'notice_period': '1 month minimum',
                'annual_leave': '7-21 days based on service',
                'sick_leave': '14 days paid, 60 days hospitalization'
            },
            'australia': {
                'fair_work_act': 'Fair Work Act 2009',
                'minimum_wage': 'AUD 21.38/hour',
                'probation_period': '6 months maximum',
                'notice_period': '1-4 weeks based on service',
                'annual_leave': '4 weeks minimum',
                'sick_leave': '10 days personal/carer leave'
            },
            'malaysia': {
                'employment_act': 'Employment Act 1955',
                'minimum_wage': 'MYR 1,500/month',
                'probation_period': '4 months maximum',
                'notice_period': '4 weeks minimum',
                'annual_leave': '8-16 days based on service',
                'sick_leave': '14-60 days based on service'
            },
            'united_states': {
                'employment_law': 'At-will employment',
                'minimum_wage': 'USD 7.25/hour federal',
                'probation_period': 'No legal requirement',
                'notice_period': 'No legal requirement',
                'annual_leave': 'No legal requirement',
                'sick_leave': 'Varies by state'
            }
        }
        
        # Initialize database
        self._init_database()
    
    def _init_database(self):
        """Initialize database tables for administrative automation."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Automation tasks table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS automation_tasks (
                    task_id TEXT PRIMARY KEY,
                    task_type TEXT NOT NULL,
                    employee_id TEXT,
                    user_id TEXT NOT NULL,
                    priority TEXT NOT NULL,
                    status TEXT NOT NULL,
                    parameters TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    completed_at TIMESTAMP,
                    result TEXT,
                    error_message TEXT
                )
            ''')
            
            # Document templates table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS document_templates (
                    template_id TEXT PRIMARY KEY,
                    document_type TEXT NOT NULL,
                    country TEXT NOT NULL,
                    language TEXT NOT NULL,
                    template_content TEXT NOT NULL,
                    required_fields TEXT NOT NULL,
                    legal_compliance TEXT NOT NULL,
                    version TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Generated documents table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS generated_documents (
                    document_id TEXT PRIMARY KEY,
                    task_id TEXT NOT NULL,
                    document_type TEXT NOT NULL,
                    employee_id TEXT,
                    file_path TEXT NOT NULL,
                    metadata TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (task_id) REFERENCES automation_tasks (task_id)
                )
            ''')
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"Database initialization error: {str(e)}")
    
    async def create_automation_task(self, task_type: str, user_id: str, 
                                   parameters: Dict[str, Any], 
                                   employee_id: Optional[str] = None,
                                   priority: Priority = Priority.MEDIUM) -> str:
        """
        Create a new automation task.
        
        Args:
            task_type: Type of automation task
            user_id: ID of user requesting automation
            parameters: Task-specific parameters
            employee_id: Optional employee ID for employee-specific tasks
            priority: Task priority level
            
        Returns:
            Task ID for tracking
        """
        task_id = str(uuid.uuid4())
        
        task = AutomationTask(
            task_id=task_id,
            task_type=task_type,
            employee_id=employee_id,
            user_id=user_id,
            priority=priority,
            status=AutomationStatus.PENDING,
            parameters=parameters,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            completed_at=None,
            result=None,
            error_message=None
        )
        
        # Save to database
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO automation_tasks 
                (task_id, task_type, employee_id, user_id, priority, status, parameters)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                task.task_id,
                task.task_type,
                task.employee_id,
                task.user_id,
                task.priority.value,
                task.status.value,
                json.dumps(task.parameters)
            ))
            
            conn.commit()
            conn.close()
            
            # Process task asynchronously
            asyncio.create_task(self._process_automation_task(task_id))
            
            return task_id
            
        except Exception as e:
            print(f"Error creating automation task: {str(e)}")
            return None
    
    async def _process_automation_task(self, task_id: str):
        """Process an automation task based on its type."""
        try:
            # Update status to in progress
            await self._update_task_status(task_id, AutomationStatus.IN_PROGRESS)
            
            # Get task details
            task = await self._get_task(task_id)
            if not task:
                return
            
            # Route to appropriate handler
            if task['task_type'] == 'generate_contract':
                result = await self._generate_employment_contract(task)
            elif task['task_type'] == 'generate_offer_letter':
                result = await self._generate_offer_letter(task)
            elif task['task_type'] == 'process_benefits_enrollment':
                result = await self._process_benefits_enrollment(task)
            elif task['task_type'] == 'generate_performance_review':
                result = await self._generate_performance_review(task)
            elif task['task_type'] == 'process_payroll':
                result = await self._process_payroll_automation(task)
            elif task['task_type'] == 'generate_policy_document':
                result = await self._generate_policy_document(task)
            else:
                result = {'success': False, 'error': f'Unknown task type: {task["task_type"]}'}
            
            # Update task with result
            if result['success']:
                await self._update_task_completion(task_id, result)
            else:
                await self._update_task_error(task_id, result.get('error', 'Unknown error'))
                
        except Exception as e:
            await self._update_task_error(task_id, str(e))
    
    async def _generate_employment_contract(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Generate an employment contract based on parameters."""
        try:
            parameters = json.loads(task['parameters'])
            country = parameters.get('country', 'singapore').lower()
            
            # Get employee data
            employee_data = await self._get_employee_data(task['employee_id'])
            if not employee_data:
                return {'success': False, 'error': 'Employee not found'}
            
            # Get legal requirements for country
            legal_reqs = self.legal_requirements.get(country, self.legal_requirements['singapore'])
            
            # Prepare template data
            template_data = {
                'employee': employee_data,
                'company': parameters.get('company', {}),
                'position': parameters.get('position', {}),
                'compensation': parameters.get('compensation', {}),
                'legal_requirements': legal_reqs,
                'effective_date': parameters.get('effective_date', datetime.now().strftime('%Y-%m-%d')),
                'generated_date': datetime.now().strftime('%Y-%m-%d'),
                'contract_id': str(uuid.uuid4())[:8].upper()
            }
            
            # Generate contract
            template_name = f'employment_contract_{country}.html'
            if not (self.templates_dir / template_name).exists():
                # Use default template
                template_name = 'employment_contract_default.html'
                await self._create_default_contract_template(template_name)
            
            template = self.jinja_env.get_template(template_name)
            contract_html = template.render(**template_data)
            
            # Save generated contract
            filename = f"contract_{employee_data['employee_id']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
            file_path = self.output_dir / filename
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(contract_html)
            
            # Save document record
            await self._save_generated_document(
                task['task_id'],
                DocumentType.EMPLOYMENT_CONTRACT.value,
                task['employee_id'],
                str(file_path),
                template_data
            )
            
            return {
                'success': True,
                'document_path': str(file_path),
                'document_type': 'employment_contract',
                'employee_id': task['employee_id'],
                'metadata': template_data
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    async def _generate_offer_letter(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Generate an offer letter based on parameters."""
        try:
            parameters = json.loads(task['parameters'])
            
            # Prepare template data
            template_data = {
                'candidate': parameters.get('candidate', {}),
                'company': parameters.get('company', {}),
                'position': parameters.get('position', {}),
                'compensation': parameters.get('compensation', {}),
                'start_date': parameters.get('start_date'),
                'offer_expires': parameters.get('offer_expires'),
                'generated_date': datetime.now().strftime('%Y-%m-%d'),
                'offer_id': str(uuid.uuid4())[:8].upper()
            }
            
            # Generate offer letter
            template_name = 'offer_letter.html'
            if not (self.templates_dir / template_name).exists():
                await self._create_default_offer_template(template_name)
            
            template = self.jinja_env.get_template(template_name)
            offer_html = template.render(**template_data)
            
            # Save generated offer letter
            filename = f"offer_{template_data['candidate'].get('name', 'candidate').replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
            file_path = self.output_dir / filename
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(offer_html)
            
            # Save document record
            await self._save_generated_document(
                task['task_id'],
                DocumentType.OFFER_LETTER.value,
                None,  # No employee ID for offer letters
                str(file_path),
                template_data
            )
            
            return {
                'success': True,
                'document_path': str(file_path),
                'document_type': 'offer_letter',
                'metadata': template_data
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    async def _process_benefits_enrollment(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process benefits enrollment automation."""
        try:
            parameters = json.loads(task['parameters'])
            employee_id = task['employee_id']
            
            # Get employee data
            employee_data = await self._get_employee_data(employee_id)
            if not employee_data:
                return {'success': False, 'error': 'Employee not found'}
            
            # Process benefits selections
            benefits_data = {
                'employee': employee_data,
                'health_insurance': parameters.get('health_insurance', {}),
                'dental_insurance': parameters.get('dental_insurance', {}),
                'vision_insurance': parameters.get('vision_insurance', {}),
                'retirement_plan': parameters.get('retirement_plan', {}),
                'life_insurance': parameters.get('life_insurance', {}),
                'enrollment_date': parameters.get('enrollment_date', datetime.now().strftime('%Y-%m-%d')),
                'effective_date': parameters.get('effective_date'),
                'enrollment_id': str(uuid.uuid4())[:8].upper()
            }
            
            # Generate benefits enrollment document
            template_name = 'benefits_enrollment.html'
            if not (self.templates_dir / template_name).exists():
                await self._create_default_benefits_template(template_name)
            
            template = self.jinja_env.get_template(template_name)
            benefits_html = template.render(**benefits_data)
            
            # Save generated document
            filename = f"benefits_{employee_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
            file_path = self.output_dir / filename
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(benefits_html)
            
            # Save document record
            await self._save_generated_document(
                task['task_id'],
                DocumentType.BENEFITS_ENROLLMENT.value,
                employee_id,
                str(file_path),
                benefits_data
            )
            
            # TODO: Integrate with actual benefits system
            # This would typically involve API calls to benefits providers
            
            return {
                'success': True,
                'document_path': str(file_path),
                'document_type': 'benefits_enrollment',
                'employee_id': employee_id,
                'enrollment_id': benefits_data['enrollment_id'],
                'metadata': benefits_data
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    async def _process_payroll_automation(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process payroll automation tasks."""
        try:
            parameters = json.loads(task['parameters'])
            
            # This would typically integrate with payroll systems
            # For now, we'll generate a payroll summary document
            
            payroll_data = {
                'pay_period': parameters.get('pay_period'),
                'employees': parameters.get('employees', []),
                'company': parameters.get('company', {}),
                'generated_date': datetime.now().strftime('%Y-%m-%d'),
                'payroll_id': str(uuid.uuid4())[:8].upper()
            }
            
            # Generate payroll summary
            template_name = 'payroll_summary.html'
            if not (self.templates_dir / template_name).exists():
                await self._create_default_payroll_template(template_name)
            
            template = self.jinja_env.get_template(template_name)
            payroll_html = template.render(**payroll_data)
            
            # Save generated document
            filename = f"payroll_{payroll_data['pay_period']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
            file_path = self.output_dir / filename
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(payroll_html)
            
            # Save document record
            await self._save_generated_document(
                task['task_id'],
                DocumentType.PAYROLL_SUMMARY.value,
                None,
                str(file_path),
                payroll_data
            )
            
            return {
                'success': True,
                'document_path': str(file_path),
                'document_type': 'payroll_summary',
                'payroll_id': payroll_data['payroll_id'],
                'metadata': payroll_data
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    async def _create_default_contract_template(self, template_name: str):
        """Create a default employment contract template."""
        template_content = '''
<!DOCTYPE html>
<html>
<head>
    <title>Employment Contract</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }
        .header { text-align: center; margin-bottom: 30px; }
        .section { margin-bottom: 20px; }
        .signature { margin-top: 50px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>EMPLOYMENT CONTRACT</h1>
        <p>Contract ID: {{ contract_id }}</p>
        <p>Date: {{ generated_date }}</p>
    </div>
    
    <div class="section">
        <h2>PARTIES</h2>
        <p><strong>Employer:</strong> {{ company.name }}<br>
        Address: {{ company.address }}<br>
        Registration: {{ company.registration }}</p>
        
        <p><strong>Employee:</strong> {{ employee.first_name }} {{ employee.last_name }}<br>
        Address: {{ employee.address }}<br>
        Email: {{ employee.email }}</p>
    </div>
    
    <div class="section">
        <h2>POSITION AND DUTIES</h2>
        <p><strong>Position:</strong> {{ position.title }}</p>
        <p><strong>Department:</strong> {{ position.department }}</p>
        <p><strong>Start Date:</strong> {{ effective_date }}</p>
        <p><strong>Employment Type:</strong> {{ position.employment_type }}</p>
    </div>
    
    <div class="section">
        <h2>COMPENSATION</h2>
        <p><strong>Base Salary:</strong> {{ compensation.base_salary }} {{ compensation.currency }} per {{ compensation.frequency }}</p>
        {% if compensation.benefits %}
        <p><strong>Benefits:</strong> {{ compensation.benefits }}</p>
        {% endif %}
    </div>
    
    <div class="section">
        <h2>LEGAL REQUIREMENTS</h2>
        <p>This contract is governed by {{ legal_requirements.employment_act }}.</p>
        {% if legal_requirements.probation_period %}
        <p><strong>Probation Period:</strong> {{ legal_requirements.probation_period }}</p>
        {% endif %}
        <p><strong>Notice Period:</strong> {{ legal_requirements.notice_period }}</p>
        <p><strong>Annual Leave:</strong> {{ legal_requirements.annual_leave }}</p>
        <p><strong>Sick Leave:</strong> {{ legal_requirements.sick_leave }}</p>
    </div>
    
    <div class="signature">
        <table width="100%">
            <tr>
                <td width="50%">
                    <p>_________________________<br>
                    Employer Signature<br>
                    Date: ___________</p>
                </td>
                <td width="50%">
                    <p>_________________________<br>
                    Employee Signature<br>
                    Date: ___________</p>
                </td>
            </tr>
        </table>
    </div>
</body>
</html>
        '''
        
        with open(self.templates_dir / template_name, 'w', encoding='utf-8') as f:
            f.write(template_content)
    
    # Helper methods for database operations
    async def _get_employee_data(self, employee_id: str) -> Optional[Dict[str, Any]]:
        """Get employee data from database."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM employees WHERE employee_id = ?', (employee_id,))
            row = cursor.fetchone()
            
            if row:
                columns = [description[0] for description in cursor.description]
                employee_data = dict(zip(columns, row))
                conn.close()
                return employee_data
            
            conn.close()
            return None
            
        except Exception as e:
            print(f"Error getting employee data: {str(e)}")
            return None
    
    async def _update_task_status(self, task_id: str, status: AutomationStatus):
        """Update task status in database."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE automation_tasks 
                SET status = ?, updated_at = CURRENT_TIMESTAMP 
                WHERE task_id = ?
            ''', (status.value, task_id))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"Error updating task status: {str(e)}")
    
    async def _get_task(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get task details from database."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM automation_tasks WHERE task_id = ?', (task_id,))
            row = cursor.fetchone()
            
            if row:
                columns = [description[0] for description in cursor.description]
                task_data = dict(zip(columns, row))
                conn.close()
                return task_data
            
            conn.close()
            return None
            
        except Exception as e:
            print(f"Error getting task: {str(e)}")
            return None
    
    async def get_automation_status(self, user_id: str) -> Dict[str, Any]:
        """Get automation status and metrics for a user."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get task counts by status
            cursor.execute('''
                SELECT status, COUNT(*) as count 
                FROM automation_tasks 
                WHERE user_id = ? 
                GROUP BY status
            ''', (user_id,))
            
            status_counts = dict(cursor.fetchall())
            
            # Get recent tasks
            cursor.execute('''
                SELECT task_id, task_type, status, created_at, completed_at
                FROM automation_tasks 
                WHERE user_id = ? 
                ORDER BY created_at DESC 
                LIMIT 10
            ''', (user_id,))
            
            recent_tasks = []
            for row in cursor.fetchall():
                recent_tasks.append({
                    'task_id': row[0],
                    'task_type': row[1],
                    'status': row[2],
                    'created_at': row[3],
                    'completed_at': row[4]
                })
            
            conn.close()
            
            return {
                'status_counts': status_counts,
                'recent_tasks': recent_tasks,
                'total_tasks': sum(status_counts.values()),
                'success_rate': status_counts.get('completed', 0) / max(sum(status_counts.values()), 1) * 100
            }
            
        except Exception as e:
            return {'error': str(e)}

# Additional template creation methods would go here...
# (Abbreviated for space - would include methods for offer letters, benefits, payroll, etc.)

