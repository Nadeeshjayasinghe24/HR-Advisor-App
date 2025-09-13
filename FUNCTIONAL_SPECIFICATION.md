# AnNi AI - Functional Specification Document

**Version:** 1.1  
**Last Updated:** September 2025  
**Document Type:** Technical & Functional Specification  
**Platform:** AnNi AI - HR made simple  

---

## 📋 **Executive Summary**

AnNi AI is an intelligent, multi-agent HR management platform designed specifically for the APAC market. The platform transforms complex HR processes into simple, conversational interactions while maintaining enterprise-grade capabilities through sophisticated AI orchestration.

### **Core Value Proposition**
- **"HR made simple"** - Zero learning curve interface
- **Multi-agent AI system** - 6+ AI providers working in parallel
- **APAC-focused compliance** - 13 countries with localized expertise
- **Proactive automation** - Predictive insights and workflow management

---

## 🏗️ **System Architecture**

### **High-Level Architecture**
```
┌─────────────────────────────────────────────────────────────┐
│                    AnNi AI Platform                         │
├─────────────────────────────────────────────────────────────┤
│  Frontend (React)           │  Backend (Flask)              │
│  ├── Simplified Dashboard   │  ├── Multi-LLM Orchestrator   │
│  ├── Conversational AI      │  ├── Workflow Automation      │
│  ├── Employee Management    │  ├── Document Generation      │
│  ├── HR Analytics          │  ├── Predictive Analytics     │
│  └── Authentication        │  ├── Compliance Monitoring    │
│                            │  └── AI Governance           │
├─────────────────────────────────────────────────────────────┤
│                    Agent Layer                              │
│  ├── OpenAI (GPT-4, GPT-3.5)    ├── Groq (Llama 3.3)      │
│  ├── Google (Gemini Pro/Flash)   ├── DeepSeek (R1/V3)      │
│  ├── Anthropic (Claude-3)        ├── Together AI (Llama)   │
├─────────────────────────────────────────────────────────────┤
│                    Data Layer                               │
│  ├── SQLite Database            ├── Source Integration     │
│  ├── User Management            ├── Government APIs        │
│  ├── Employee Records           ├── Legal Databases        │
│  └── Analytics Storage          └── Compliance Sources     │
└─────────────────────────────────────────────────────────────┘
```

### **Technology Stack**

#### **Frontend**
- **Framework:** React 18+ with Vite
- **UI Library:** Shadcn/UI components
- **Styling:** Tailwind CSS
- **State Management:** React Hooks
- **Authentication:** JWT tokens
- **Deployment:** Vercel (static hosting)

#### **Backend**
- **Framework:** Flask (Python)
- **Database:** SQLite with SQLAlchemy ORM
- **Authentication:** JWT with bcrypt
- **AI Integration:** Multiple provider SDKs
- **Deployment:** Render (cloud hosting)

#### **AI Providers**
- **OpenAI:** GPT-4, GPT-3.5-turbo
- **Google:** Gemini Pro, Gemini Flash
- **Anthropic:** Claude-3 Sonnet, Claude-3 Haiku
- **Groq:** Llama 3.3 70B, Llama 3.1 8B
- **OpenRouter:** DeepSeek R1, DeepSeek V3
- **Together AI:** Llama 3.2 11B

---

## 🤖 **Agent System Architecture**
### Recent Update: Agent system update: Add comprehensive functional specification document and automated documentation agent
**Date:** 2025-09-13
**Impact:** High


### Recent Update: Agent system update: Fix regex bug in documentation agent
**Date:** 2025-09-13
**Impact:** High


### Recent Update: Agent system update: Add comprehensive functional specification document and automated documentation agent
**Date:** 2025-09-13
**Impact:** High



### **1. Multi-LLM Orchestration Agent (Master Agent)**

**Location:** `/backend/src/llm_orchestrator.py`

**Responsibilities:**
- Query routing and load balancing
- Parallel execution coordination
- Response validation and ranking
- Voting mechanism implementation
- Fallback system management

**Key Methods:**
```python
async def orchestrate_llm_responses(query, country_context, user_context)
async def validate_responses(responses)
async def select_best_response(responses, criteria)
async def handle_provider_failure(provider, fallback_providers)
```

**Decision Logic:**
- **Complex legal queries** → DeepSeek R1 (reasoning capabilities)
- **General HR advice** → Groq Llama 3.3 70B (fast, reliable)
- **High-volume queries** → Together AI (unlimited free tier)
- **Premium features** → OpenAI GPT-4 (highest quality)

### **2. Workflow Automation Agent**

**Location:** `/backend/src/workflow_automation_agent.py`

**Capabilities:**
- **360 Performance Reviews:** Automated creation, scheduling, and tracking
- **Onboarding Workflows:** Multi-step process automation
- **Offboarding Processes:** Compliance-driven exit procedures
- **Policy Enforcement:** Automated compliance checking
- **Task Management:** Assignment and progress tracking

**Workflow Types:**
```python
WORKFLOW_TYPES = {
    'performance_review_360': {
        'steps': ['self_assessment', 'peer_feedback', 'manager_review', 'goal_setting'],
        'duration': '30_days',
        'automation_level': 'high'
    },
    'employee_onboarding': {
        'steps': ['welcome_email', 'document_collection', 'training_schedule', 'buddy_assignment'],
        'duration': '90_days',
        'automation_level': 'full'
    },
    'compliance_audit': {
        'steps': ['data_collection', 'policy_review', 'gap_analysis', 'action_plan'],
        'duration': '14_days',
        'automation_level': 'medium'
    }
}
```

