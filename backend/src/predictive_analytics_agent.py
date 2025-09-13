"""
Predictive Analytics Agent for HR Advisor
Provides predictive insights on employee retention, performance, hiring needs, and workforce trends
"""

import asyncio
import json
import uuid
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, mean_squared_error
import warnings
warnings.filterwarnings('ignore')

class PredictionType(Enum):
    RETENTION_RISK = "retention_risk"
    PERFORMANCE_FORECAST = "performance_forecast"
    HIRING_DEMAND = "hiring_demand"
    PROMOTION_READINESS = "promotion_readiness"
    COMPENSATION_ANALYSIS = "compensation_analysis"
    ENGAGEMENT_PREDICTION = "engagement_prediction"
    ABSENTEEISM_FORECAST = "absenteeism_forecast"
    TURNOVER_ANALYSIS = "turnover_analysis"

class RiskLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class PredictionResult:
    prediction_id: str
    employee_id: Optional[str]
    department: Optional[str]
    prediction_type: PredictionType
    risk_level: RiskLevel
    confidence_score: float
    predicted_value: Any
    contributing_factors: List[Dict[str, Any]]
    recommendations: List[str]
    prediction_date: datetime
    valid_until: datetime
    metadata: Dict[str, Any]

@dataclass
class ModelMetrics:
    model_id: str
    model_type: str
    accuracy: float
    precision: float
    recall: float
    f1_score: float
    last_trained: datetime
    training_samples: int
    feature_importance: Dict[str, float]

@dataclass
class WorkforceInsight:
    insight_id: str
    title: str
    description: str
    insight_type: str
    impact_level: RiskLevel
    affected_employees: int
    departments: List[str]
    trend_data: Dict[str, Any]
    recommendations: List[str]
    generated_date: datetime

