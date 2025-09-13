"""
Workflow Automation Agent for HR Advisor
Handles automated HR workflows including 360 reviews, onboarding, offboarding, and performance management
"""

import asyncio
import json
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class WorkflowType(Enum):
    ONBOARDING = "onboarding"
    OFFBOARDING = "offboarding"
    PERFORMANCE_REVIEW = "performance_review"
    REVIEW_360 = "360_review"
    COMPLIANCE_CHECK = "compliance_check"
    TRAINING_ASSIGNMENT = "training_assignment"
    POLICY_ACKNOWLEDGMENT = "policy_acknowledgment"
    PROBATION_REVIEW = "probation_review"
    SALARY_REVIEW = "salary_review"
    PROMOTION_PROCESS = "promotion_process"

class WorkflowStatus(Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    OVERDUE = "overdue"

class StepType(Enum):
    TASK = "task"
    APPROVAL = "approval"
    FORM = "form"
    NOTIFICATION = "notification"
    DOCUMENT = "document"
    MEETING = "meeting"
    TRAINING = "training"
    EVALUATION = "evaluation"

@dataclass
class WorkflowStep:
    step_id: str
    title: str
    description: str
    step_type: StepType
    assignee_role: str
    assignee_email: Optional[str]
    due_date: datetime
    dependencies: List[str]  # List of step_ids that must complete first
    form_template: Optional[Dict[str, Any]] = None
    documents_required: List[str] = None
    auto_complete: bool = False
    completed: bool = False
    completed_date: Optional[datetime] = None
    completed_by: Optional[str] = None
    notes: Optional[str] = None

@dataclass
class Workflow:
    workflow_id: str
    workflow_type: WorkflowType
    title: str
    description: str
    employee_id: str
    employee_name: str
    employee_email: str
    manager_id: Optional[str]
    manager_email: Optional[str]
    hr_contact: str
    status: WorkflowStatus
    created_date: datetime
    start_date: datetime
    target_completion_date: datetime
    actual_completion_date: Optional[datetime]
    steps: List[WorkflowStep]
    metadata: Dict[str, Any]
    country: str = "US"

class WorkflowAutomationAgent:
    def __init__(self):
        self.active_workflows: Dict[str, Workflow] = {}
        self.workflow_templates = self._initialize_templates()
        
    def _initialize_templates(self) -> Dict[WorkflowType, Dict[str, Any]]:
        """Initialize predefined workflow templates"""
        return {
            WorkflowType.ONBOARDING: {
                "title": "Employee Onboarding Process",
                "description": "Complete onboarding workflow for new employees",
                "duration_days": 30,
                "steps": [
                    {
                        "title": "Send Welcome Email",
                        "description": "Send welcome email with first day information",
                        "step_type": StepType.NOTIFICATION,
                        "assignee_role": "HR",
                        "days_offset": -3,
                        "auto_complete": True
                    },
                    {
                        "title": "Prepare Workspace",
                        "description": "Set up desk, equipment, and access credentials",
                        "step_type": StepType.TASK,
                        "assignee_role": "IT",
                        "days_offset": -1,
                        "documents_required": ["Equipment Checklist", "Access Request Form"]
                    },
                    {
                        "title": "First Day Orientation",
                        "description": "Conduct company orientation and introductions",
                        "step_type": StepType.MEETING,
                        "assignee_role": "HR",
                        "days_offset": 0
                    },
                    {
                        "title": "Complete New Hire Paperwork",
                        "description": "Fill out tax forms, benefits enrollment, emergency contacts",
                        "step_type": StepType.FORM,
                        "assignee_role": "Employee",
                        "days_offset": 1,
                        "form_template": {
                            "fields": ["tax_forms", "benefits_selection", "emergency_contacts", "bank_details"]
                        }
                    },
                    {
                        "title": "Department Introduction",
                        "description": "Meet team members and understand role expectations",
                        "step_type": StepType.MEETING,
                        "assignee_role": "Manager",
                        "days_offset": 2
                    },
                    {
                        "title": "Mandatory Training Completion",
                        "description": "Complete required compliance and safety training",
                        "step_type": StepType.TRAINING,
                        "assignee_role": "Employee",
                        "days_offset": 7
                    },
                    {
                        "title": "30-Day Check-in",
                        "description": "Review progress and address any concerns",
                        "step_type": StepType.EVALUATION,
                        "assignee_role": "Manager",
                        "days_offset": 30
                    }
                ]
            },
            
            WorkflowType.REVIEW_360: {
                "title": "360-Degree Performance Review",
                "description": "Comprehensive performance review with multi-source feedback",
                "duration_days": 21,
                "steps": [
                    {
                        "title": "Initiate Review Process",
                        "description": "Set up review cycle and notify participants",
                        "step_type": StepType.NOTIFICATION,
                        "assignee_role": "HR",
                        "days_offset": 0,
                        "auto_complete": True
                    },
                    {
                        "title": "Self-Assessment",
                        "description": "Employee completes self-evaluation form",
                        "step_type": StepType.FORM,
                        "assignee_role": "Employee",
                        "days_offset": 3,
                        "form_template": {
                            "fields": ["achievements", "challenges", "goals", "development_needs", "self_rating"]
                        }
                    },
                    {
                        "title": "Manager Assessment",
                        "description": "Direct manager completes performance evaluation",
                        "step_type": StepType.FORM,
                        "assignee_role": "Manager",
                        "days_offset": 7,
                        "form_template": {
                            "fields": ["performance_rating", "achievements", "areas_for_improvement", "goals", "development_plan"]
                        }
                    },
                    {
                        "title": "Peer Feedback Collection",
                        "description": "Collect feedback from 3-5 peer colleagues",
                        "step_type": StepType.FORM,
                        "assignee_role": "Peers",
                        "days_offset": 10,
                        "form_template": {
                            "fields": ["collaboration", "communication", "reliability", "innovation", "peer_rating"]
                        }
                    },
                    {
                        "title": "Direct Report Feedback",
                        "description": "Collect upward feedback from direct reports (if applicable)",
                        "step_type": StepType.FORM,
                        "assignee_role": "Direct Reports",
                        "days_offset": 10,
                        "form_template": {
                            "fields": ["leadership", "communication", "support", "development", "leadership_rating"]
                        }
                    },
                    {
                        "title": "Review Compilation",
                        "description": "Compile all feedback into comprehensive review",
                        "step_type": StepType.TASK,
                        "assignee_role": "HR",
                        "days_offset": 14
                    },
                    {
                        "title": "Review Meeting",
                        "description": "Conduct performance review discussion",
                        "step_type": StepType.MEETING,
                        "assignee_role": "Manager",
                        "days_offset": 18
                    },
                    {
                        "title": "Development Plan Creation",
                        "description": "Create personalized development plan based on feedback",
                        "step_type": StepType.DOCUMENT,
                        "assignee_role": "Manager",
                        "days_offset": 21
                    }
                ]
            },
            
            WorkflowType.OFFBOARDING: {
                "title": "Employee Offboarding Process",
                "description": "Complete offboarding workflow for departing employees",
                "duration_days": 14,
                "steps": [
                    {
                        "title": "Resignation Acknowledgment",
                        "description": "Acknowledge resignation and confirm last working day",
                        "step_type": StepType.NOTIFICATION,
                        "assignee_role": "HR",
                        "days_offset": 0,
                        "auto_complete": True
                    },
                    {
                        "title": "Knowledge Transfer Planning",
                        "description": "Plan knowledge transfer to team members",
                        "step_type": StepType.TASK,
                        "assignee_role": "Manager",
                        "days_offset": 1
                    },
                    {
                        "title": "Access Revocation",
                        "description": "Revoke system access and collect company property",
                        "step_type": StepType.TASK,
                        "assignee_role": "IT",
                        "days_offset": -1,
                        "documents_required": ["Asset Return Checklist"]
                    },
                    {
                        "title": "Exit Interview",
                        "description": "Conduct exit interview to gather feedback",
                        "step_type": StepType.MEETING,
                        "assignee_role": "HR",
                        "days_offset": -2,
                        "form_template": {
                            "fields": ["reason_for_leaving", "job_satisfaction", "management_feedback", "company_culture", "recommendations"]
                        }
                    },
                    {
                        "title": "Final Payroll Processing",
                        "description": "Process final salary, benefits, and accrued leave",
                        "step_type": StepType.TASK,
                        "assignee_role": "Payroll",
                        "days_offset": 0
                    },
                    {
                        "title": "Documentation Update",
                        "description": "Update employee records and close accounts",
                        "step_type": StepType.TASK,
                        "assignee_role": "HR",
                        "days_offset": 1
                    }
                ]
            }
        }
    
    async def create_workflow(self, workflow_type: WorkflowType, employee_data: Dict[str, Any], 
                            custom_params: Optional[Dict[str, Any]] = None) -> str:
        """Create a new workflow instance"""
        workflow_id = str(uuid.uuid4())
        template = self.workflow_templates[workflow_type]
        
        # Calculate dates
        start_date = datetime.now()
        if custom_params and 'start_date' in custom_params:
            start_date = custom_params['start_date']
        
        target_completion = start_date + timedelta(days=template['duration_days'])
        
        # Create workflow steps
        steps = []
        for step_template in template['steps']:
            step_id = str(uuid.uuid4())
            due_date = start_date + timedelta(days=step_template['days_offset'])
            
            step = WorkflowStep(
                step_id=step_id,
                title=step_template['title'],
                description=step_template['description'],
                step_type=StepType(step_template['step_type']),
                assignee_role=step_template['assignee_role'],
                assignee_email=self._get_assignee_email(step_template['assignee_role'], employee_data),
                due_date=due_date,
                dependencies=step_template.get('dependencies', []),
                form_template=step_template.get('form_template'),
                documents_required=step_template.get('documents_required', []),
                auto_complete=step_template.get('auto_complete', False)
            )
            steps.append(step)
        
        # Create workflow
        workflow = Workflow(
            workflow_id=workflow_id,
            workflow_type=workflow_type,
            title=template['title'],
            description=template['description'],
            employee_id=employee_data['employee_id'],
            employee_name=employee_data['name'],
            employee_email=employee_data['email'],
            manager_id=employee_data.get('manager_id'),
            manager_email=employee_data.get('manager_email'),
            hr_contact=employee_data.get('hr_contact', 'hr@company.com'),
            status=WorkflowStatus.ACTIVE,
            created_date=datetime.now(),
            start_date=start_date,
            target_completion_date=target_completion,
            actual_completion_date=None,
            steps=steps,
            metadata=custom_params or {},
            country=employee_data.get('country', 'US')
        )
        
        self.active_workflows[workflow_id] = workflow
        
        # Auto-complete any auto-complete steps
        await self._process_auto_complete_steps(workflow_id)
        
        return workflow_id
    
    def _get_assignee_email(self, role: str, employee_data: Dict[str, Any]) -> Optional[str]:
        """Get assignee email based on role"""
        role_mapping = {
            'Employee': employee_data.get('email'),
            'Manager': employee_data.get('manager_email'),
            'HR': employee_data.get('hr_contact', 'hr@company.com'),
            'IT': 'it@company.com',
            'Payroll': 'payroll@company.com',
            'Peers': None,  # Will be handled separately
            'Direct Reports': None  # Will be handled separately
        }
        return role_mapping.get(role)
    
    async def _process_auto_complete_steps(self, workflow_id: str):
        """Process steps that can be auto-completed"""
        workflow = self.active_workflows[workflow_id]
        
        for step in workflow.steps:
            if step.auto_complete and not step.completed:
                if step.step_type == StepType.NOTIFICATION:
                    # Send notification
                    await self._send_notification(workflow, step)
                    step.completed = True
                    step.completed_date = datetime.now()
                    step.completed_by = "System"
    
    async def _send_notification(self, workflow: Workflow, step: WorkflowStep):
        """Send email notification for workflow step"""
        # This would integrate with your email service
        print(f"Sending notification: {step.title} for workflow {workflow.title}")
        # Implementation would use SMTP or email service API
    
    async def complete_step(self, workflow_id: str, step_id: str, completed_by: str, 
                          form_data: Optional[Dict[str, Any]] = None, notes: Optional[str] = None) -> bool:
        """Mark a workflow step as completed"""
        if workflow_id not in self.active_workflows:
            return False
        
        workflow = self.active_workflows[workflow_id]
        
        # Find the step
        step = None
        for s in workflow.steps:
            if s.step_id == step_id:
                step = s
                break
        
        if not step or step.completed:
            return False
        
        # Check dependencies
        for dep_id in step.dependencies:
            dep_step = next((s for s in workflow.steps if s.step_id == dep_id), None)
            if not dep_step or not dep_step.completed:
                return False  # Dependencies not met
        
        # Complete the step
        step.completed = True
        step.completed_date = datetime.now()
        step.completed_by = completed_by
        step.notes = notes
        
        if form_data:
            step.metadata = form_data
        
        # Check if workflow is complete
        if all(s.completed for s in workflow.steps):
            workflow.status = WorkflowStatus.COMPLETED
            workflow.actual_completion_date = datetime.now()
        
        return True
    
    def get_workflow(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """Get workflow details"""
        if workflow_id not in self.active_workflows:
            return None
        
        workflow = self.active_workflows[workflow_id]
        return {
            'workflow': asdict(workflow),
            'progress': self._calculate_progress(workflow),
            'overdue_steps': self._get_overdue_steps(workflow),
            'next_steps': self._get_next_steps(workflow)
        }
    
    def _calculate_progress(self, workflow: Workflow) -> Dict[str, Any]:
        """Calculate workflow progress"""
        total_steps = len(workflow.steps)
        completed_steps = sum(1 for s in workflow.steps if s.completed)
        
        return {
            'total_steps': total_steps,
            'completed_steps': completed_steps,
            'progress_percentage': (completed_steps / total_steps) * 100 if total_steps > 0 else 0,
            'days_remaining': (workflow.target_completion_date - datetime.now()).days
        }
    
    def _get_overdue_steps(self, workflow: Workflow) -> List[Dict[str, Any]]:
        """Get overdue steps"""
        now = datetime.now()
        overdue = []
        
        for step in workflow.steps:
            if not step.completed and step.due_date < now:
                overdue.append({
                    'step_id': step.step_id,
                    'title': step.title,
                    'assignee_role': step.assignee_role,
                    'days_overdue': (now - step.due_date).days
                })
        
        return overdue
    
    def _get_next_steps(self, workflow: Workflow) -> List[Dict[str, Any]]:
        """Get next actionable steps"""
        next_steps = []
        
        for step in workflow.steps:
            if not step.completed:
                # Check if dependencies are met
                deps_met = all(
                    any(s.step_id == dep_id and s.completed for s in workflow.steps)
                    for dep_id in step.dependencies
                )
                
                if deps_met:
                    next_steps.append({
                        'step_id': step.step_id,
                        'title': step.title,
                        'description': step.description,
                        'assignee_role': step.assignee_role,
                        'due_date': step.due_date.isoformat(),
                        'step_type': step.step_type.value
                    })
        
        return next_steps
    
    def get_employee_workflows(self, employee_id: str) -> List[Dict[str, Any]]:
        """Get all workflows for an employee"""
        employee_workflows = []
        
        for workflow in self.active_workflows.values():
            if workflow.employee_id == employee_id:
                employee_workflows.append({
                    'workflow_id': workflow.workflow_id,
                    'title': workflow.title,
                    'type': workflow.workflow_type.value,
                    'status': workflow.status.value,
                    'progress': self._calculate_progress(workflow),
                    'created_date': workflow.created_date.isoformat(),
                    'target_completion': workflow.target_completion_date.isoformat()
                })
        
        return employee_workflows
    
    def get_pending_tasks(self, assignee_email: str) -> List[Dict[str, Any]]:
        """Get pending tasks for a specific assignee"""
        pending_tasks = []
        
        for workflow in self.active_workflows.values():
            if workflow.status in [WorkflowStatus.ACTIVE, WorkflowStatus.IN_PROGRESS]:
                for step in workflow.steps:
                    if (not step.completed and 
                        step.assignee_email == assignee_email and
                        all(any(s.step_id == dep_id and s.completed for s in workflow.steps) 
                            for dep_id in step.dependencies)):
                        
                        pending_tasks.append({
                            'workflow_id': workflow.workflow_id,
                            'workflow_title': workflow.title,
                            'step_id': step.step_id,
                            'step_title': step.title,
                            'description': step.description,
                            'due_date': step.due_date.isoformat(),
                            'employee_name': workflow.employee_name,
                            'step_type': step.step_type.value,
                            'overdue': step.due_date < datetime.now()
                        })
        
        return pending_tasks
    
    async def send_reminders(self):
        """Send reminders for overdue and upcoming tasks"""
        # This would be called by a scheduled job
        for workflow in self.active_workflows.values():
            if workflow.status in [WorkflowStatus.ACTIVE, WorkflowStatus.IN_PROGRESS]:
                overdue_steps = self._get_overdue_steps(workflow)
                
                for overdue in overdue_steps:
                    # Send overdue reminder
                    await self._send_reminder_notification(workflow, overdue, "overdue")
                
                # Check for upcoming due dates (within 2 days)
                upcoming_steps = [
                    s for s in workflow.steps 
                    if not s.completed and 
                    0 <= (s.due_date - datetime.now()).days <= 2
                ]
                
                for step in upcoming_steps:
                    await self._send_reminder_notification(workflow, step, "upcoming")
    
    async def _send_reminder_notification(self, workflow: Workflow, step: Any, reminder_type: str):
        """Send reminder notification"""
        # Implementation would send actual email/notification
        print(f"Sending {reminder_type} reminder for {step['title'] if isinstance(step, dict) else step.title}")

# Global instance
workflow_agent = WorkflowAutomationAgent()