### **3. Document Generation Agent**

**Location:** `/backend/src/document_generation_agent.py`

**Document Types:**
- **Employment Contracts:** Country-specific legal templates
- **Policy Documents:** HR policies with local compliance
- **Performance Reports:** Automated analytics summaries
- **Compliance Reports:** Regulatory requirement tracking
- **Training Materials:** Role-specific onboarding content

**Generation Process:**
1. **Template Selection:** Based on document type and country
2. **Data Integration:** Employee and company information
3. **Legal Compliance:** Country-specific requirements
4. **Quality Assurance:** Multi-agent validation
5. **Version Control:** Document history tracking

### **4. Predictive Analytics Agent**

**Location:** `/backend/src/predictive_analytics_agent.py`

**Prediction Models:**
- **Retention Risk:** Employee likelihood to leave
- **Performance Trends:** Future performance indicators
- **Hiring Needs:** Workforce planning predictions
- **Compliance Risks:** Potential policy violations
- **Engagement Patterns:** Team morale forecasting

**Analytics Capabilities:**
```python
ANALYTICS_MODELS = {
    'retention_risk': {
        'features': ['engagement_score', 'performance_rating', 'tenure', 'salary_percentile'],
        'algorithm': 'gradient_boosting',
        'accuracy': '87%'
    },
    'performance_prediction': {
        'features': ['historical_ratings', 'goal_achievement', 'training_completion'],
        'algorithm': 'neural_network',
        'accuracy': '82%'
    }
}
```

### **5. Proactive Compliance Agent**

**Location:** `/backend/src/proactive_compliance_agent.py`

**Monitoring Areas:**
- **Policy Violations:** Real-time detection
- **Regulatory Changes:** Government update tracking
- **Deadline Management:** Compliance timeline monitoring
- **Risk Assessment:** Continuous compliance scoring
- **Alert System:** Proactive notification management

**Compliance Coverage:**
- **13 APAC Countries:** Singapore, Australia, Malaysia, Hong Kong, Japan, etc.
- **Employment Laws:** Local labor regulations
- **Data Privacy:** GDPR, PDPA compliance
- **Industry Standards:** HR best practices

### **6. AI Governance Agent**

**Location:** `/backend/src/ai_governance_agent.py`

**Governance Functions:**
- **Usage Monitoring:** AI provider utilization tracking
- **Quality Assurance:** Response accuracy validation
- **Bias Detection:** Fairness and equity monitoring
- **Audit Trails:** Decision process logging
- **Performance Metrics:** System effectiveness measurement

**Governance Metrics:**
```python
GOVERNANCE_METRICS = {
    'response_accuracy': 'percentage_of_validated_responses',
    'bias_detection': 'fairness_score_across_demographics',
    'system_reliability': 'uptime_and_error_rates',
    'user_satisfaction': 'feedback_and_usage_patterns'
}
```

---

## 🎯 **Core Features**
<!-- UI Update: UI component update: Complete rebranding to AnNi AI - HR made simple - 2025-09-13 -->

<!-- UI Update: UI component update: Complete rebranding to AnNi AI - HR made simple - 2025-09-13 -->


### **1. Conversational AI Interface**

**Component:** `ConversationalAI.jsx`

**Capabilities:**
- **Natural Language Processing:** Plain English queries
- **Context Awareness:** Conversation history and user context
- **Smart Suggestions:** Proactive recommendations
- **Multi-turn Conversations:** Complex query handling
- **Action Integration:** Direct task execution from chat

**Example Interactions:**
```
User: "Show me employees at retention risk"
AnNi AI: "I've identified 3 employees at retention risk:
• John Smith (Engineering) - Low engagement, no recent promotion
• Sarah Johnson (Marketing) - Work-life balance concerns
• Mike Chen (Sales) - Manager relationship issues

Would you like me to schedule one-on-one meetings?"

[Schedule Meetings] [Generate Report] [Create Action Plan]
```

### **2. Employee Management System**

**Components:** `EmployeeTable.jsx`, `EmployeeManagement.jsx`

**Features:**
- **Comprehensive Profiles:** 25+ data fields per employee
- **Table Interface:** Sortable, searchable, filterable
- **CRUD Operations:** Create, read, update, delete
- **Bulk Actions:** Mass updates and operations
- **Export Capabilities:** CSV, PDF report generation

**Employee Data Model:**
```python
class Employee(db.Model):
    # Personal Information
    employee_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    
    # Employment Details
    position = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    hire_date = db.Column(db.Date, nullable=False)
    employment_type = db.Column(db.String(50), nullable=False)
    salary = db.Column(db.Decimal(10, 2))
    country = db.Column(db.String(100), nullable=False)
    
    # HR Analytics Fields
    performance_rating = db.Column(db.Float)
    engagement_score = db.Column(db.Float)
    last_promotion_date = db.Column(db.Date)
    training_completion_rate = db.Column(db.Float)
    absenteeism_rate = db.Column(db.Float)
    
    # Diversity & Demographics
    gender = db.Column(db.String(20))
    age_group = db.Column(db.String(20))
    ethnicity = db.Column(db.String(50))
    
    # Status & Tracking
    status = db.Column(db.String(20), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
```

