"""
AI Governance Agent for HR Advisor
Handles AI usage monitoring, approval workflows, compliance tracking, and governance oversight

Enhanced with G-P requirements:
- AI usage approval workflows (92% of executives require organizational approval)
- AI tool governance dashboard
- Usage monitoring and audit trails
- Compliance verification for AI decisions
- Risk assessment for AI recommendations
"""

import asyncio
import json
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import hashlib
import sqlite3
from pathlib import Path

class AIOperation(Enum):
    QUERY_PROCESSING = "query_processing"
    DOCUMENT_GENERATION = "document_generation"
    WORKFLOW_AUTOMATION = "workflow_automation"
    PREDICTIVE_ANALYSIS = "predictive_analysis"
    COMPLIANCE_CHECK = "compliance_check"
    EMPLOYEE_EVALUATION = "employee_evaluation"
    POLICY_RECOMMENDATION = "policy_recommendation"
    DATA_ANALYSIS = "data_analysis"

class ApprovalStatus(Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    CONDITIONAL = "conditional"
    EXPIRED = "expired"

class RiskLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class GovernanceRole(Enum):
    HR_ADMIN = "hr_admin"
    IT_ADMIN = "it_admin"
    COMPLIANCE_OFFICER = "compliance_officer"
    LEGAL_COUNSEL = "legal_counsel"
    DEPARTMENT_HEAD = "department_head"
    C_LEVEL = "c_level"

@dataclass
class AIUsageLog:
    log_id: str
    user_id: str
    user_email: str
    operation: AIOperation
    ai_provider: str
    model_used: str
    input_data_hash: str
    output_data_hash: str
    confidence_score: float
    tokens_used: int
    cost: float
    processing_time: float
    timestamp: datetime
    risk_level: RiskLevel
    compliance_flags: List[str]
    approved: bool
    approval_id: Optional[str] = None

@dataclass
class ApprovalRequest:
    request_id: str
    operation: AIOperation
    user_id: str
    user_email: str
    description: str
    risk_assessment: Dict[str, Any]
    required_approvers: List[GovernanceRole]
    approvals_received: List[Dict[str, Any]]
    status: ApprovalStatus
    created_date: datetime
    expiry_date: datetime
    metadata: Dict[str, Any]
    conditions: List[str] = None

@dataclass
class GovernancePolicy:
    policy_id: str
    name: str
    description: str
    operation_type: AIOperation
    risk_threshold: RiskLevel
    required_approvers: List[GovernanceRole]
    auto_approve_conditions: List[str]
    monitoring_requirements: List[str]
    compliance_checks: List[str]
    active: bool
    created_date: datetime
    updated_date: datetime

@dataclass
class ComplianceAlert:
    alert_id: str
    alert_type: str
    severity: RiskLevel
    description: str
    affected_operations: List[str]
    recommended_actions: List[str]
    created_date: datetime
    resolved: bool
    resolved_date: Optional[datetime] = None

class AIGovernanceAgent:
    def __init__(self):
        self.usage_logs: Dict[str, AIUsageLog] = {}
        self.approval_requests: Dict[str, ApprovalRequest] = {}
        self.governance_policies: Dict[str, GovernancePolicy] = {}
        self.compliance_alerts: Dict[str, ComplianceAlert] = {}
        self.user_permissions: Dict[str, List[AIOperation]] = {}
        self._initialize_default_policies()
    
    def _initialize_default_policies(self):
        """Initialize default governance policies"""
        
        # High-risk operations policy
        high_risk_policy = GovernancePolicy(
            policy_id="policy_high_risk_001",
            name="High-Risk AI Operations",
            description="Governance for high-risk AI operations requiring approval",
            operation_type=AIOperation.EMPLOYEE_EVALUATION,
            risk_threshold=RiskLevel.HIGH,
            required_approvers=[GovernanceRole.HR_ADMIN, GovernanceRole.COMPLIANCE_OFFICER],
            auto_approve_conditions=[],
            monitoring_requirements=["audit_trail", "human_review", "bias_check"],
            compliance_checks=["data_privacy", "fairness_assessment", "legal_review"],
            active=True,
            created_date=datetime.now(),
            updated_date=datetime.now()
        )
        
        # Document generation policy
        doc_gen_policy = GovernancePolicy(
            policy_id="policy_doc_gen_001",
            name="Document Generation Governance",
            description="Approval requirements for AI-generated legal documents",
            operation_type=AIOperation.DOCUMENT_GENERATION,
            risk_threshold=RiskLevel.MEDIUM,
            required_approvers=[GovernanceRole.HR_ADMIN],
            auto_approve_conditions=["template_approved", "standard_fields_only"],
            monitoring_requirements=["content_review", "legal_compliance"],
            compliance_checks=["template_validation", "field_completeness"],
            active=True,
            created_date=datetime.now(),
            updated_date=datetime.now()
        )
        
        # Query processing policy
        query_policy = GovernancePolicy(
            policy_id="policy_query_001",
            name="AI Query Processing",
            description="Governance for general AI query processing",
            operation_type=AIOperation.QUERY_PROCESSING,
            risk_threshold=RiskLevel.LOW,
            required_approvers=[],
            auto_approve_conditions=["standard_hr_query", "no_personal_data"],
            monitoring_requirements=["usage_tracking", "response_quality"],
            compliance_checks=["data_sensitivity", "output_appropriateness"],
            active=True,
            created_date=datetime.now(),
            updated_date=datetime.now()
        )
        
        self.governance_policies[high_risk_policy.policy_id] = high_risk_policy
        self.governance_policies[doc_gen_policy.policy_id] = doc_gen_policy
        self.governance_policies[query_policy.policy_id] = query_policy
    
    async def request_ai_operation_approval(self, operation: AIOperation, user_id: str, 
                                          user_email: str, description: str,
                                          metadata: Dict[str, Any] = None) -> Tuple[bool, str]:
        """Request approval for AI operation"""
        
        # Find applicable policy
        policy = self._get_applicable_policy(operation)
        if not policy:
            return True, "no_policy_required"  # No governance required
        
        # Assess risk
        risk_assessment = await self._assess_operation_risk(operation, metadata or {})
        
        # Check auto-approval conditions
        if await self._check_auto_approval(policy, risk_assessment, metadata or {}):
            # Log the auto-approved operation
            await self._log_auto_approval(operation, user_id, user_email, risk_assessment)
            return True, "auto_approved"
        
        # Create approval request
        request_id = str(uuid.uuid4())
        approval_request = ApprovalRequest(
            request_id=request_id,
            operation=operation,
            user_id=user_id,
            user_email=user_email,
            description=description,
            risk_assessment=risk_assessment,
            required_approvers=policy.required_approvers,
            approvals_received=[],
            status=ApprovalStatus.PENDING,
            created_date=datetime.now(),
            expiry_date=datetime.now() + timedelta(days=7),  # 7-day expiry
            metadata=metadata or {},
            conditions=[]
        )
        
        self.approval_requests[request_id] = approval_request
        
        # Send notifications to required approvers
        await self._notify_approvers(approval_request)
        
        return False, request_id
    
    def _get_applicable_policy(self, operation: AIOperation) -> Optional[GovernancePolicy]:
        """Get the applicable governance policy for an operation"""
        for policy in self.governance_policies.values():
            if policy.operation_type == operation and policy.active:
                return policy
        return None
    
    async def _assess_operation_risk(self, operation: AIOperation, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Assess risk level of AI operation"""
        risk_factors = {
            "data_sensitivity": self._assess_data_sensitivity(metadata),
            "output_impact": self._assess_output_impact(operation),
            "user_permissions": self._assess_user_permissions(metadata.get("user_id")),
            "compliance_requirements": self._assess_compliance_requirements(operation)
        }
        
        # Calculate overall risk level
        risk_score = sum([
            risk_factors["data_sensitivity"] * 0.3,
            risk_factors["output_impact"] * 0.4,
            risk_factors["user_permissions"] * 0.2,
            risk_factors["compliance_requirements"] * 0.1
        ])
        
        if risk_score >= 0.8:
            risk_level = RiskLevel.CRITICAL
        elif risk_score >= 0.6:
            risk_level = RiskLevel.HIGH
        elif risk_score >= 0.4:
            risk_level = RiskLevel.MEDIUM
        else:
            risk_level = RiskLevel.LOW
        
        return {
            "risk_level": risk_level,
            "risk_score": risk_score,
            "factors": risk_factors,
            "recommendations": self._get_risk_recommendations(risk_level)
        }
    
    def _assess_data_sensitivity(self, metadata: Dict[str, Any]) -> float:
        """Assess sensitivity of data involved"""
        sensitive_fields = ["ssn", "salary", "performance_rating", "disciplinary_action"]
        
        if any(field in str(metadata).lower() for field in sensitive_fields):
            return 1.0
        elif "employee_data" in metadata:
            return 0.7
        else:
            return 0.3
    
    def _assess_output_impact(self, operation: AIOperation) -> float:
        """Assess potential impact of operation output"""
        impact_levels = {
            AIOperation.EMPLOYEE_EVALUATION: 1.0,
            AIOperation.DOCUMENT_GENERATION: 0.8,
            AIOperation.POLICY_RECOMMENDATION: 0.7,
            AIOperation.WORKFLOW_AUTOMATION: 0.6,
            AIOperation.PREDICTIVE_ANALYSIS: 0.5,
            AIOperation.COMPLIANCE_CHECK: 0.4,
            AIOperation.DATA_ANALYSIS: 0.3,
            AIOperation.QUERY_PROCESSING: 0.2
        }
        return impact_levels.get(operation, 0.5)
    
    def _assess_user_permissions(self, user_id: str) -> float:
        """Assess user permission level"""
        if not user_id or user_id not in self.user_permissions:
            return 0.8  # High risk for unknown users
        
        user_ops = self.user_permissions[user_id]
        if len(user_ops) > 5:
            return 0.2  # Low risk for highly privileged users
        elif len(user_ops) > 2:
            return 0.5  # Medium risk
        else:
            return 0.7  # Higher risk for limited users
    
    def _assess_compliance_requirements(self, operation: AIOperation) -> float:
        """Assess compliance requirements"""
        high_compliance_ops = [
            AIOperation.EMPLOYEE_EVALUATION,
            AIOperation.DOCUMENT_GENERATION,
            AIOperation.POLICY_RECOMMENDATION
        ]
        
        return 1.0 if operation in high_compliance_ops else 0.3
    
    def _get_risk_recommendations(self, risk_level: RiskLevel) -> List[str]:
        """Get recommendations based on risk level"""
        recommendations = {
            RiskLevel.CRITICAL: [
                "Require C-level approval",
                "Conduct thorough audit",
                "Implement additional monitoring",
                "Consider manual alternative"
            ],
            RiskLevel.HIGH: [
                "Require manager approval",
                "Enable detailed logging",
                "Schedule review meeting",
                "Implement safeguards"
            ],
            RiskLevel.MEDIUM: [
                "Enable monitoring",
                "Document decision rationale",
                "Schedule periodic review"
            ],
            RiskLevel.LOW: [
                "Standard monitoring",
                "Regular usage review"
            ]
        }
        return recommendations.get(risk_level, [])
    
    async def _check_auto_approval(self, policy: GovernancePolicy, 
                                 risk_assessment: Dict[str, Any],
                                 metadata: Dict[str, Any]) -> bool:
        """Check if operation meets auto-approval conditions"""
        if not policy.auto_approve_conditions:
            return False
        
        # Check each auto-approval condition
        for condition in policy.auto_approve_conditions:
            if not await self._evaluate_condition(condition, risk_assessment, metadata):
                return False
        
        return True
    
    async def _evaluate_condition(self, condition: str, risk_assessment: Dict[str, Any],
                                metadata: Dict[str, Any]) -> bool:
        """Evaluate a specific auto-approval condition"""
        condition_evaluators = {
            "standard_hr_query": lambda: "employee_evaluation" not in str(metadata).lower(),
            "no_personal_data": lambda: risk_assessment["factors"]["data_sensitivity"] < 0.5,
            "template_approved": lambda: metadata.get("template_approved", False),
            "standard_fields_only": lambda: not metadata.get("custom_fields", []),
            "low_risk_only": lambda: risk_assessment["risk_level"] == RiskLevel.LOW
        }
        
        evaluator = condition_evaluators.get(condition)
        return evaluator() if evaluator else False
    
    async def _log_auto_approval(self, operation: AIOperation, user_id: str, 
                               user_email: str, risk_assessment: Dict[str, Any]):
        """Log auto-approved operation"""
        log_id = str(uuid.uuid4())
        usage_log = AIUsageLog(
            log_id=log_id,
            user_id=user_id,
            user_email=user_email,
            operation=operation,
            ai_provider="auto_approved",
            model_used="governance_agent",
            input_data_hash="auto_approved",
            output_data_hash="auto_approved",
            confidence_score=1.0,
            tokens_used=0,
            cost=0.0,
            processing_time=0.0,
            timestamp=datetime.now(),
            risk_level=risk_assessment["risk_level"],
            compliance_flags=[],
            approved=True,
            approval_id="auto_approved"
        )
        
        self.usage_logs[log_id] = usage_log
    
    async def _notify_approvers(self, approval_request: ApprovalRequest):
        """Send notifications to required approvers"""
        # This would integrate with your notification system
        print(f"Notifying approvers for request {approval_request.request_id}")
        # Implementation would send emails/notifications to approvers
    
    async def process_approval(self, request_id: str, approver_role: GovernanceRole,
                             approver_email: str, decision: ApprovalStatus,
                             comments: str = "", conditions: List[str] = None) -> bool:
        """Process an approval decision"""
        
        if request_id not in self.approval_requests:
            return False
        
        approval_request = self.approval_requests[request_id]
        
        # Check if approver is authorized
        if approver_role not in approval_request.required_approvers:
            return False
        
        # Check if already approved by this role
        existing_approval = next(
            (a for a in approval_request.approvals_received if a["role"] == approver_role),
            None
        )
        if existing_approval:
            return False  # Already approved by this role
        
        # Add approval
        approval_request.approvals_received.append({
            "role": approver_role,
            "approver_email": approver_email,
            "decision": decision,
            "comments": comments,
            "timestamp": datetime.now().isoformat(),
            "conditions": conditions or []
        })
        
        # Update conditions
        if conditions:
            approval_request.conditions.extend(conditions)
        
        # Check if all required approvals received
        approved_roles = [a["role"] for a in approval_request.approvals_received 
                         if a["decision"] == ApprovalStatus.APPROVED]
        
        if decision == ApprovalStatus.REJECTED:
            approval_request.status = ApprovalStatus.REJECTED
        elif set(approved_roles) >= set(approval_request.required_approvers):
            approval_request.status = ApprovalStatus.APPROVED if not approval_request.conditions else ApprovalStatus.CONDITIONAL
        
        return True
    
    async def log_ai_usage(self, user_id: str, user_email: str, operation: AIOperation,
                         ai_provider: str, model_used: str, input_data: str,
                         output_data: str, confidence_score: float, tokens_used: int,
                         cost: float, processing_time: float) -> str:
        """Log AI usage for monitoring and compliance"""
        
        log_id = str(uuid.uuid4())
        
        # Hash sensitive data
        input_hash = hashlib.sha256(input_data.encode()).hexdigest()
        output_hash = hashlib.sha256(output_data.encode()).hexdigest()
        
        # Assess compliance flags
        compliance_flags = await self._check_compliance_flags(operation, input_data, output_data)
        
        # Determine risk level
        risk_assessment = await self._assess_operation_risk(operation, {
            "user_id": user_id,
            "input_data": input_data,
            "output_data": output_data
        })
        
        usage_log = AIUsageLog(
            log_id=log_id,
            user_id=user_id,
            user_email=user_email,
            operation=operation,
            ai_provider=ai_provider,
            model_used=model_used,
            input_data_hash=input_hash,
            output_data_hash=output_hash,
            confidence_score=confidence_score,
            tokens_used=tokens_used,
            cost=cost,
            processing_time=processing_time,
            timestamp=datetime.now(),
            risk_level=risk_assessment["risk_level"],
            compliance_flags=compliance_flags,
            approved=True  # Assume approved if logging after execution
        )
        
        self.usage_logs[log_id] = usage_log
        
        # Check for compliance alerts
        await self._check_compliance_alerts(usage_log)
        
        return log_id
    
    async def _check_compliance_flags(self, operation: AIOperation, 
                                    input_data: str, output_data: str) -> List[str]:
        """Check for compliance flags in AI usage"""
        flags = []
        
        # Check for sensitive data
        sensitive_patterns = ["ssn", "social security", "credit card", "password"]
        if any(pattern in input_data.lower() or pattern in output_data.lower() 
               for pattern in sensitive_patterns):
            flags.append("sensitive_data_detected")
        
        # Check for bias indicators
        bias_patterns = ["discriminatory", "biased", "unfair"]
        if any(pattern in output_data.lower() for pattern in bias_patterns):
            flags.append("potential_bias")
        
        # Check for legal concerns
        legal_patterns = ["illegal", "violation", "lawsuit"]
        if any(pattern in output_data.lower() for pattern in legal_patterns):
            flags.append("legal_concern")
        
        return flags
    
    async def _check_compliance_alerts(self, usage_log: AIUsageLog):
        """Check if usage log triggers compliance alerts"""
        
        # High-risk operation alert
        if usage_log.risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]:
            await self._create_compliance_alert(
                "high_risk_operation",
                usage_log.risk_level,
                f"High-risk AI operation detected: {usage_log.operation.value}",
                [usage_log.log_id],
                ["Review operation", "Assess impact", "Consider additional controls"]
            )
        
        # Compliance flag alert
        if usage_log.compliance_flags:
            await self._create_compliance_alert(
                "compliance_violation",
                RiskLevel.MEDIUM,
                f"Compliance flags detected: {', '.join(usage_log.compliance_flags)}",
                [usage_log.log_id],
                ["Review flagged content", "Assess compliance impact", "Update policies if needed"]
            )
    
    async def _create_compliance_alert(self, alert_type: str, severity: RiskLevel,
                                     description: str, affected_operations: List[str],
                                     recommended_actions: List[str]):
        """Create a compliance alert"""
        alert_id = str(uuid.uuid4())
        alert = ComplianceAlert(
            alert_id=alert_id,
            alert_type=alert_type,
            severity=severity,
            description=description,
            affected_operations=affected_operations,
            recommended_actions=recommended_actions,
            created_date=datetime.now(),
            resolved=False
        )
        
        self.compliance_alerts[alert_id] = alert
    
    def get_usage_analytics(self, start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        """Get AI usage analytics for governance reporting"""
        
        relevant_logs = [
            log for log in self.usage_logs.values()
            if start_date <= log.timestamp <= end_date
        ]
        
        if not relevant_logs:
            return {"message": "No usage data for specified period"}
        
        # Calculate metrics
        total_operations = len(relevant_logs)
        total_cost = sum(log.cost for log in relevant_logs)
        total_tokens = sum(log.tokens_used for log in relevant_logs)
        avg_confidence = sum(log.confidence_score for log in relevant_logs) / total_operations
        
        # Operation breakdown
        operation_counts = {}
        for log in relevant_logs:
            op = log.operation.value
            operation_counts[op] = operation_counts.get(op, 0) + 1
        
        # Risk level breakdown
        risk_counts = {}
        for log in relevant_logs:
            risk = log.risk_level.value
            risk_counts[risk] = risk_counts.get(risk, 0) + 1
        
        # Provider breakdown
        provider_counts = {}
        for log in relevant_logs:
            provider = log.ai_provider
            provider_counts[provider] = provider_counts.get(provider, 0) + 1
        
        # Compliance issues
        compliance_issues = sum(len(log.compliance_flags) for log in relevant_logs)
        
        return {
            "period": {
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat()
            },
            "summary": {
                "total_operations": total_operations,
                "total_cost": round(total_cost, 2),
                "total_tokens": total_tokens,
                "average_confidence": round(avg_confidence, 2),
                "compliance_issues": compliance_issues
            },
            "breakdowns": {
                "by_operation": operation_counts,
                "by_risk_level": risk_counts,
                "by_provider": provider_counts
            },
            "compliance": {
                "total_flags": compliance_issues,
                "high_risk_operations": risk_counts.get("high", 0) + risk_counts.get("critical", 0)
            }
        }
    
    def get_pending_approvals(self, approver_role: GovernanceRole) -> List[Dict[str, Any]]:
        """Get pending approval requests for a specific role"""
        pending = []
        
        for request in self.approval_requests.values():
            if (request.status == ApprovalStatus.PENDING and 
                approver_role in request.required_approvers and
                not any(a["role"] == approver_role for a in request.approvals_received)):
                
                pending.append({
                    "request_id": request.request_id,
                    "operation": request.operation.value,
                    "user_email": request.user_email,
                    "description": request.description,
                    "risk_level": request.risk_assessment["risk_level"].value,
                    "created_date": request.created_date.isoformat(),
                    "expiry_date": request.expiry_date.isoformat(),
                    "required_approvers": [role.value for role in request.required_approvers],
                    "approvals_received": len(request.approvals_received)
                })
        
        return pending
    
    def get_compliance_alerts(self, resolved: Optional[bool] = None) -> List[Dict[str, Any]]:
        """Get compliance alerts"""
        alerts = []
        
        for alert in self.compliance_alerts.values():
            if resolved is None or alert.resolved == resolved:
                alerts.append({
                    "alert_id": alert.alert_id,
                    "alert_type": alert.alert_type,
                    "severity": alert.severity.value,
                    "description": alert.description,
                    "affected_operations": alert.affected_operations,
                    "recommended_actions": alert.recommended_actions,
                    "created_date": alert.created_date.isoformat(),
                    "resolved": alert.resolved,
                    "resolved_date": alert.resolved_date.isoformat() if alert.resolved_date else None
                })
        
        return alerts

# Global instance
governance_agent = AIGovernanceAgent()

