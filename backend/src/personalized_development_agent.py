"""
Personalized Development Plans Agent for AnNi AI

Implements G-P requirements for personalized professional development:
- AI-driven learning recommendations
- Skill gap analysis
- Career path planning
- Training program suggestions
- Performance improvement plans

G-P Insight: "Create personalized professional development plans"
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
import numpy as np

class SkillLevel(Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"

class DevelopmentGoal(Enum):
    SKILL_IMPROVEMENT = "skill_improvement"
    CAREER_ADVANCEMENT = "career_advancement"
    LEADERSHIP_DEVELOPMENT = "leadership_development"
    TECHNICAL_EXPERTISE = "technical_expertise"
    SOFT_SKILLS = "soft_skills"
    COMPLIANCE_TRAINING = "compliance_training"

class LearningStyle(Enum):
    VISUAL = "visual"
    AUDITORY = "auditory"
    KINESTHETIC = "kinesthetic"
    READING_WRITING = "reading_writing"

class TrainingType(Enum):
    ONLINE_COURSE = "online_course"
    WORKSHOP = "workshop"
    MENTORING = "mentoring"
    ON_THE_JOB = "on_the_job"
    CERTIFICATION = "certification"
    CONFERENCE = "conference"
    BOOK_STUDY = "book_study"

@dataclass
class SkillAssessment:
    skill_id: str
    skill_name: str
    current_level: SkillLevel
    target_level: SkillLevel
    importance: int  # 1-10 scale
    last_assessed: datetime
    assessor: str
    evidence: List[str]

@dataclass
class DevelopmentPlan:
    plan_id: str
    employee_id: str
    created_by: str
    goals: List[DevelopmentGoal]
    skill_gaps: List[SkillAssessment]
    recommended_actions: List[Dict[str, Any]]
    timeline: Dict[str, Any]
    budget_estimate: float
    success_metrics: List[str]
    created_at: datetime
    updated_at: datetime
    status: str

@dataclass
class LearningRecommendation:
    recommendation_id: str
    employee_id: str
    skill_target: str
    training_type: TrainingType
    provider: str
    title: str
    description: str
    duration: str
    cost: float
    relevance_score: float
    difficulty_level: SkillLevel
    prerequisites: List[str]
    learning_outcomes: List[str]

class PersonalizedDevelopmentAgent:
    """
    Handles personalized professional development planning and recommendations.
    
    Key capabilities:
    - Skill gap analysis using AI
    - Personalized learning path generation
    - Career progression planning
    - Training recommendation engine
    - Progress tracking and analytics
    """
    
    def __init__(self, project_root: str = "/home/ubuntu/hr_advisor_app"):
        self.project_root = Path(project_root)
        self.db_path = self.project_root / "backend" / "hr_advisor.db"
        
        # Skill taxonomy and career paths
        self.skill_taxonomy = {
            'technical': {
                'programming': ['Python', 'JavaScript', 'Java', 'C++', 'SQL'],
                'data_analysis': ['Excel', 'Tableau', 'Power BI', 'R', 'Python'],
                'cloud_computing': ['AWS', 'Azure', 'Google Cloud', 'Docker', 'Kubernetes'],
                'cybersecurity': ['Network Security', 'Ethical Hacking', 'Compliance', 'Risk Assessment'],
                'project_management': ['Agile', 'Scrum', 'PMP', 'Risk Management', 'Budgeting']
            },
            'soft_skills': {
                'leadership': ['Team Management', 'Strategic Thinking', 'Decision Making', 'Delegation'],
                'communication': ['Public Speaking', 'Written Communication', 'Active Listening', 'Negotiation'],
                'problem_solving': ['Critical Thinking', 'Analytical Skills', 'Creativity', 'Innovation'],
                'emotional_intelligence': ['Self-Awareness', 'Empathy', 'Social Skills', 'Self-Regulation']
            },
            'business': {
                'finance': ['Financial Analysis', 'Budgeting', 'Forecasting', 'Investment Analysis'],
                'marketing': ['Digital Marketing', 'Content Strategy', 'SEO/SEM', 'Analytics'],
                'sales': ['Relationship Building', 'Negotiation', 'CRM', 'Lead Generation'],
                'operations': ['Process Improvement', 'Quality Management', 'Supply Chain', 'Lean Six Sigma']
            }
        }
        
        # Career progression paths
        self.career_paths = {
            'software_engineer': {
                'junior': ['Programming Fundamentals', 'Version Control', 'Testing', 'Debugging'],
                'mid': ['System Design', 'Architecture', 'Code Review', 'Mentoring'],
                'senior': ['Technical Leadership', 'Project Management', 'Strategic Planning'],
                'lead': ['Team Management', 'Hiring', 'Technology Strategy', 'Business Alignment']
            },
            'data_analyst': {
                'junior': ['Excel', 'SQL', 'Basic Statistics', 'Data Visualization'],
                'mid': ['Advanced Analytics', 'Python/R', 'Machine Learning', 'Business Intelligence'],
                'senior': ['Data Strategy', 'Advanced ML', 'Team Leadership', 'Stakeholder Management'],
                'lead': ['Data Science Strategy', 'Team Management', 'Business Strategy', 'Innovation']
            },
            'hr_specialist': {
                'junior': ['HR Fundamentals', 'Employment Law', 'Recruitment', 'Employee Relations'],
                'mid': ['Performance Management', 'Training & Development', 'Compensation', 'Analytics'],
                'senior': ['HR Strategy', 'Change Management', 'Leadership Development', 'Compliance'],
                'lead': ['Strategic HR', 'Organizational Development', 'Executive Coaching', 'Business Partnership']
            }
        }
        
        # Learning providers and resources
        self.learning_providers = {
            'coursera': {
                'type': 'online_platform',
                'strengths': ['University courses', 'Certificates', 'Specializations'],
                'cost_range': (29, 79),
                'quality_score': 9
            },
            'linkedin_learning': {
                'type': 'online_platform',
                'strengths': ['Professional skills', 'Business topics', 'Software training'],
                'cost_range': (29.99, 29.99),
                'quality_score': 8
            },
            'udemy': {
                'type': 'online_platform',
                'strengths': ['Technical skills', 'Practical projects', 'Affordable'],
                'cost_range': (10, 200),
                'quality_score': 7
            },
            'pluralsight': {
                'type': 'online_platform',
                'strengths': ['Technology skills', 'Skill assessments', 'Learning paths'],
                'cost_range': (29, 45),
                'quality_score': 8
            }
        }
        
        # Initialize database
        self._init_database()
    
    def _init_database(self):
        """Initialize database tables for development planning."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Skill assessments table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS skill_assessments (
                    assessment_id TEXT PRIMARY KEY,
                    employee_id TEXT NOT NULL,
                    skill_name TEXT NOT NULL,
                    current_level TEXT NOT NULL,
                    target_level TEXT NOT NULL,
                    importance INTEGER NOT NULL,
                    last_assessed TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    assessor TEXT NOT NULL,
                    evidence TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Development plans table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS development_plans (
                    plan_id TEXT PRIMARY KEY,
                    employee_id TEXT NOT NULL,
                    created_by TEXT NOT NULL,
                    goals TEXT NOT NULL,
                    skill_gaps TEXT NOT NULL,
                    recommended_actions TEXT NOT NULL,
                    timeline TEXT NOT NULL,
                    budget_estimate REAL,
                    success_metrics TEXT NOT NULL,
                    status TEXT DEFAULT 'active',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Learning recommendations table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS learning_recommendations (
                    recommendation_id TEXT PRIMARY KEY,
                    employee_id TEXT NOT NULL,
                    skill_target TEXT NOT NULL,
                    training_type TEXT NOT NULL,
                    provider TEXT NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT,
                    duration TEXT,
                    cost REAL,
                    relevance_score REAL,
                    difficulty_level TEXT,
                    prerequisites TEXT,
                    learning_outcomes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Learning progress table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS learning_progress (
                    progress_id TEXT PRIMARY KEY,
                    employee_id TEXT NOT NULL,
                    recommendation_id TEXT NOT NULL,
                    status TEXT DEFAULT 'not_started',
                    progress_percentage INTEGER DEFAULT 0,
                    started_at TIMESTAMP,
                    completed_at TIMESTAMP,
                    feedback TEXT,
                    rating INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (recommendation_id) REFERENCES learning_recommendations (recommendation_id)
                )
            ''')
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"Database initialization error: {str(e)}")
    
    async def analyze_skill_gaps(self, employee_id: str, target_role: Optional[str] = None) -> Dict[str, Any]:
        """
        Analyze skill gaps for an employee based on current skills and target role.
        
        Args:
            employee_id: Employee to analyze
            target_role: Optional target role for gap analysis
            
        Returns:
            Skill gap analysis results
        """
        try:
            # Get employee data
            employee_data = await self._get_employee_data(employee_id)
            if not employee_data:
                return {'error': 'Employee not found'}
            
            # Get current skill assessments
            current_skills = await self._get_skill_assessments(employee_id)
            
            # Determine target skills based on role
            if target_role:
                target_skills = self._get_role_requirements(target_role)
            else:
                # Use current role for improvement
                current_role = employee_data.get('position', '').lower().replace(' ', '_')
                target_skills = self._get_role_requirements(current_role)
            
            # Calculate skill gaps
            skill_gaps = []
            for skill_category, skills in target_skills.items():
                for skill in skills:
                    current_level = self._get_current_skill_level(skill, current_skills)
                    target_level = self._get_target_skill_level(skill, target_role or employee_data.get('position'))
                    
                    if self._skill_level_to_int(target_level) > self._skill_level_to_int(current_level):
                        gap = {
                            'skill_name': skill,
                            'category': skill_category,
                            'current_level': current_level,
                            'target_level': target_level,
                            'gap_size': self._skill_level_to_int(target_level) - self._skill_level_to_int(current_level),
                            'importance': self._calculate_skill_importance(skill, target_role or employee_data.get('position')),
                            'priority': 'high' if self._skill_level_to_int(target_level) - self._skill_level_to_int(current_level) >= 2 else 'medium'
                        }
                        skill_gaps.append(gap)
            
            # Sort by importance and gap size
            skill_gaps.sort(key=lambda x: (x['importance'], x['gap_size']), reverse=True)
            
            return {
                'employee_id': employee_id,
                'target_role': target_role,
                'skill_gaps': skill_gaps,
                'total_gaps': len(skill_gaps),
                'high_priority_gaps': len([g for g in skill_gaps if g['priority'] == 'high']),
                'analysis_date': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    async def generate_development_plan(self, employee_id: str, created_by: str, 
                                      goals: List[str], timeline_months: int = 12) -> str:
        """
        Generate a personalized development plan for an employee.
        
        Args:
            employee_id: Employee to create plan for
            created_by: User creating the plan
            goals: Development goals
            timeline_months: Plan timeline in months
            
        Returns:
            Development plan ID
        """
        try:
            # Analyze skill gaps
            gap_analysis = await self.analyze_skill_gaps(employee_id)
            if 'error' in gap_analysis:
                return None
            
            # Generate learning recommendations
            recommendations = await self.generate_learning_recommendations(
                employee_id, 
                gap_analysis['skill_gaps'][:10]  # Top 10 gaps
            )
            
            # Create timeline
            timeline = self._create_development_timeline(
                gap_analysis['skill_gaps'], 
                timeline_months
            )
            
            # Calculate budget estimate
            budget_estimate = self._calculate_budget_estimate(recommendations)
            
            # Define success metrics
            success_metrics = self._define_success_metrics(gap_analysis['skill_gaps'])
            
            # Create development plan
            plan_id = str(uuid.uuid4())
            
            plan_data = {
                'plan_id': plan_id,
                'employee_id': employee_id,
                'created_by': created_by,
                'goals': goals,
                'skill_gaps': gap_analysis['skill_gaps'],
                'recommended_actions': recommendations,
                'timeline': timeline,
                'budget_estimate': budget_estimate,
                'success_metrics': success_metrics,
                'created_at': datetime.now(),
                'updated_at': datetime.now(),
                'status': 'active'
            }
            
            # Save to database
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO development_plans 
                (plan_id, employee_id, created_by, goals, skill_gaps, recommended_actions, 
                 timeline, budget_estimate, success_metrics, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                plan_id,
                employee_id,
                created_by,
                json.dumps(goals),
                json.dumps(gap_analysis['skill_gaps']),
                json.dumps(recommendations),
                json.dumps(timeline),
                budget_estimate,
                json.dumps(success_metrics),
                'active'
            ))
            
            conn.commit()
            conn.close()
            
            return plan_id
            
        except Exception as e:
            print(f"Error generating development plan: {str(e)}")
            return None
    
    async def generate_learning_recommendations(self, employee_id: str, 
                                              skill_gaps: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Generate personalized learning recommendations based on skill gaps.
        
        Args:
            employee_id: Employee to generate recommendations for
            skill_gaps: List of identified skill gaps
            
        Returns:
            List of learning recommendations
        """
        try:
            recommendations = []
            
            # Get employee learning preferences
            employee_data = await self._get_employee_data(employee_id)
            learning_style = self._infer_learning_style(employee_data)
            
            for gap in skill_gaps:
                skill_name = gap['skill_name']
                current_level = gap['current_level']
                target_level = gap['target_level']
                
                # Find suitable learning resources
                suitable_resources = self._find_learning_resources(
                    skill_name, 
                    current_level, 
                    target_level,
                    learning_style
                )
                
                for resource in suitable_resources:
                    recommendation = {
                        'recommendation_id': str(uuid.uuid4()),
                        'employee_id': employee_id,
                        'skill_target': skill_name,
                        'training_type': resource['type'],
                        'provider': resource['provider'],
                        'title': resource['title'],
                        'description': resource['description'],
                        'duration': resource['duration'],
                        'cost': resource['cost'],
                        'relevance_score': resource['relevance_score'],
                        'difficulty_level': resource['difficulty_level'],
                        'prerequisites': resource['prerequisites'],
                        'learning_outcomes': resource['learning_outcomes']
                    }
                    
                    recommendations.append(recommendation)
                    
                    # Save to database
                    await self._save_learning_recommendation(recommendation)
            
            # Sort by relevance score
            recommendations.sort(key=lambda x: x['relevance_score'], reverse=True)
            
            return recommendations
            
        except Exception as e:
            print(f"Error generating learning recommendations: {str(e)}")
            return []
    
    async def track_learning_progress(self, employee_id: str, 
                                    recommendation_id: str, 
                                    progress_percentage: int,
                                    status: str = 'in_progress') -> bool:
        """
        Track learning progress for a recommendation.
        
        Args:
            employee_id: Employee ID
            recommendation_id: Learning recommendation ID
            progress_percentage: Progress percentage (0-100)
            status: Progress status
            
        Returns:
            Success status
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Check if progress record exists
            cursor.execute('''
                SELECT progress_id FROM learning_progress 
                WHERE employee_id = ? AND recommendation_id = ?
            ''', (employee_id, recommendation_id))
            
            existing = cursor.fetchone()
            
            if existing:
                # Update existing record
                cursor.execute('''
                    UPDATE learning_progress 
                    SET progress_percentage = ?, status = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE employee_id = ? AND recommendation_id = ?
                ''', (progress_percentage, status, employee_id, recommendation_id))
            else:
                # Create new record
                progress_id = str(uuid.uuid4())
                cursor.execute('''
                    INSERT INTO learning_progress 
                    (progress_id, employee_id, recommendation_id, progress_percentage, status)
                    VALUES (?, ?, ?, ?, ?)
                ''', (progress_id, employee_id, recommendation_id, progress_percentage, status))
            
            conn.commit()
            conn.close()
            
            return True
            
        except Exception as e:
            print(f"Error tracking learning progress: {str(e)}")
            return False
    
    async def get_development_analytics(self, employee_id: str) -> Dict[str, Any]:
        """
        Get development analytics for an employee.
        
        Args:
            employee_id: Employee to analyze
            
        Returns:
            Development analytics data
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get active development plans
            cursor.execute('''
                SELECT COUNT(*) FROM development_plans 
                WHERE employee_id = ? AND status = 'active'
            ''', (employee_id,))
            active_plans = cursor.fetchone()[0]
            
            # Get learning progress
            cursor.execute('''
                SELECT status, COUNT(*) as count 
                FROM learning_progress 
                WHERE employee_id = ? 
                GROUP BY status
            ''', (employee_id,))
            progress_counts = dict(cursor.fetchall())
            
            # Get average progress
            cursor.execute('''
                SELECT AVG(progress_percentage) 
                FROM learning_progress 
                WHERE employee_id = ?
            ''', (employee_id,))
            avg_progress = cursor.fetchone()[0] or 0
            
            # Get skill assessments count
            cursor.execute('''
                SELECT COUNT(*) FROM skill_assessments 
                WHERE employee_id = ?
            ''', (employee_id,))
            skill_assessments = cursor.fetchone()[0]
            
            conn.close()
            
            return {
                'employee_id': employee_id,
                'active_development_plans': active_plans,
                'learning_progress': progress_counts,
                'average_progress': round(avg_progress, 1),
                'skill_assessments_completed': skill_assessments,
                'completed_trainings': progress_counts.get('completed', 0),
                'in_progress_trainings': progress_counts.get('in_progress', 0),
                'development_score': self._calculate_development_score(
                    active_plans, avg_progress, progress_counts
                )
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    # Helper methods
    def _get_role_requirements(self, role: str) -> Dict[str, List[str]]:
        """Get skill requirements for a role."""
        role_key = role.lower().replace(' ', '_')
        
        if role_key in self.career_paths:
            # Get skills for current level and above
            all_skills = {}
            for level, skills in self.career_paths[role_key].items():
                category = 'technical' if 'engineer' in role_key or 'analyst' in role_key else 'business'
                if category not in all_skills:
                    all_skills[category] = []
                all_skills[category].extend(skills)
            return all_skills
        
        # Default skills for unknown roles
        return {
            'soft_skills': ['Communication', 'Problem Solving', 'Teamwork'],
            'technical': ['Computer Literacy', 'Industry Knowledge']
        }
    
    def _skill_level_to_int(self, level: str) -> int:
        """Convert skill level to integer for comparison."""
        level_map = {
            'beginner': 1,
            'intermediate': 2,
            'advanced': 3,
            'expert': 4
        }
        return level_map.get(level.lower(), 1)
    
    def _calculate_development_score(self, active_plans: int, avg_progress: float, 
                                   progress_counts: Dict[str, int]) -> int:
        """Calculate overall development score."""
        score = 0
        
        # Active engagement
        if active_plans > 0:
            score += 20
        
        # Progress completion
        score += min(avg_progress * 0.6, 60)  # Max 60 points for progress
        
        # Completed trainings
        completed = progress_counts.get('completed', 0)
        score += min(completed * 5, 20)  # Max 20 points for completions
        
        return min(int(score), 100)

# Additional helper methods would be implemented here...
# (Abbreviated for space)