### **3. HR Analytics Dashboard**

**Component:** `HRAnalyticsDashboard.jsx`

**Analytics Modules:**

#### **Workforce Overview**
- **Headcount Metrics:** Total, by department, location, type
- **Growth Trends:** Hiring vs. exits over time
- **Demographic Breakdown:** Age, gender, ethnicity distribution

#### **Performance Analytics**
- **Performance Distribution:** Rating spread across organization
- **Top Performers:** High-achieving employees identification
- **Improvement Areas:** Underperformance pattern analysis

#### **Retention & Engagement**
- **Turnover Rates:** Voluntary vs. involuntary separation
- **Retention Risk:** Predictive analytics for at-risk employees
- **Engagement Scores:** Team and individual satisfaction metrics

#### **Compliance Monitoring**
- **Policy Adherence:** Compliance rate tracking
- **Training Completion:** Mandatory training status
- **Audit Readiness:** Compliance documentation status

### **4. Simplified Dashboard**

**Component:** `SimplifiedDashboard.jsx`

**User Experience Design:**
- **Personalized Greeting:** Time-aware, user-specific welcome
- **Today's Focus:** Priority tasks and deadlines
- **AI Insights:** Proactive recommendations and alerts
- **Quick Actions:** One-click access to common tasks
- **Recent Activity:** System and user action history

**Dashboard Sections:**
```javascript
DASHBOARD_SECTIONS = {
    'ai_assistant': 'Central conversational interface',
    'quick_stats': 'Key metrics at a glance',
    'todays_focus': 'Priority tasks and deadlines',
    'smart_insights': 'AI-generated recommendations',
    'quick_actions': 'Common task shortcuts',
    'recent_activity': 'System and user history'
}
```

### **5. Authentication & User Management**

**Component:** `Login.jsx`

**Authentication Features:**
- **Email-based Login:** Simplified user identification
- **Password Security:** Bcrypt hashing, strength validation
- **Google OAuth:** Single sign-on integration
- **JWT Tokens:** Secure session management
- **Password Recovery:** Email-based reset system

**User Roles & Permissions:**
```python
USER_ROLES = {
    'hr_admin': {
        'permissions': ['full_access', 'user_management', 'system_config'],
        'description': 'Complete platform access'
    },
    'hr_manager': {
        'permissions': ['employee_management', 'analytics_view', 'workflow_create'],
        'description': 'Standard HR management access'
    },
    'employee': {
        'permissions': ['self_service', 'basic_analytics'],
        'description': 'Limited self-service access'
    }
}
```

### **6. Subscription Management**

**Component:** `Subscription.jsx`

**Subscription Tiers:**
```python
SUBSCRIPTION_PLANS = {
    'free': {
        'price': 0,
        'employees': 10,
        'ai_queries': 100,
        'features': ['basic_analytics', 'employee_management']
    },
    'premium': {
        'price': 29,
        'employees': 100,
        'ai_queries': 1000,
        'features': ['advanced_analytics', 'workflow_automation', 'compliance_monitoring']
    },
    'enterprise': {
        'price': 99,
        'employees': 'unlimited',
        'ai_queries': 'unlimited',
        'features': ['all_features', 'custom_integrations', 'dedicated_support']
    }
}
```

---

## 🌐 **APAC Market Specialization**

### **Country Coverage**

**Tier 1 Countries (Full Support):**
- **Singapore:** MOM compliance, PDPA requirements
- **Australia:** Fair Work Act, privacy legislation
- **Malaysia:** Employment Act, PDPA compliance
- **Hong Kong:** Employment Ordinance, privacy laws

**Tier 2 Countries (Growing Support):**
- **Japan:** Labor Standards Act, privacy regulations
- **Indonesia:** Manpower Law, data protection
- **Thailand:** Labor Protection Act, PDPA
- **Philippines:** Labor Code, Data Privacy Act

**Tier 3 Countries (Basic Support):**
- **India:** Labor laws, IT Act compliance
- **Vietnam:** Labor Code, cybersecurity law
- **South Korea:** Labor Standards Act, PIPA
- **Taiwan:** Labor Standards Act, PDPA
- **New Zealand:** Employment Relations Act

### **Localization Features**

**Legal Compliance:**
- **Employment Contracts:** Country-specific templates
- **Policy Templates:** Local law compliance
- **Regulatory Updates:** Real-time law change monitoring
- **Audit Trails:** Compliance documentation

**Cultural Adaptation:**
- **Language Support:** English with local terminology
- **Business Practices:** Regional HR customs
- **Holiday Calendars:** Country-specific observances
- **Communication Styles:** Cultural sensitivity

---

## 🔄 **Workflow Management**

### **Performance Review Workflows**

**360-Degree Review Process:**
```python
PERFORMANCE_REVIEW_WORKFLOW = {
    'phases': [
        {
            'name': 'self_assessment',
            'duration': 7,
            'participants': ['employee'],
            'automation': 'form_generation'
        },
        {
            'name': 'peer_feedback',
            'duration': 10,
            'participants': ['selected_peers'],
            'automation': 'invitation_sending'
        },
        {
            'name': 'manager_review',
            'duration': 7,
            'participants': ['direct_manager'],
            'automation': 'data_compilation'
        },
        {
            'name': 'goal_setting',
            'duration': 5,
            'participants': ['employee', 'manager'],
            'automation': 'template_generation'
        }
    ],
    'total_duration': 30,
    'automation_level': 'high'
}
```