class PredictiveAnalyticsAgent:
    def __init__(self):
        self.predictions: Dict[str, PredictionResult] = {}
        self.models: Dict[str, Any] = {}
        self.model_metrics: Dict[str, ModelMetrics] = {}
        self.insights: Dict[str, WorkforceInsight] = {}
        self.scalers: Dict[str, StandardScaler] = {}
        self.encoders: Dict[str, Dict[str, LabelEncoder]] = {}
        self._initialize_models()
    
    def _initialize_models(self):
        """Initialize predictive models"""
        
        # Retention Risk Model
        self.models['retention_risk'] = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        
        # Performance Forecast Model
        self.models['performance_forecast'] = GradientBoostingRegressor(
            n_estimators=100,
            max_depth=6,
            random_state=42
        )
        
        # Engagement Prediction Model
        self.models['engagement_prediction'] = RandomForestClassifier(
            n_estimators=100,
            max_depth=8,
            random_state=42
        )
        
        # Initialize scalers and encoders
        for model_name in self.models.keys():
            self.scalers[model_name] = StandardScaler()
            self.encoders[model_name] = {}
    
    async def predict_retention_risk(self, employee_data: List[Dict[str, Any]]) -> List[str]:
        """Predict retention risk for employees"""
        prediction_ids = []
        
        # Prepare data for prediction
        df = pd.DataFrame(employee_data)
        
        if len(df) < 10:  # Need minimum data for meaningful predictions
            return await self._generate_rule_based_retention_predictions(employee_data)
        
        # Feature engineering
        features = self._engineer_retention_features(df)
        
        # Train model if not already trained or needs retraining
        if 'retention_risk' not in self.model_metrics or self._needs_retraining('retention_risk'):
            await self._train_retention_model(features)
        
        # Make predictions
        for idx, employee in enumerate(employee_data):
            try:
                prediction_id = await self._predict_employee_retention(employee, features.iloc[idx])
                prediction_ids.append(prediction_id)
            except Exception as e:
                print(f"Error predicting retention for employee {employee.get('employee_id', 'unknown')}: {e}")
                continue
        
        return prediction_ids
    
    def _engineer_retention_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Engineer features for retention prediction"""
        features = df.copy()
        
        # Calculate tenure
        if 'hire_date' in features.columns:
            features['hire_date'] = pd.to_datetime(features['hire_date'], errors='coerce')
            features['tenure_days'] = (datetime.now() - features['hire_date']).dt.days
            features['tenure_years'] = features['tenure_days'] / 365.25
        else:
            features['tenure_years'] = 1.0  # Default
        
        # Salary percentile within department
        if 'salary' in features.columns and 'department' in features.columns:
            features['salary_percentile'] = features.groupby('department')['salary'].rank(pct=True)
        else:
            features['salary_percentile'] = 0.5  # Default
        
        # Age groups
        if 'age' in features.columns:
            features['age_group'] = pd.cut(features['age'], 
                                         bins=[0, 25, 35, 45, 55, 100], 
                                         labels=['<25', '25-35', '35-45', '45-55', '55+'])
        else:
            features['age_group'] = '25-35'  # Default
        
        # Performance indicators
        if 'performance_rating' in features.columns:
            features['high_performer'] = (features['performance_rating'] >= 4).astype(int)
        else:
            features['high_performer'] = 1  # Default
        
        # Engagement indicators
        if 'engagement_score' in features.columns:
            features['low_engagement'] = (features['engagement_score'] < 3).astype(int)
        else:
            features['low_engagement'] = 0  # Default
        
        # Manager relationship
        if 'manager_rating' in features.columns:
            features['poor_manager_relationship'] = (features['manager_rating'] < 3).astype(int)
        else:
            features['poor_manager_relationship'] = 0  # Default
        
        # Work-life balance
        if 'work_life_balance' in features.columns:
            features['poor_work_life_balance'] = (features['work_life_balance'] < 3).astype(int)
        else:
            features['poor_work_life_balance'] = 0  # Default
        
        # Recent promotion
        if 'last_promotion_date' in features.columns:
            features['last_promotion_date'] = pd.to_datetime(features['last_promotion_date'], errors='coerce')
            features['months_since_promotion'] = (datetime.now() - features['last_promotion_date']).dt.days / 30.44
            features['recent_promotion'] = (features['months_since_promotion'] <= 12).astype(int)
        else:
            features['recent_promotion'] = 0  # Default
        
        return features
    
    async def _train_retention_model(self, features: pd.DataFrame):
        """Train the retention risk model"""
        
        # Create synthetic target variable for demonstration
        # In real implementation, this would be historical turnover data
        target = self._generate_synthetic_retention_target(features)
        
        # Select features for training
        feature_columns = [
            'tenure_years', 'salary_percentile', 'high_performer', 
            'low_engagement', 'poor_manager_relationship', 'poor_work_life_balance',
            'recent_promotion'
        ]
        
        # Ensure all feature columns exist
        for col in feature_columns:
            if col not in features.columns:
                features[col] = 0  # Default value
        
        X = features[feature_columns].fillna(0)
        y = target
        
        # Encode categorical variables if any
        categorical_columns = X.select_dtypes(include=['object']).columns
        for col in categorical_columns:
            if col not in self.encoders['retention_risk']:
                self.encoders['retention_risk'][col] = LabelEncoder()
            X[col] = self.encoders['retention_risk'][col].fit_transform(X[col].astype(str))
        
        # Scale features
        X_scaled = self.scalers['retention_risk'].fit_transform(X)
        
        # Train model
        self.models['retention_risk'].fit(X_scaled, y)
        
        # Calculate metrics
        y_pred = self.models['retention_risk'].predict(X_scaled)
        accuracy = accuracy_score(y, y_pred)
        
        # Store model metrics
        feature_importance = dict(zip(feature_columns, self.models['retention_risk'].feature_importances_))
        
        self.model_metrics['retention_risk'] = ModelMetrics(
            model_id='retention_risk_v1',
            model_type='RandomForestClassifier',
            accuracy=accuracy,
            precision=accuracy,  # Simplified for demo
            recall=accuracy,
            f1_score=accuracy,
            last_trained=datetime.now(),
            training_samples=len(X),
            feature_importance=feature_importance
        )
    
    def _generate_synthetic_retention_target(self, features: pd.DataFrame) -> np.ndarray:
        """Generate synthetic retention target for training"""
        # This creates a realistic retention risk based on common factors
        risk_score = 0
        
        # Tenure factor (U-shaped curve - new and very long tenure employees at higher risk)
        if 'tenure_years' in features.columns:
            tenure_risk = np.where(
                (features['tenure_years'] < 1) | (features['tenure_years'] > 10),
                0.3, 0.1
            )
            risk_score += tenure_risk
        
        # Performance factor
        if 'high_performer' in features.columns:
            performance_risk = np.where(features['high_performer'] == 0, 0.4, 0.1)
            risk_score += performance_risk
        
        # Engagement factor
        if 'low_engagement' in features.columns:
            engagement_risk = np.where(features['low_engagement'] == 1, 0.5, 0.1)
            risk_score += engagement_risk
        
        # Manager relationship factor
        if 'poor_manager_relationship' in features.columns:
            manager_risk = np.where(features['poor_manager_relationship'] == 1, 0.3, 0.1)
            risk_score += manager_risk
        
        # Add some randomness
        risk_score += np.random.normal(0, 0.1, len(features))
        
        # Convert to binary target (1 = high retention risk)
        return (risk_score > 0.5).astype(int)
    
    async def _predict_employee_retention(self, employee: Dict[str, Any], 
                                        features: pd.Series) -> str:
        """Predict retention risk for a single employee"""
        
        # Prepare features
        feature_columns = [
            'tenure_years', 'salary_percentile', 'high_performer', 
            'low_engagement', 'poor_manager_relationship', 'poor_work_life_balance',
            'recent_promotion'
        ]
        
        X = np.array([[features.get(col, 0) for col in feature_columns]])
        X_scaled = self.scalers['retention_risk'].transform(X)
        
        # Make prediction
        risk_prob = self.models['retention_risk'].predict_proba(X_scaled)[0]
        risk_prediction = self.models['retention_risk'].predict(X_scaled)[0]
        
        # Determine risk level
        high_risk_prob = risk_prob[1] if len(risk_prob) > 1 else risk_prob[0]
        
        if high_risk_prob >= 0.8:
            risk_level = RiskLevel.CRITICAL
        elif high_risk_prob >= 0.6:
            risk_level = RiskLevel.HIGH
        elif high_risk_prob >= 0.4:
            risk_level = RiskLevel.MEDIUM
        else:
            risk_level = RiskLevel.LOW
        
        # Identify contributing factors
        feature_importance = self.model_metrics['retention_risk'].feature_importance
        contributing_factors = []
        
        for i, col in enumerate(feature_columns):
            factor_value = X[0][i]
            importance = feature_importance.get(col, 0)
            
            if importance > 0.1:  # Only include significant factors
                contributing_factors.append({
                    "factor": col.replace('_', ' ').title(),
                    "value": factor_value,
                    "importance": importance,
                    "impact": "negative" if factor_value > 0.5 else "positive"
                })
        
        # Generate recommendations
        recommendations = self._generate_retention_recommendations(
            employee, features, contributing_factors
        )
        
        # Create prediction result
        prediction_id = str(uuid.uuid4())
        prediction = PredictionResult(
            prediction_id=prediction_id,
            employee_id=employee.get('employee_id'),
            department=employee.get('department'),
            prediction_type=PredictionType.RETENTION_RISK,
            risk_level=risk_level,
            confidence_score=max(risk_prob),
            predicted_value={"retention_risk_probability": high_risk_prob},
            contributing_factors=contributing_factors,
            recommendations=recommendations,
            prediction_date=datetime.now(),
            valid_until=datetime.now() + timedelta(days=90),
            metadata={
                "model_version": "v1",
                "employee_name": employee.get('name', 'Unknown'),
                "current_role": employee.get('job_title', 'Unknown')
            }
        )
        
        self.predictions[prediction_id] = prediction
        return prediction_id
    
    def _generate_retention_recommendations(self, employee: Dict[str, Any], 
                                          features: pd.Series,
                                          contributing_factors: List[Dict[str, Any]]) -> List[str]:
        """Generate retention recommendations based on risk factors"""
        recommendations = []
        
        # Analyze contributing factors
        factor_names = [f["factor"].lower() for f in contributing_factors]
        
        if "low engagement" in factor_names:
            recommendations.extend([
                "Schedule one-on-one meeting to discuss engagement concerns",
                "Consider role adjustment or new challenges",
                "Explore professional development opportunities"
            ])
        
        if "poor manager relationship" in factor_names:
            recommendations.extend([
                "Facilitate manager-employee relationship coaching",
                "Consider team or manager reassignment if appropriate",
                "Provide conflict resolution support"
            ])
        
        if "poor work life balance" in factor_names:
            recommendations.extend([
                "Review workload and redistribute if necessary",
                "Discuss flexible work arrangements",
                "Promote wellness programs and time-off usage"
            ])
        
        if "tenure years" in factor_names:
            tenure = features.get('tenure_years', 1)
            if tenure < 1:
                recommendations.extend([
                    "Enhance onboarding and mentorship programs",
                    "Provide clear career path guidance",
                    "Increase check-in frequency during first year"
                ])
            elif tenure > 10:
                recommendations.extend([
                    "Explore new challenges and growth opportunities",
                    "Consider leadership or mentoring roles",
                    "Discuss long-term career aspirations"
                ])
        
        if not recommendations:
            recommendations = [
                "Continue regular performance discussions",
                "Monitor engagement levels closely",
                "Maintain open communication channels"
            ]
        
        return recommendations
    
    async def _generate_rule_based_retention_predictions(self, 
                                                       employee_data: List[Dict[str, Any]]) -> List[str]:
        """Generate rule-based retention predictions when insufficient data for ML"""
        prediction_ids = []
        
        for employee in employee_data:
            # Simple rule-based assessment
            risk_factors = 0
            
            # Check engagement
            if employee.get('engagement_score', 5) < 3:
                risk_factors += 2
            
            # Check performance
            if employee.get('performance_rating', 5) < 3:
                risk_factors += 2
            
            # Check tenure (new employees and very long tenure)
            tenure_years = employee.get('tenure_years', 1)
            if tenure_years < 0.5 or tenure_years > 15:
                risk_factors += 1
            
            # Check salary satisfaction
            if employee.get('salary_satisfaction', 5) < 3:
                risk_factors += 1
            
            # Check work-life balance
            if employee.get('work_life_balance', 5) < 3:
                risk_factors += 1
            
            # Determine risk level
            if risk_factors >= 4:
                risk_level = RiskLevel.CRITICAL
            elif risk_factors >= 3:
                risk_level = RiskLevel.HIGH
            elif risk_factors >= 2:
                risk_level = RiskLevel.MEDIUM
            else:
                risk_level = RiskLevel.LOW
            
            # Create prediction
            prediction_id = str(uuid.uuid4())
            prediction = PredictionResult(
                prediction_id=prediction_id,
                employee_id=employee.get('employee_id'),
                department=employee.get('department'),
                prediction_type=PredictionType.RETENTION_RISK,
                risk_level=risk_level,
                confidence_score=0.7,  # Lower confidence for rule-based
                predicted_value={"risk_factors_count": risk_factors},
                contributing_factors=[
                    {"factor": "Rule-based assessment", "value": risk_factors, "importance": 1.0}
                ],
                recommendations=self._generate_retention_recommendations(employee, pd.Series(employee), []),
                prediction_date=datetime.now(),
                valid_until=datetime.now() + timedelta(days=30),
                metadata={"method": "rule_based", "insufficient_data": True}
            )
            
            self.predictions[prediction_id] = prediction
            prediction_ids.append(prediction_id)
        
        return prediction_ids
    
    async def predict_hiring_demand(self, department_data: Dict[str, Any], 
                                  historical_data: List[Dict[str, Any]]) -> str:
        """Predict hiring demand for departments"""
        
        # Analyze historical trends
        df = pd.DataFrame(historical_data)
        
        # Calculate turnover rate
        total_employees = len(df)
        terminated_employees = len(df[df.get('status') == 'terminated'])
        turnover_rate = terminated_employees / total_employees if total_employees > 0 else 0
        
        # Calculate growth rate
        current_headcount = department_data.get('current_headcount', 0)
        target_headcount = department_data.get('target_headcount', current_headcount)
        growth_rate = (target_headcount - current_headcount) / current_headcount if current_headcount > 0 else 0
        
        # Predict hiring needs
        replacement_hires = int(current_headcount * turnover_rate)
        growth_hires = max(0, target_headcount - current_headcount)
        total_hiring_need = replacement_hires + growth_hires
        
        # Determine urgency
        if total_hiring_need >= current_headcount * 0.3:
            risk_level = RiskLevel.CRITICAL
        elif total_hiring_need >= current_headcount * 0.2:
            risk_level = RiskLevel.HIGH
        elif total_hiring_need >= current_headcount * 0.1:
            risk_level = RiskLevel.MEDIUM
        else:
            risk_level = RiskLevel.LOW
        
        # Generate recommendations
        recommendations = [
            f"Plan to hire {total_hiring_need} employees in next 12 months",
            f"Budget for {replacement_hires} replacement hires due to turnover",
            f"Prepare for {growth_hires} growth-related hires"
        ]
        
        if risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]:
            recommendations.extend([
                "Start recruitment process immediately",
                "Consider temporary staffing solutions",
                "Review and improve retention strategies"
            ])
        
        # Create prediction
        prediction_id = str(uuid.uuid4())
        prediction = PredictionResult(
            prediction_id=prediction_id,
            employee_id=None,
            department=department_data.get('department'),
            prediction_type=PredictionType.HIRING_DEMAND,
            risk_level=risk_level,
            confidence_score=0.8,
            predicted_value={
                "total_hiring_need": total_hiring_need,
                "replacement_hires": replacement_hires,
                "growth_hires": growth_hires,
                "turnover_rate": turnover_rate,
                "growth_rate": growth_rate
            },
            contributing_factors=[
                {"factor": "Turnover Rate", "value": turnover_rate, "importance": 0.6},
                {"factor": "Growth Rate", "value": growth_rate, "importance": 0.4}
            ],
            recommendations=recommendations,
            prediction_date=datetime.now(),
            valid_until=datetime.now() + timedelta(days=180),
            metadata={
                "current_headcount": current_headcount,
                "target_headcount": target_headcount,
                "department": department_data.get('department')
            }
        )
        
        self.predictions[prediction_id] = prediction
        return prediction_id
    
    async def generate_workforce_insights(self, employee_data: List[Dict[str, Any]]) -> List[str]:
        """Generate workforce insights and trends"""
        insight_ids = []
        
        df = pd.DataFrame(employee_data)
        
        if len(df) == 0:
            return insight_ids
        
        # Insight 1: Retention Risk by Department
        if 'department' in df.columns:
            dept_retention_insight = await self._analyze_department_retention_risk(df)
            if dept_retention_insight:
                insight_ids.append(dept_retention_insight)
        
        # Insight 2: Performance Distribution
        if 'performance_rating' in df.columns:
            performance_insight = await self._analyze_performance_distribution(df)
            if performance_insight:
                insight_ids.append(performance_insight)
        
        # Insight 3: Tenure Analysis
        if 'hire_date' in df.columns:
            tenure_insight = await self._analyze_tenure_patterns(df)
            if tenure_insight:
                insight_ids.append(tenure_insight)
        
        # Insight 4: Compensation Equity
        if 'salary' in df.columns and 'department' in df.columns:
            compensation_insight = await self._analyze_compensation_equity(df)
            if compensation_insight:
                insight_ids.append(compensation_insight)
        
        return insight_ids
    
    async def _analyze_department_retention_risk(self, df: pd.DataFrame) -> Optional[str]:
        """Analyze retention risk by department"""
        
        # Calculate retention risk by department (simplified)
        dept_risk = {}
        for dept in df['department'].unique():
            dept_employees = df[df['department'] == dept]
            
            # Simple risk calculation based on engagement and performance
            low_engagement = len(dept_employees[dept_employees.get('engagement_score', 5) < 3])
            low_performance = len(dept_employees[dept_employees.get('performance_rating', 5) < 3])
            total = len(dept_employees)
            
            risk_score = (low_engagement + low_performance) / (total * 2) if total > 0 else 0
            dept_risk[dept] = risk_score
        
        # Find highest risk department
        if not dept_risk:
            return None
        
        highest_risk_dept = max(dept_risk, key=dept_risk.get)
        highest_risk_score = dept_risk[highest_risk_dept]
        
        if highest_risk_score < 0.2:
            return None  # No significant risk
        
        # Determine impact level
        if highest_risk_score >= 0.5:
            impact_level = RiskLevel.CRITICAL
        elif highest_risk_score >= 0.3:
            impact_level = RiskLevel.HIGH
        else:
            impact_level = RiskLevel.MEDIUM
        
        # Generate insight
        insight_id = str(uuid.uuid4())
        insight = WorkforceInsight(
            insight_id=insight_id,
            title=f"High Retention Risk in {highest_risk_dept}",
            description=f"The {highest_risk_dept} department shows elevated retention risk with {highest_risk_score:.1%} of employees at risk",
            insight_type="retention_risk",
            impact_level=impact_level,
            affected_employees=len(df[df['department'] == highest_risk_dept]),
            departments=[highest_risk_dept],
            trend_data={"department_risk_scores": dept_risk},
            recommendations=[
                f"Conduct engagement survey in {highest_risk_dept}",
                "Review management practices and workload distribution",
                "Implement targeted retention initiatives",
                "Consider compensation and benefits review"
            ],
            generated_date=datetime.now()
        )
        
        self.insights[insight_id] = insight
        return insight_id
    
    async def _analyze_performance_distribution(self, df: pd.DataFrame) -> Optional[str]:
        """Analyze performance rating distribution"""
        
        performance_dist = df['performance_rating'].value_counts().sort_index()
        total_employees = len(df)
        
        # Check for concerning patterns
        low_performers = len(df[df['performance_rating'] < 3])
        low_performer_pct = low_performers / total_employees
        
        high_performers = len(df[df['performance_rating'] >= 4])
        high_performer_pct = high_performers / total_employees
        
        # Generate insight if there's an issue
        if low_performer_pct > 0.2:  # More than 20% low performers
            impact_level = RiskLevel.HIGH if low_performer_pct > 0.3 else RiskLevel.MEDIUM
            
            insight_id = str(uuid.uuid4())
            insight = WorkforceInsight(
                insight_id=insight_id,
                title="High Percentage of Low Performers",
                description=f"{low_performer_pct:.1%} of employees have performance ratings below 3.0",
                insight_type="performance_distribution",
                impact_level=impact_level,
                affected_employees=low_performers,
                departments=list(df['department'].unique()) if 'department' in df.columns else [],
                trend_data={
                    "performance_distribution": performance_dist.to_dict(),
                    "low_performer_percentage": low_performer_pct,
                    "high_performer_percentage": high_performer_pct
                },
                recommendations=[
                    "Implement performance improvement plans",
                    "Review training and development programs",
                    "Assess management effectiveness",
                    "Consider role-fit evaluations"
                ],
                generated_date=datetime.now()
            )
            
            self.insights[insight_id] = insight
            return insight_id
        
        return None
    
    async def _analyze_tenure_patterns(self, df: pd.DataFrame) -> Optional[str]:
        """Analyze employee tenure patterns"""
        
        df['hire_date'] = pd.to_datetime(df['hire_date'], errors='coerce')
        df['tenure_years'] = (datetime.now() - df['hire_date']).dt.days / 365.25
        
        # Analyze tenure distribution
        short_tenure = len(df[df['tenure_years'] < 1])  # Less than 1 year
        medium_tenure = len(df[(df['tenure_years'] >= 1) & (df['tenure_years'] < 5)])
        long_tenure = len(df[df['tenure_years'] >= 5])
        
        total = len(df)
        short_tenure_pct = short_tenure / total
        
        # Check for high early turnover
        if short_tenure_pct > 0.3:  # More than 30% with less than 1 year tenure
            impact_level = RiskLevel.HIGH if short_tenure_pct > 0.5 else RiskLevel.MEDIUM
            
            insight_id = str(uuid.uuid4())
            insight = WorkforceInsight(
                insight_id=insight_id,
                title="High Early Career Turnover Risk",
                description=f"{short_tenure_pct:.1%} of employees have less than 1 year tenure, indicating potential early-career retention issues",
                insight_type="tenure_analysis",
                impact_level=impact_level,
                affected_employees=short_tenure,
                departments=list(df['department'].unique()) if 'department' in df.columns else [],
                trend_data={
                    "short_tenure_count": short_tenure,
                    "medium_tenure_count": medium_tenure,
                    "long_tenure_count": long_tenure,
                    "short_tenure_percentage": short_tenure_pct
                },
                recommendations=[
                    "Review and enhance onboarding programs",
                    "Implement mentorship for new hires",
                    "Analyze exit interview feedback",
                    "Improve early-career development paths"
                ],
                generated_date=datetime.now()
            )
            
            self.insights[insight_id] = insight
            return insight_id
        
        return None
    
    async def _analyze_compensation_equity(self, df: pd.DataFrame) -> Optional[str]:
        """Analyze compensation equity across departments"""
        
        # Calculate salary statistics by department
        dept_salary_stats = df.groupby('department')['salary'].agg(['mean', 'median', 'std']).round(2)
        
        # Check for significant variations
        overall_median = df['salary'].median()
        equity_issues = []
        
        for dept in dept_salary_stats.index:
            dept_median = dept_salary_stats.loc[dept, 'median']
            dept_std = dept_salary_stats.loc[dept, 'std']
            
            # Check for significant deviation from overall median
            deviation = abs(dept_median - overall_median) / overall_median
            
            if deviation > 0.2:  # More than 20% deviation
                equity_issues.append({
                    "department": dept,
                    "median_salary": dept_median,
                    "deviation": deviation,
                    "std_dev": dept_std
                })
        
        if equity_issues:
            insight_id = str(uuid.uuid4())
            insight = WorkforceInsight(
                insight_id=insight_id,
                title="Compensation Equity Concerns",
                description=f"Significant salary variations detected across {len(equity_issues)} departments",
                insight_type="compensation_equity",
                impact_level=RiskLevel.MEDIUM,
                affected_employees=len(df),
                departments=[issue["department"] for issue in equity_issues],
                trend_data={
                    "department_salary_stats": dept_salary_stats.to_dict(),
                    "equity_issues": equity_issues,
                    "overall_median": overall_median
                },
                recommendations=[
                    "Conduct comprehensive compensation analysis",
                    "Review job leveling and salary bands",
                    "Ensure pay equity compliance",
                    "Consider market rate adjustments"
                ],
                generated_date=datetime.now()
            )
            
            self.insights[insight_id] = insight
            return insight_id
        
        return None
    
    def _needs_retraining(self, model_name: str) -> bool:
        """Check if model needs retraining"""
        if model_name not in self.model_metrics:
            return True
        
        metrics = self.model_metrics[model_name]
        days_since_training = (datetime.now() - metrics.last_trained).days
        
        # Retrain if model is older than 30 days or accuracy is low
        return days_since_training > 30 or metrics.accuracy < 0.7
    
    def get_predictions(self, prediction_type: Optional[PredictionType] = None,
                       employee_id: Optional[str] = None,
                       department: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get predictions with optional filtering"""
        predictions = []
        
        for prediction in self.predictions.values():
            # Apply filters
            if prediction_type and prediction.prediction_type != prediction_type:
                continue
            if employee_id and prediction.employee_id != employee_id:
                continue
            if department and prediction.department != department:
                continue
            
            # Check if prediction is still valid
            if prediction.valid_until < datetime.now():
                continue
            
            predictions.append({
                "prediction_id": prediction.prediction_id,
                "employee_id": prediction.employee_id,
                "department": prediction.department,
                "prediction_type": prediction.prediction_type.value,
                "risk_level": prediction.risk_level.value,
                "confidence_score": prediction.confidence_score,
                "predicted_value": prediction.predicted_value,
                "contributing_factors": prediction.contributing_factors,
                "recommendations": prediction.recommendations,
                "prediction_date": prediction.prediction_date.isoformat(),
                "valid_until": prediction.valid_until.isoformat(),
                "metadata": prediction.metadata
            })
        
        return sorted(predictions, key=lambda x: x["prediction_date"], reverse=True)
    
    def get_insights(self, insight_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get workforce insights"""
        insights = []
        
        for insight in self.insights.values():
            if insight_type and insight.insight_type != insight_type:
                continue
            
            insights.append({
                "insight_id": insight.insight_id,
                "title": insight.title,
                "description": insight.description,
                "insight_type": insight.insight_type,
                "impact_level": insight.impact_level.value,
                "affected_employees": insight.affected_employees,
                "departments": insight.departments,
                "trend_data": insight.trend_data,
                "recommendations": insight.recommendations,
                "generated_date": insight.generated_date.isoformat()
            })
        
        return sorted(insights, key=lambda x: x["generated_date"], reverse=True)
    
    def get_model_performance(self) -> Dict[str, Any]:
        """Get model performance metrics"""
        performance = {}
        
        for model_name, metrics in self.model_metrics.items():
            performance[model_name] = {
                "model_id": metrics.model_id,
                "model_type": metrics.model_type,
                "accuracy": metrics.accuracy,
                "precision": metrics.precision,
                "recall": metrics.recall,
                "f1_score": metrics.f1_score,
                "last_trained": metrics.last_trained.isoformat(),
                "training_samples": metrics.training_samples,
                "feature_importance": metrics.feature_importance
            }
        
        return performance

# Global instance
predictive_agent = PredictiveAnalyticsAgent()

