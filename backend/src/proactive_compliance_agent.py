"""
Proactive Compliance Agent for HR Advisor
Monitors compliance requirements, sends alerts, tracks policy changes, and ensures regulatory adherence
"""

import asyncio
import json
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import requests
from bs4 import BeautifulSoup
import re

class ComplianceArea(Enum):
    EMPLOYMENT_LAW = "employment_law"
    DATA_PRIVACY = "data_privacy"
    WORKPLACE_SAFETY = "workplace_safety"
    EQUAL_OPPORTUNITY = "equal_opportunity"
    WAGE_HOUR = "wage_hour"
    BENEFITS = "benefits"
    IMMIGRATION = "immigration"
    LABOR_RELATIONS = "labor_relations"
    TERMINATION = "termination"
    HARASSMENT = "harassment"

class AlertSeverity(Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"
    URGENT = "urgent"

class ComplianceStatus(Enum):
    COMPLIANT = "compliant"
    AT_RISK = "at_risk"
    NON_COMPLIANT = "non_compliant"
    UNKNOWN = "unknown"

@dataclass
class ComplianceRule:
    rule_id: str
    name: str
    description: str
    area: ComplianceArea
    country: str
    jurisdiction: str
    effective_date: datetime
    expiry_date: Optional[datetime]
    requirements: List[str]
    penalties: List[str]
    monitoring_frequency: str  # daily, weekly, monthly
    source_url: str
    last_updated: datetime
    active: bool

@dataclass
class ComplianceAlert:
    alert_id: str
    rule_id: str
    employee_id: Optional[str]
    department: Optional[str]
    severity: AlertSeverity
    title: str
    description: str
    recommended_actions: List[str]
    deadline: Optional[datetime]
    created_date: datetime
    acknowledged: bool
    resolved: bool
    resolved_date: Optional[datetime]
    metadata: Dict[str, Any]

@dataclass
class ComplianceAssessment:
    assessment_id: str
    employee_id: Optional[str]
    department: Optional[str]
    area: ComplianceArea
    status: ComplianceStatus
    score: float  # 0-100
    issues_found: List[str]
    recommendations: List[str]
    next_review_date: datetime
    assessed_date: datetime
    assessor: str

@dataclass
class PolicyUpdate:
    update_id: str
    area: ComplianceArea
    country: str
    title: str
    summary: str
    effective_date: datetime
    impact_level: AlertSeverity
    affected_rules: List[str]
    required_actions: List[str]
    source: str
    detected_date: datetime

class ProactiveComplianceAgent:
    def __init__(self):
        self.compliance_rules: Dict[str, ComplianceRule] = {}
        self.alerts: Dict[str, ComplianceAlert] = {}
        self.assessments: Dict[str, ComplianceAssessment] = {}
        self.policy_updates: Dict[str, PolicyUpdate] = {}
        self.monitoring_schedule: Dict[str, datetime] = {}
        self._initialize_compliance_rules()
    
    def _initialize_compliance_rules(self):
        """Initialize compliance rules for different jurisdictions"""
        
        # US Federal Rules
        flsa_rule = ComplianceRule(
            rule_id="us_flsa_001",
            name="Fair Labor Standards Act - Overtime",
            description="Employees must receive overtime pay for hours worked over 40 in a workweek",
            area=ComplianceArea.WAGE_HOUR,
            country="US",
            jurisdiction="Federal",
            effective_date=datetime(1938, 6, 25),
            expiry_date=None,
            requirements=[
                "Track all employee working hours",
                "Pay overtime at 1.5x regular rate for hours over 40/week",
                "Maintain accurate payroll records",
                "Classify employees correctly (exempt vs non-exempt)"
            ],
            penalties=[
                "Back wages owed to employees",
                "Liquidated damages equal to back wages",
                "Civil penalties up to $2,074 per violation",
                "Criminal prosecution for willful violations"
            ],
            monitoring_frequency="weekly",
            source_url="https://www.dol.gov/agencies/whd/flsa",
            last_updated=datetime.now(),
            active=True
        )
        
        # Singapore Employment Act
        sg_employment_rule = ComplianceRule(
            rule_id="sg_ea_001",
            name="Singapore Employment Act - Working Hours",
            description="Maximum working hours and overtime regulations",
            area=ComplianceArea.WAGE_HOUR,
            country="SG",
            jurisdiction="National",
            effective_date=datetime(1968, 12, 1),
            expiry_date=None,
            requirements=[
                "Maximum 44 hours per week for non-shift workers",
                "Maximum 12 hours per day including overtime",
                "Overtime pay at 1.5x for first 2 hours, 2x thereafter",
                "Minimum 1 rest day per week"
            ],
            penalties=[
                "Fine up to S$5,000",
                "Imprisonment up to 6 months",
                "Compensation to affected employees"
            ],
            monitoring_frequency="weekly",
            source_url="https://www.mom.gov.sg/employment-practices/hours-of-work-overtime-and-rest-days",
            last_updated=datetime.now(),
            active=True
        )
        
        # GDPR Data Privacy
        gdpr_rule = ComplianceRule(
            rule_id="eu_gdpr_001",
            name="GDPR - Employee Data Protection",
            description="Protection of employee personal data under GDPR",
            area=ComplianceArea.DATA_PRIVACY,
            country="EU",
            jurisdiction="European Union",
            effective_date=datetime(2018, 5, 25),
            expiry_date=None,
            requirements=[
                "Obtain explicit consent for data processing",
                "Implement data protection by design",
                "Conduct Data Protection Impact Assessments",
                "Appoint Data Protection Officer if required",
                "Report breaches within 72 hours"
            ],
            penalties=[
                "Fines up to €20 million or 4% of annual turnover",
                "Administrative sanctions",
                "Compensation to affected individuals"
            ],
            monitoring_frequency="monthly",
            source_url="https://gdpr-info.eu/",
            last_updated=datetime.now(),
            active=True
        )
        
        # UK Employment Rights
        uk_employment_rule = ComplianceRule(
            rule_id="uk_era_001",
            name="Employment Rights Act - Unfair Dismissal",
            description="Protection against unfair dismissal",
            area=ComplianceArea.TERMINATION,
            country="UK",
            jurisdiction="National",
            effective_date=datetime(1996, 5, 22),
            expiry_date=None,
            requirements=[
                "Follow fair dismissal procedures",
                "Provide written reasons for dismissal",
                "Allow right to be accompanied at hearings",
                "Consider alternatives to dismissal",
                "Provide appropriate notice periods"
            ],
            penalties=[
                "Basic award up to £17,130",
                "Compensatory award up to £93,878",
                "Additional award for non-compliance",
                "Reinstatement or re-engagement orders"
            ],
            monitoring_frequency="monthly",
            source_url="https://www.gov.uk/dismiss-staff",
            last_updated=datetime.now(),
            active=True
        )
        
        # Store rules
        self.compliance_rules[flsa_rule.rule_id] = flsa_rule
        self.compliance_rules[sg_employment_rule.rule_id] = sg_employment_rule
        self.compliance_rules[gdpr_rule.rule_id] = gdpr_rule
        self.compliance_rules[uk_employment_rule.rule_id] = uk_employment_rule
    
    async def monitor_compliance(self, employee_data: List[Dict[str, Any]]) -> List[str]:
        """Monitor compliance across all employees and generate alerts"""
        alert_ids = []
        
        for employee in employee_data:
            # Check each compliance area
            for rule in self.compliance_rules.values():
                if not rule.active:
                    continue
                
                # Check if rule applies to employee's country
                if rule.country != employee.get('country', 'US'):
                    continue
                
                # Perform compliance check based on rule area
                compliance_issues = await self._check_rule_compliance(rule, employee)
                
                # Generate alerts for issues found
                for issue in compliance_issues:
                    alert_id = await self._create_compliance_alert(
                        rule, employee, issue
                    )
                    alert_ids.append(alert_id)
        
        return alert_ids
    
    async def _check_rule_compliance(self, rule: ComplianceRule, 
                                   employee: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Check compliance for a specific rule and employee"""
        issues = []
        
        if rule.area == ComplianceArea.WAGE_HOUR:
            issues.extend(await self._check_wage_hour_compliance(rule, employee))
        elif rule.area == ComplianceArea.DATA_PRIVACY:
            issues.extend(await self._check_data_privacy_compliance(rule, employee))
        elif rule.area == ComplianceArea.EQUAL_OPPORTUNITY:
            issues.extend(await self._check_equal_opportunity_compliance(rule, employee))
        elif rule.area == ComplianceArea.WORKPLACE_SAFETY:
            issues.extend(await self._check_safety_compliance(rule, employee))
        elif rule.area == ComplianceArea.TERMINATION:
            issues.extend(await self._check_termination_compliance(rule, employee))
        
        return issues
    
    async def _check_wage_hour_compliance(self, rule: ComplianceRule, 
                                        employee: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Check wage and hour compliance"""
        issues = []
        
        # Check working hours
        weekly_hours = employee.get('weekly_hours', 40)
        if rule.country == "US" and weekly_hours > 40:
            overtime_hours = weekly_hours - 40
            if not employee.get('overtime_eligible', True):
                issues.append({
                    "type": "overtime_classification",
                    "severity": AlertSeverity.CRITICAL,
                    "description": f"Employee working {weekly_hours} hours/week but not eligible for overtime",
                    "recommendation": "Review employee classification and ensure overtime eligibility"
                })
        
        elif rule.country == "SG" and weekly_hours > 44:
            issues.append({
                "type": "excessive_hours",
                "severity": AlertSeverity.WARNING,
                "description": f"Employee working {weekly_hours} hours/week exceeds Singapore limit of 44",
                "recommendation": "Reduce working hours or ensure proper overtime compensation"
            })
        
        # Check minimum wage compliance
        hourly_rate = employee.get('hourly_rate', 0)
        if rule.country == "US" and hourly_rate < 7.25:  # Federal minimum wage
            issues.append({
                "type": "minimum_wage",
                "severity": AlertSeverity.CRITICAL,
                "description": f"Employee hourly rate ${hourly_rate} below federal minimum wage",
                "recommendation": "Increase hourly rate to meet minimum wage requirements"
            })
        
        return issues
    
    async def _check_data_privacy_compliance(self, rule: ComplianceRule, 
                                           employee: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Check data privacy compliance"""
        issues = []
        
        # Check consent for data processing
        if not employee.get('data_processing_consent', False):
            issues.append({
                "type": "missing_consent",
                "severity": AlertSeverity.CRITICAL,
                "description": "No explicit consent recorded for employee data processing",
                "recommendation": "Obtain and document explicit consent for data processing"
            })
        
        # Check data retention
        hire_date = employee.get('hire_date')
        if hire_date:
            hire_datetime = datetime.fromisoformat(hire_date) if isinstance(hire_date, str) else hire_date
            years_employed = (datetime.now() - hire_datetime).days / 365
            
            if years_employed > 7 and not employee.get('data_retention_reviewed', False):
                issues.append({
                    "type": "data_retention",
                    "severity": AlertSeverity.WARNING,
                    "description": "Employee data retention period may exceed legal requirements",
                    "recommendation": "Review data retention policy and purge unnecessary data"
                })
        
        return issues
    
    async def _check_equal_opportunity_compliance(self, rule: ComplianceRule, 
                                                employee: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Check equal opportunity compliance"""
        issues = []
        
        # This would involve statistical analysis across employee population
        # For now, we'll check for basic indicators
        
        return issues
    
    async def _check_safety_compliance(self, rule: ComplianceRule, 
                                     employee: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Check workplace safety compliance"""
        issues = []
        
        # Check safety training
        last_safety_training = employee.get('last_safety_training')
        if not last_safety_training:
            issues.append({
                "type": "missing_safety_training",
                "severity": AlertSeverity.WARNING,
                "description": "No safety training recorded for employee",
                "recommendation": "Schedule mandatory safety training"
            })
        elif isinstance(last_safety_training, str):
            training_date = datetime.fromisoformat(last_safety_training)
            if (datetime.now() - training_date).days > 365:
                issues.append({
                    "type": "expired_safety_training",
                    "severity": AlertSeverity.WARNING,
                    "description": "Safety training expired over 1 year ago",
                    "recommendation": "Schedule refresher safety training"
                })
        
        return issues
    
    async def _check_termination_compliance(self, rule: ComplianceRule, 
                                          employee: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Check termination compliance"""
        issues = []
        
        # Check if employee is marked for termination
        if employee.get('status') == 'terminated':
            termination_date = employee.get('termination_date')
            termination_reason = employee.get('termination_reason')
            
            if not termination_reason:
                issues.append({
                    "type": "missing_termination_reason",
                    "severity": AlertSeverity.CRITICAL,
                    "description": "Terminated employee missing documented reason",
                    "recommendation": "Document termination reason for legal compliance"
                })
            
            # Check notice period
            notice_given = employee.get('notice_period_given', 0)
            required_notice = self._get_required_notice_period(rule.country, employee)
            
            if notice_given < required_notice:
                issues.append({
                    "type": "insufficient_notice",
                    "severity": AlertSeverity.CRITICAL,
                    "description": f"Notice period {notice_given} days less than required {required_notice} days",
                    "recommendation": "Provide payment in lieu of notice or extend notice period"
                })
        
        return issues
    
    def _get_required_notice_period(self, country: str, employee: Dict[str, Any]) -> int:
        """Get required notice period based on country and tenure"""
        tenure_years = employee.get('tenure_years', 0)
        
        notice_periods = {
            "US": 0,  # At-will employment, no notice required
            "UK": min(12, max(1, tenure_years)) * 7,  # 1-12 weeks based on tenure
            "SG": min(4, max(1, tenure_years)) * 7,   # 1-4 weeks based on tenure
            "AU": min(5, max(1, tenure_years)) * 7,   # 1-5 weeks based on tenure
        }
        
        return notice_periods.get(country, 14)  # Default 2 weeks
    
    async def _create_compliance_alert(self, rule: ComplianceRule, 
                                     employee: Dict[str, Any], 
                                     issue: Dict[str, Any]) -> str:
        """Create a compliance alert"""
        alert_id = str(uuid.uuid4())
        
        # Calculate deadline based on severity
        deadline = None
        if issue["severity"] == AlertSeverity.CRITICAL:
            deadline = datetime.now() + timedelta(days=7)
        elif issue["severity"] == AlertSeverity.WARNING:
            deadline = datetime.now() + timedelta(days=30)
        
        alert = ComplianceAlert(
            alert_id=alert_id,
            rule_id=rule.rule_id,
            employee_id=employee.get('employee_id'),
            department=employee.get('department'),
            severity=issue["severity"],
            title=f"{rule.name} - {issue['type'].replace('_', ' ').title()}",
            description=issue["description"],
            recommended_actions=[issue["recommendation"]],
            deadline=deadline,
            created_date=datetime.now(),
            acknowledged=False,
            resolved=False,
            resolved_date=None,
            metadata={
                "rule_area": rule.area.value,
                "country": rule.country,
                "employee_name": employee.get('name', 'Unknown'),
                "issue_type": issue["type"]
            }
        )
        
        self.alerts[alert_id] = alert
        return alert_id
    
    async def scan_policy_updates(self, countries: List[str]) -> List[str]:
        """Scan for policy updates from government sources"""
        update_ids = []
        
        for country in countries:
            try:
                updates = await self._scan_country_updates(country)
                for update in updates:
                    update_id = await self._create_policy_update(update)
                    update_ids.append(update_id)
            except Exception as e:
                print(f"Error scanning updates for {country}: {e}")
                continue
        
        return update_ids
    
    async def _scan_country_updates(self, country: str) -> List[Dict[str, Any]]:
        """Scan for policy updates from a specific country"""
        updates = []
        
        # Define government sources for each country
        sources = {
            "US": [
                "https://www.dol.gov/newsroom/releases",
                "https://www.eeoc.gov/newsroom/releases"
            ],
            "UK": [
                "https://www.gov.uk/government/news",
                "https://www.acas.org.uk/news"
            ],
            "SG": [
                "https://www.mom.gov.sg/newsroom",
                "https://www.cpf.gov.sg/member/news-and-announcement"
            ],
            "AU": [
                "https://www.fairwork.gov.au/about-us/news-and-media-releases"
            ]
        }
        
        country_sources = sources.get(country, [])
        
        for source_url in country_sources:
            try:
                # This is a simplified example - real implementation would need
                # proper web scraping with respect for robots.txt and rate limits
                updates.extend(await self._scrape_policy_updates(source_url, country))
            except Exception as e:
                print(f"Error scraping {source_url}: {e}")
                continue
        
        return updates
    
    async def _scrape_policy_updates(self, url: str, country: str) -> List[Dict[str, Any]]:
        """Scrape policy updates from a government website"""
        # This is a placeholder - real implementation would need proper web scraping
        # For demo purposes, we'll return mock updates
        
        mock_updates = [
            {
                "title": "Updated Minimum Wage Requirements",
                "summary": "New minimum wage rates effective January 2025",
                "area": ComplianceArea.WAGE_HOUR,
                "effective_date": datetime(2025, 1, 1),
                "impact_level": AlertSeverity.CRITICAL,
                "source": url
            },
            {
                "title": "Enhanced Data Protection Guidelines",
                "summary": "New guidelines for employee data protection",
                "area": ComplianceArea.DATA_PRIVACY,
                "effective_date": datetime(2025, 3, 1),
                "impact_level": AlertSeverity.WARNING,
                "source": url
            }
        ]
        
        return mock_updates
    
    async def _create_policy_update(self, update_data: Dict[str, Any]) -> str:
        """Create a policy update record"""
        update_id = str(uuid.uuid4())
        
        # Determine affected rules
        affected_rules = []
        for rule in self.compliance_rules.values():
            if rule.area == update_data["area"] and rule.active:
                affected_rules.append(rule.rule_id)
        
        # Generate required actions
        required_actions = [
            "Review current policies",
            "Update employee handbook",
            "Train HR staff on changes",
            "Communicate changes to employees"
        ]
        
        if update_data["impact_level"] == AlertSeverity.CRITICAL:
            required_actions.insert(0, "Immediate compliance review required")
        
        policy_update = PolicyUpdate(
            update_id=update_id,
            area=update_data["area"],
            country=update_data.get("country", "Unknown"),
            title=update_data["title"],
            summary=update_data["summary"],
            effective_date=update_data["effective_date"],
            impact_level=update_data["impact_level"],
            affected_rules=affected_rules,
            required_actions=required_actions,
            source=update_data["source"],
            detected_date=datetime.now()
        )
        
        self.policy_updates[update_id] = policy_update
        return update_id
    
    async def assess_department_compliance(self, department: str, 
                                         employee_data: List[Dict[str, Any]]) -> str:
        """Assess compliance for a specific department"""
        assessment_id = str(uuid.uuid4())
        
        dept_employees = [emp for emp in employee_data if emp.get('department') == department]
        
        if not dept_employees:
            return assessment_id
        
        # Assess each compliance area
        area_scores = {}
        all_issues = []
        all_recommendations = []
        
        for area in ComplianceArea:
            area_issues = []
            
            # Check relevant rules for this area
            area_rules = [rule for rule in self.compliance_rules.values() 
                         if rule.area == area and rule.active]
            
            for rule in area_rules:
                for employee in dept_employees:
                    if rule.country == employee.get('country', 'US'):
                        issues = await self._check_rule_compliance(rule, employee)
                        area_issues.extend(issues)
            
            # Calculate area score (100 - percentage of employees with issues)
            if area_rules:  # Only assess areas with applicable rules
                employees_with_issues = len(set(
                    emp['employee_id'] for emp in dept_employees 
                    for issue in area_issues 
                    if any(rule.country == emp.get('country', 'US') for rule in area_rules)
                ))
                area_score = max(0, 100 - (employees_with_issues / len(dept_employees) * 100))
                area_scores[area.value] = area_score
                
                # Collect issues and recommendations
                area_issue_types = list(set(issue['type'] for issue in area_issues))
                all_issues.extend(area_issue_types)
                
                area_recommendations = list(set(issue['recommendation'] for issue in area_issues))
                all_recommendations.extend(area_recommendations)
        
        # Calculate overall score
        overall_score = sum(area_scores.values()) / len(area_scores) if area_scores else 100
        
        # Determine status
        if overall_score >= 90:
            status = ComplianceStatus.COMPLIANT
        elif overall_score >= 70:
            status = ComplianceStatus.AT_RISK
        else:
            status = ComplianceStatus.NON_COMPLIANT
        
        assessment = ComplianceAssessment(
            assessment_id=assessment_id,
            employee_id=None,
            department=department,
            area=ComplianceArea.EMPLOYMENT_LAW,  # Overall assessment
            status=status,
            score=overall_score,
            issues_found=list(set(all_issues)),
            recommendations=list(set(all_recommendations)),
            next_review_date=datetime.now() + timedelta(days=90),
            assessed_date=datetime.now(),
            assessor="Proactive Compliance Agent"
        )
        
        self.assessments[assessment_id] = assessment
        return assessment_id
    
    def get_compliance_dashboard(self) -> Dict[str, Any]:
        """Get compliance dashboard data"""
        
        # Alert summary
        alert_counts = {}
        for severity in AlertSeverity:
            alert_counts[severity.value] = len([
                alert for alert in self.alerts.values() 
                if alert.severity == severity and not alert.resolved
            ])
        
        # Recent policy updates
        recent_updates = sorted(
            self.policy_updates.values(),
            key=lambda x: x.detected_date,
            reverse=True
        )[:5]
        
        # Compliance areas at risk
        at_risk_areas = []
        for assessment in self.assessments.values():
            if assessment.status == ComplianceStatus.AT_RISK:
                at_risk_areas.append({
                    "department": assessment.department,
                    "area": assessment.area.value,
                    "score": assessment.score
                })
        
        return {
            "summary": {
                "total_alerts": len([a for a in self.alerts.values() if not a.resolved]),
                "critical_alerts": alert_counts.get("critical", 0),
                "pending_updates": len([u for u in self.policy_updates.values()]),
                "compliance_score": self._calculate_overall_compliance_score()
            },
            "alerts_by_severity": alert_counts,
            "recent_policy_updates": [
                {
                    "title": update.title,
                    "area": update.area.value,
                    "effective_date": update.effective_date.isoformat(),
                    "impact_level": update.impact_level.value
                }
                for update in recent_updates
            ],
            "at_risk_areas": at_risk_areas
        }
    
    def _calculate_overall_compliance_score(self) -> float:
        """Calculate overall compliance score"""
        if not self.assessments:
            return 100.0
        
        scores = [assessment.score for assessment in self.assessments.values()]
        return sum(scores) / len(scores)
    
    def get_alerts(self, severity: Optional[AlertSeverity] = None, 
                  resolved: Optional[bool] = None) -> List[Dict[str, Any]]:
        """Get compliance alerts"""
        alerts = []
        
        for alert in self.alerts.values():
            if severity and alert.severity != severity:
                continue
            if resolved is not None and alert.resolved != resolved:
                continue
            
            alerts.append({
                "alert_id": alert.alert_id,
                "title": alert.title,
                "description": alert.description,
                "severity": alert.severity.value,
                "employee_id": alert.employee_id,
                "department": alert.department,
                "deadline": alert.deadline.isoformat() if alert.deadline else None,
                "created_date": alert.created_date.isoformat(),
                "acknowledged": alert.acknowledged,
                "resolved": alert.resolved,
                "recommended_actions": alert.recommended_actions
            })
        
        return sorted(alerts, key=lambda x: x["created_date"], reverse=True)
    
    async def acknowledge_alert(self, alert_id: str, user_id: str) -> bool:
        """Acknowledge a compliance alert"""
        if alert_id not in self.alerts:
            return False
        
        self.alerts[alert_id].acknowledged = True
        return True
    
    async def resolve_alert(self, alert_id: str, user_id: str, 
                          resolution_notes: str = "") -> bool:
        """Resolve a compliance alert"""
        if alert_id not in self.alerts:
            return False
        
        alert = self.alerts[alert_id]
        alert.resolved = True
        alert.resolved_date = datetime.now()
        alert.metadata["resolution_notes"] = resolution_notes
        alert.metadata["resolved_by"] = user_id
        
        return True

# Global instance
compliance_agent = ProactiveComplianceAgent()