**Onboarding Workflows:**
```python
ONBOARDING_WORKFLOW = {
    'pre_arrival': [
        'welcome_email_sequence',
        'document_collection',
        'equipment_preparation',
        'access_provisioning'
    ],
    'first_week': [
        'orientation_session',
        'buddy_assignment',
        'initial_training',
        'manager_introduction'
    ],
    'first_month': [
        'role_specific_training',
        'team_integration',
        'goal_setting',
        'feedback_session'
    ],
    'first_quarter': [
        'performance_check',
        'development_planning',
        'culture_integration',
        'retention_assessment'
    ]
}
```

---

## 📊 **Data Models & Relationships**

### **Core Data Entities**

#### **User Model**
```python
class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    google_id = db.Column(db.String(255), unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    coins = db.Column(db.Integer, default=100)
    country_context = db.Column(db.String(100), default='Singapore')
    subscription_plan_id = db.Column(db.Integer, db.ForeignKey('subscription_plan.plan_id'))
    subscription_start_date = db.Column(db.Date)
    subscription_end_date = db.Column(db.Date)
```

#### **Employee Model**
```python
class Employee(db.Model):
    employee_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    # [Complete model definition as shown above]
```

#### **Subscription Plan Model**
```python
class SubscriptionPlan(db.Model):
    plan_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Decimal(10, 2), nullable=False)
    max_employees = db.Column(db.Integer)
    max_queries = db.Column(db.Integer)
    features = db.Column(db.JSON)
```

#### **Prompt History Model**
```python
class PromptHistory(db.Model):
    history_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    prompt = db.Column(db.Text, nullable=False)
    response = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    country_context = db.Column(db.String(100))
    ai_provider = db.Column(db.String(100))
    confidence_score = db.Column(db.Float)
```

### **Entity Relationships**

```
User (1) ←→ (N) Employee
User (N) ←→ (1) SubscriptionPlan
User (1) ←→ (N) PromptHistory
Employee (N) ←→ (1) Department
Employee (1) ←→ (N) PerformanceReview
Employee (1) ←→ (N) WorkflowInstance
```

---

## 🔌 **API Endpoints**

### **Authentication Endpoints**
```python
POST /api/auth/register    # User registration
POST /api/auth/login       # User authentication
POST /api/auth/google      # Google OAuth
POST /api/auth/logout      # Session termination
POST /api/auth/refresh     # Token refresh
```

### **Employee Management Endpoints**
```python
GET    /api/employees           # List employees
POST   /api/employees           # Create employee
GET    /api/employees/{id}      # Get employee details
PUT    /api/employees/{id}      # Update employee
DELETE /api/employees/{id}      # Delete employee
GET    /api/employees/analytics # Employee analytics
```

### **AI Assistant Endpoints**
```python
POST /api/hr-advisor/chat      # AI conversation
POST /api/hr-advisor/template  # Generate templates
GET  /api/history/prompts      # Query history
GET  /api/analytics/insights   # AI insights
```

### **Workflow Endpoints**
```python
GET    /api/workflows              # List workflows
POST   /api/workflows              # Create workflow
GET    /api/workflows/{id}         # Get workflow
PUT    /api/workflows/{id}         # Update workflow
POST   /api/workflows/{id}/execute # Execute workflow
```

### **Analytics Endpoints**
```python
GET /api/analytics/dashboard    # Dashboard metrics
GET /api/analytics/retention    # Retention analysis
GET /api/analytics/performance  # Performance metrics
GET /api/analytics/compliance   # Compliance status
GET /api/analytics/diversity    # Diversity metrics
```

---

## 🔒 **Security & Compliance**

### **Data Security**
- **Encryption:** AES-256 for data at rest
- **Transport Security:** TLS 1.3 for data in transit
- **Authentication:** JWT with secure signing
- **Authorization:** Role-based access control
- **Session Management:** Secure token handling

### **Privacy Compliance**
- **GDPR Compliance:** EU data protection requirements
- **PDPA Compliance:** Singapore/Malaysia privacy laws
- **Data Minimization:** Collect only necessary data
- **Right to Deletion:** User data removal capabilities
- **Audit Trails:** Complete action logging

### **AI Ethics & Governance**
- **Bias Monitoring:** Algorithmic fairness tracking
- **Transparency:** Explainable AI decisions
- **Human Oversight:** Critical decision validation
- **Data Quality:** Training data validation
- **Continuous Monitoring:** Performance and bias tracking

---

## 📈 **Performance & Scalability**

### **System Performance**
- **Response Time:** <2 seconds for AI queries
- **Uptime:** 99.9% availability target
- **Concurrent Users:** 1000+ simultaneous users
- **Database Performance:** Optimized queries and indexing
- **Caching:** Redis for frequently accessed data

### **Scalability Architecture**
- **Horizontal Scaling:** Load balancer with multiple instances
- **Database Scaling:** Read replicas and sharding
- **AI Provider Scaling:** Multiple provider load balancing
- **CDN Integration:** Global content delivery
- **Auto-scaling:** Dynamic resource allocation

### **Monitoring & Observability**
- **Application Monitoring:** Real-time performance tracking
- **Error Tracking:** Comprehensive error logging
- **User Analytics:** Usage pattern analysis
- **AI Performance:** Provider response time and accuracy
- **Business Metrics:** Feature adoption and user satisfaction

---

## 🚀 **Deployment & DevOps**

### **Deployment Architecture**
```
GitHub Repository
    ↓
Automatic CI/CD Pipeline
    ↓
┌─────────────────┬─────────────────┐
│   Frontend      │    Backend      │
│   (Vercel)      │   (Render)      │
│   - React App   │   - Flask API   │
│   - Static CDN  │   - Database    │
│   - Auto Deploy │   - Auto Deploy │
└─────────────────┴─────────────────┘
```

### **Environment Configuration**
```python
ENVIRONMENTS = {
    'development': {
        'database': 'sqlite:///dev.db',
        'debug': True,
        'ai_providers': 'free_tier_only'
    },
    'staging': {
        'database': 'postgresql://staging_db',
        'debug': False,
        'ai_providers': 'limited_paid'
    },
    'production': {
        'database': 'postgresql://prod_db',
        'debug': False,
        'ai_providers': 'full_access'
    }
}
```

### **Continuous Integration**
- **Automated Testing:** Unit, integration, and E2E tests
- **Code Quality:** Linting, formatting, and security scanning
- **Dependency Management:** Automated security updates
- **Performance Testing:** Load and stress testing
- **Deployment Automation:** Zero-downtime deployments

---

## 📚 **Documentation & Support**

### **Technical Documentation**
- **API Documentation:** OpenAPI/Swagger specifications
- **Developer Guide:** Setup and development instructions
- **Architecture Guide:** System design and patterns
- **Deployment Guide:** Production deployment procedures
- **Troubleshooting Guide:** Common issues and solutions

### **User Documentation**
- **User Manual:** Feature usage instructions
- **Quick Start Guide:** Getting started tutorial
- **Best Practices:** HR management recommendations
- **FAQ:** Frequently asked questions
- **Video Tutorials:** Step-by-step demonstrations

### **Support Channels**
- **In-app Help:** Contextual assistance
- **Knowledge Base:** Searchable documentation
- **Community Forum:** User discussion platform
- **Email Support:** Direct assistance channel
- **Live Chat:** Real-time support (premium plans)

---

## 🔄 **Future Roadmap**

### **Phase 1: Core Enhancement (Q1 2025)**
- **Advanced Analytics:** Predictive workforce modeling
- **Mobile App:** Native iOS/Android applications
- **Integration APIs:** Third-party HR system connections
- **Advanced Workflows:** Complex automation scenarios

### **Phase 2: Market Expansion (Q2 2025)**
- **Additional Countries:** India, Vietnam, South Korea
- **Language Support:** Local language interfaces
- **Regional Partnerships:** Local HR service providers
- **Compliance Automation:** Regulatory change monitoring

### **Phase 3: AI Enhancement (Q3 2025)**
- **Custom AI Models:** Company-specific training
- **Voice Interface:** Speech-to-text interaction
- **Computer Vision:** Document processing automation
- **Advanced Reasoning:** Complex decision support

### **Phase 4: Enterprise Features (Q4 2025)**
- **Multi-tenant Architecture:** Enterprise customer support
- **Advanced Security:** SOC2, ISO27001 compliance
- **Custom Integrations:** Enterprise system connections
- **White-label Solutions:** Partner platform offerings

---

## 📊 **Success Metrics**

### **User Engagement Metrics**
- **Daily Active Users:** Platform usage frequency
- **Feature Adoption:** Individual feature utilization
- **Session Duration:** User engagement depth
- **Query Volume:** AI assistant usage
- **User Satisfaction:** NPS and feedback scores

### **Business Metrics**
- **Customer Acquisition:** New user registration rate
- **Revenue Growth:** Subscription revenue trends
- **Churn Rate:** User retention metrics
- **Market Penetration:** APAC market share
- **Cost Efficiency:** AI provider cost optimization

### **Technical Metrics**
- **System Performance:** Response time and uptime
- **AI Accuracy:** Response quality and relevance
- **Error Rates:** System reliability metrics
- **Scalability:** Performance under load
- **Security:** Incident and vulnerability tracking

---

## 🏷️ **Version History**

| Version | Date | Changes | Author |
|---------| 1.1 | Sep 2025 | Automated feature updates and enhancements | Auto-update |
| 1.1 | Sep 2025 | Automated feature updates and enhancements | Auto-update |
|------| 1.1 | Sep 2025 | Automated feature updates and enhancements | Auto-update |
| 1.1 | Sep 2025 | Automated feature updates and enhancements | Auto-update |
|------| 1.1 | Sep 2025 | Automated feature updates and enhancements | Auto-update |
| 1.1 | Sep 2025 | Automated feature updates and enhancements | Auto-update |
---|------| 1.1 | Sep 2025 | Automated feature updates and enhancements | Auto-update |
| 1.1 | Sep 2025 | Automated feature updates and enhancements | Auto-update |
--|
| 1.0 | Dec 2024 | Initial functional specification | System |
| 1.1 | TBD | Feature updates and enhancements | Auto-update |

---

## 📝 **Document Maintenance**

**Auto-Update Triggers:**
- New feature implementation
- Agent system modifications
- API endpoint changes
- Database schema updates
- Configuration changes

**Update Process:**
1. **Change Detection:** Git commit analysis
2. **Content Generation:** AI-powered documentation update
3. **Version Control:** Automatic versioning
4. **Stakeholder Notification:** Change alerts
5. **Review Process:** Technical validation

**Maintenance Schedule:**
- **Real-time:** Critical changes and new features
- **Weekly:** Minor updates and improvements
- **Monthly:** Comprehensive review and optimization
- **Quarterly:** Major version updates and roadmap alignment

---

*This document is automatically maintained and updated as AnNi AI evolves. For the latest version, please refer to the GitHub repository.*



---

## 📚 **APPENDIX A: Technical Configuration & API Keys**

### **🔑 API Keys & Authentication**

#### **Multi-LLM Orchestration Providers**

| Provider | API Key | Usage Limit | Purpose | Status |
|----------|---------|-------------|---------|--------|
| **OpenRouter** | `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` | 50 requests/day (FREE) | DeepSeek R1/V3 models for complex reasoning | ✅ Active |
| **Groq** | `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` | 14,400 requests/day (FREE) | Llama 3.3 70B, Llama 3.1 8B for fast inference | ✅ Active |
| **OpenAI** | `your_openai_api_key_here` | Pay-per-use | GPT-4, GPT-3.5-turbo for premium features | ⏳ Pending |
| **Google** | `your_google_api_key_here` | Generous free tier | Gemini Pro/Flash for multimodal tasks | ⏳ Pending |
| **Anthropic** | `your_anthropic_api_key_here` | Pay-per-use | Claude-3 for safety-critical decisions | ⏳ Pending |

#### **Authentication & Security**

| Component | Key/Token | Purpose |
|-----------|-----------|---------|
| **Flask Secret Key** | `anni-ai-hr-made-simple-secret-key-2025` | Session management and CSRF protection |
| **JWT Secret Key** | `anni-ai-jwt-secret-key-hr-platform` | JSON Web Token signing and verification |
| **Google OAuth** | Client ID/Secret (configured separately) | Single Sign-On authentication |

### **🌐 Deployment URLs & Endpoints**

#### **Production Deployment**

| Service | URL | Status | Purpose |
|---------|-----|--------|---------|
| **Frontend (Vercel)** | `https://hr-advisor-app.vercel.app` | 🟢 Live | React application hosting |
| **Backend (Render)** | `https://hr-advisor-backend.onrender.com` | 🟢 Live | Flask API server |
| **Database** | SQLite (local to backend) | 🟢 Active | Employee and user data storage |

#### **API Endpoints**

| Endpoint | Method | Purpose | Authentication |
|----------|--------|---------|----------------|
| `/api/auth/login` | POST | User authentication | None |
| `/api/auth/register` | POST | User registration | None |
| `/api/auth/google` | POST | Google OAuth login | None |
| `/api/employees` | GET/POST/PUT/DELETE | Employee management | JWT Required |
| `/api/hr-advisor` | POST | AI-powered HR queries | JWT Required |
| `/api/analytics` | GET | HR analytics data | JWT Required |
| `/api/workflows` | GET/POST | Workflow automation | JWT Required |
| `/api/documents` | POST | Document generation | JWT Required |
| `/api/governance` | GET | AI governance metrics | JWT Required |

#### **Development URLs**

| Service | URL | Purpose |
|---------|-----|---------|
| **Local Frontend** | `http://localhost:5173` | Vite development server |
| **Local Backend** | `http://localhost:5000` | Flask development server |
| **Local Database** | `sqlite:///hr_advisor.db` | SQLite database file |

### **🛠️ Complete Technology Stack**

#### **Frontend Architecture**

| Technology | Version | Purpose | Configuration |
|------------|---------|---------|---------------|
| **React** | 18.2.0 | UI framework | Created with Vite template |
| **Vite** | 4.4.5 | Build tool and dev server | Hot reload, fast builds |
| **Tailwind CSS** | 3.3.0 | Utility-first styling | Custom color palette, responsive design |
| **Shadcn/UI** | Latest | Component library | Pre-built accessible components |
| **Lucide React** | Latest | Icon library | Consistent iconography |
| **Recharts** | 2.7.2 | Data visualization | HR analytics charts and graphs |
| **Axios** | 1.5.0 | HTTP client | API communication with backend |

**Frontend File Structure:**
```
frontend/
├── src/
│   ├── components/
│   │   ├── ui/           # Shadcn/UI components
│   │   ├── Login.jsx     # Authentication
│   │   ├── Dashboard.jsx # Main dashboard
│   │   ├── SimplifiedDashboard.jsx # UX-optimized dashboard
│   │   ├── ConversationalAI.jsx # AI chat interface
│   │   ├── EmployeeManagement.jsx # Employee CRUD
│   │   ├── EmployeeTable.jsx # Data table with sorting/search
│   │   ├── HRAnalyticsDashboard.jsx # Analytics visualization
│   │   ├── DailyTips.jsx # HR tips feature
│   │   └── Layout.jsx    # Common layout wrapper
│   ├── lib/
│   │   └── utils.js      # Utility functions
│   └── App.jsx           # Main application component
├── public/               # Static assets
└── package.json          # Dependencies and scripts
```

#### **Backend Architecture**

| Technology | Version | Purpose | Configuration |
|------------|---------|---------|---------------|
| **Flask** | 2.3.3 | Web framework | CORS enabled, JSON responses |
| **SQLAlchemy** | 2.0.21 | ORM and database toolkit | SQLite database, model definitions |
| **Flask-JWT-Extended** | 4.5.3 | JWT authentication | Token-based auth with refresh |
| **Flask-CORS** | 4.0.0 | Cross-origin requests | Allow all origins for development |
| **Bcrypt** | 4.0.1 | Password hashing | Secure password storage |
| **Requests** | 2.31.0 | HTTP client | External API calls |
| **Python-dotenv** | 1.0.0 | Environment variables | Configuration management |

**Backend File Structure:**
```
backend/
├── src/
│   ├── main.py                    # Flask application entry point
│   ├── llm_orchestrator.py       # Multi-LLM coordination
│   ├── ai_governance_agent.py    # AI usage governance
│   ├── workflow_automation_agent.py # Process automation
│   ├── document_generation_agent.py # Document creation
│   ├── predictive_analytics_agent.py # Workforce predictions
│   ├── proactive_compliance_agent.py # Compliance monitoring
│   ├── documentation_agent.py    # Auto-documentation
│   ├── documentation_scheduler.py # Scheduled doc updates
│   └── models/
│       └── employee.py           # Employee data model
├── requirements.txt              # Python dependencies
└── .env                         # Environment configuration
```

#### **Database Schema**

| Table | Purpose | Key Fields |
|-------|---------|------------|
| **users** | User authentication | id, email, password_hash, role, created_at |
| **employees** | Employee records | employee_id, first_name, last_name, email, position, department, hire_date, salary, country, performance_rating, engagement_score |
| **ai_usage_logs** | AI governance tracking | log_id, user_id, operation_type, provider_used, query_hash, response_time, confidence_score |
| **workflows** | Process automation | workflow_id, name, type, status, created_by, steps, automation_level |
| **documents** | Generated documents | doc_id, type, employee_id, content, created_at, version |

### **🤖 AI Provider Integration Details**

#### **Multi-LLM Orchestration Strategy**

| Provider | Models Used | Specialization | Request Routing Logic |
|----------|-------------|----------------|----------------------|
| **DeepSeek (OpenRouter)** | R1, V3 | Complex reasoning, legal analysis | Legal queries, policy interpretation |
| **Groq** | Llama 3.3 70B, Llama 3.1 8B | Fast inference, general HR | Quick responses, employee queries |
| **Together AI** | Llama 3.2 11B | Unlimited free tier | High-volume processing |
| **OpenAI** | GPT-4, GPT-3.5-turbo | Premium quality | Critical decisions, complex analysis |
| **Google** | Gemini Pro/Flash | Multimodal, document analysis | Document processing, image analysis |
| **Anthropic** | Claude-3 Sonnet/Haiku | Safety-critical decisions | Compliance, sensitive HR matters |

#### **Provider Selection Algorithm**

```python
def select_ai_provider(query_type, complexity, urgency, user_tier):
    if query_type == "legal_compliance":
        return "deepseek"  # Best reasoning capabilities
    elif urgency == "high" and complexity == "low":
        return "groq"      # Fastest response time
    elif user_tier == "premium":
        return "openai"    # Highest quality
    elif query_type == "document_analysis":
        return "google"    # Multimodal capabilities
    else:
        return "together"  # Free unlimited usage
```

### **🔄 Workflow Automation Configuration**

#### **Automated Processes**

| Workflow Type | Trigger | Steps | Automation Level |
|---------------|---------|-------|------------------|
| **Employee Onboarding** | New hire created | Welcome email → Document collection → Training schedule → Buddy assignment | 90% automated |
| **Performance Review** | Quarterly schedule | Self-assessment → Peer feedback → Manager review → Goal setting | 75% automated |
| **Compliance Audit** | Policy changes | Data collection → Gap analysis → Risk assessment → Action plan | 60% automated |
| **Offboarding** | Employee termination | Access revocation → Document collection → Exit interview → Final pay | 80% automated |

#### **Document Generation Templates**

| Document Type | Template Source | Customization Fields | Legal Compliance |
|---------------|----------------|---------------------|------------------|
| **Employment Contract** | Country-specific templates | Name, position, salary, start date, benefits | ✅ 13 countries |
| **Performance Review** | Standardized forms | Goals, ratings, feedback, development plans | ✅ Best practices |
| **Policy Documents** | Legal requirement templates | Company info, local laws, effective dates | ✅ Regulatory compliance |
| **Training Materials** | Role-based templates | Position requirements, skills, procedures | ✅ Industry standards |

### **📊 Analytics & Monitoring Configuration**

#### **HR Analytics Metrics**

| Category | Metrics Tracked | Data Sources | Update Frequency |
|----------|----------------|--------------|------------------|
| **Workforce Overview** | Headcount, growth trends, demographics | Employee database | Real-time |
| **Performance Analytics** | Ratings distribution, top performers, improvement areas | Performance reviews | Monthly |
| **Retention & Engagement** | Turnover rates, retention risk, engagement scores | Employee surveys, exit data | Weekly |
| **Compliance Monitoring** | Policy adherence, training completion, audit readiness | Workflow logs, training records | Daily |

#### **AI Governance Metrics**

| Metric | Purpose | Tracking Method | Alert Thresholds |
|--------|---------|----------------|------------------|
| **Response Accuracy** | Quality assurance | Human validation feedback | <85% accuracy |
| **Bias Detection** | Fairness monitoring | Demographic analysis of recommendations | Bias score >0.3 |
| **System Reliability** | Uptime monitoring | Error rates, response times | >5% error rate |
| **Usage Patterns** | Adoption tracking | Query logs, user engagement | Unusual spikes |

### **🔐 Security & Compliance Configuration**

#### **Data Protection Measures**

| Component | Security Method | Implementation |
|-----------|----------------|----------------|
| **Password Storage** | Bcrypt hashing | Salt rounds: 12 |
| **API Authentication** | JWT tokens | 24-hour expiry, refresh tokens |
| **Database Encryption** | SQLite encryption | File-level encryption |
| **API Communication** | HTTPS/TLS | SSL certificates, secure headers |
| **Data Anonymization** | PII masking | Sensitive data hashing |

#### **Compliance Standards**

| Regulation | Coverage | Implementation Status |
|------------|----------|----------------------|
| **GDPR** | EU data protection | ✅ Data consent, right to deletion |
| **PDPA** | Singapore/Malaysia privacy | ✅ Data minimization, consent |
| **CCPA** | California privacy | ✅ Data transparency, opt-out |
| **SOX** | Financial compliance | ⏳ Audit trails, data integrity |
| **ISO 27001** | Information security | ⏳ Security management system |

### **🚀 Deployment & DevOps Configuration**

#### **CI/CD Pipeline**

| Stage | Tool | Configuration | Trigger |
|-------|-----|---------------|---------|
| **Source Control** | GitHub | Private repository | Code commits |
| **Frontend Build** | Vercel | Automatic deployment | Main branch push |
| **Backend Deploy** | Render | Docker container | Main branch push |
| **Database Migration** | SQLAlchemy | Automatic schema updates | Model changes |
| **Monitoring** | Built-in logging | Error tracking, performance metrics | Continuous |

#### **Environment Variables**

| Variable | Purpose | Example Value |
|----------|---------|---------------|
| `OPENROUTER_API_KEY` | DeepSeek model access | `sk-or-v1-...` |
| `GROQ_API_KEY` | Llama model access | `gsk_...` |
| `SECRET_KEY` | Flask session security | `anni-ai-hr-...` |
| `JWT_SECRET_KEY` | Token signing | `anni-ai-jwt-...` |
| `SQLALCHEMY_DATABASE_URI` | Database connection | `sqlite:///hr_advisor.db` |

### **📈 Performance & Scaling Configuration**

#### **Current Capacity**

| Component | Current Limit | Scaling Strategy |
|-----------|---------------|------------------|
| **Frontend** | Unlimited (Vercel) | Global CDN, automatic scaling |
| **Backend** | 512MB RAM (Render) | Horizontal scaling, load balancing |
| **Database** | SQLite file | Migration to PostgreSQL for scale |
| **AI Providers** | 14,400 requests/day | Multiple provider fallback |

#### **Monitoring & Alerts**

| Metric | Threshold | Alert Method |
|--------|-----------|--------------|
| **Response Time** | >2 seconds | Email notification |
| **Error Rate** | >5% | Slack alert |
| **API Quota** | >80% usage | Dashboard warning |
| **Database Size** | >100MB | Migration recommendation |

### **🔧 Development & Maintenance**

#### **Local Development Setup**

```bash
# Frontend setup
cd frontend
npm install
npm run dev  # Starts on http://localhost:5173

# Backend setup
cd backend
pip install -r requirements.txt
python src/main.py  # Starts on http://localhost:5000
```

#### **Automated Documentation System**

| Component | Purpose | Schedule |
|-----------|---------|----------|
| **Documentation Agent** | Auto-update functional spec | On code changes |
| **Documentation Scheduler** | Scheduled updates | Every 30 minutes |
| **Backup System** | Version control | Before each update |

#### **Testing Strategy**

| Test Type | Coverage | Tools |
|-----------|----------|-------|
| **Unit Tests** | Individual functions | pytest (backend), Jest (frontend) |
| **Integration Tests** | API endpoints | Postman collections |
| **E2E Tests** | User workflows | Playwright |
| **Performance Tests** | Load testing | Artillery.js |

---

## 📚 **APPENDIX B: Version History & Change Log**

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.1 | Sep 2025 | Automated feature updates and enhancements | Auto-update |
| 1.0 | Dec 2024 | Initial comprehensive specification | Development Team |

---

## 📚 **APPENDIX C: Support & Maintenance**

### **Support Contacts**

| Role | Contact | Responsibility |
|------|---------|----------------|
| **Technical Lead** | development@anni-ai.com | Architecture, API issues |
| **Product Manager** | product@anni-ai.com | Feature requests, roadmap |
| **DevOps** | devops@anni-ai.com | Deployment, infrastructure |
| **Support** | support@anni-ai.com | User issues, documentation |

### **Maintenance Schedule**

| Task | Frequency | Next Due |
|------|-----------|----------|
| **Security Updates** | Monthly | Next month |
| **Dependency Updates** | Quarterly | Q1 2025 |
| **Performance Review** | Bi-annually | H1 2025 |
| **Architecture Review** | Annually | 2025 |

---

**Document End**

*This functional specification is automatically maintained by the AnNi AI Documentation Agent and updated whenever code changes are detected.*

