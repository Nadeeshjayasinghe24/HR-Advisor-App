# AnNi AI - Documentation Automation Setup Guide

This guide explains how to set up and use the automated documentation system for AnNi AI platform.

## 🤖 **System Overview**

The automated documentation system consists of two main components:

1. **Documentation Agent** (`documentation_agent.py`) - Monitors code changes and updates functional specification
2. **Documentation Scheduler** (`documentation_scheduler.py`) - Runs the agent at regular intervals

## 📋 **Features**

### **Automated Monitoring**
- Monitors Git repository for changes
- Categorizes changes by type (agent, feature, API, model, UI, config)
- Analyzes commit messages and changed files
- Determines documentation update requirements

### **Smart Updates**
- Updates functional specification document automatically
- Maintains version history and timestamps
- Creates backup files before updates
- Applies changes based on priority (high, medium, low)

### **Flexible Scheduling**
- Immediate updates on demand
- Scheduled updates at configurable intervals
- Error handling and recovery
- Comprehensive logging

## 🚀 **Quick Start**

### **1. Immediate Update**
Run a single documentation update immediately:

```bash
cd /home/ubuntu/hr_advisor_app/backend/src
python3.11 documentation_scheduler.py --mode immediate
```

### **2. Scheduled Updates**
Run continuous updates every 30 minutes:

```bash
cd /home/ubuntu/hr_advisor_app/backend/src
python3.11 documentation_scheduler.py --mode scheduled --interval 30
```

### **3. Check Status**
View scheduler status and statistics:

```bash
cd /home/ubuntu/hr_advisor_app/backend/src
python3.11 documentation_scheduler.py --status
```

## ⚙️ **Configuration Options**

### **Command Line Arguments**

| Argument | Description | Default | Options |
|----------|-------------|---------|---------|
| `--mode` | Run mode | `immediate` | `immediate`, `scheduled` |
| `--interval` | Update interval (minutes) | `30` | Any positive integer |
| `--status` | Show status and exit | `false` | Flag |

### **Environment Variables**

The system uses the following paths and configurations:

- **Project Root:** `/home/ubuntu/hr_advisor_app`
- **Specification File:** `FUNCTIONAL_SPECIFICATION.md`
- **Log File:** `documentation_updates.log`
- **Backup Location:** Same directory as specification file

## 📊 **Monitoring & Logging**

### **Log File Location**
```
/home/ubuntu/hr_advisor_app/documentation_updates.log
```

### **Log Levels**
- **INFO:** Normal operations, successful updates
- **ERROR:** Failed updates, system errors
- **WARNING:** Non-critical issues

### **Sample Log Output**
```
2025-09-13 14:30:00,123 - DocumentationScheduler - INFO - Starting documentation update cycle
2025-09-13 14:30:01,456 - DocumentationScheduler - INFO - Processing 2 changes
2025-09-13 14:30:02,789 - DocumentationScheduler - INFO - Documentation updated successfully: 2 updates applied
2025-09-13 14:30:02,790 - DocumentationScheduler - INFO - Update cycle completed: 2 updates in 2.67s
```

## 🔄 **Change Detection**

### **Monitored File Patterns**
- `backend/src/*.py` - Backend Python files
- `frontend/src/components/*.jsx` - React components
- `backend/src/models/*.py` - Database models
- `*.md` - Markdown documentation
- `package.json` - Frontend dependencies
- `requirements.txt` - Backend dependencies

### **Change Categories**

| Category | Trigger | Impact | Example |
|----------|---------|--------|---------|
| **Agent** | Files with 'agent' in name/path | High | New AI agent implementation |
| **Feature** | Commit messages with 'add', 'implement', 'create' | High | New platform feature |
| **API** | Changes to `main.py` or API files | Medium | Endpoint modifications |
| **Model** | Changes to model files | Medium | Database schema updates |
| **UI** | Changes to `.jsx` files | Low | Component updates |
| **Config** | Changes to config files | Low | Dependency updates |

## 🛠️ **Advanced Usage**

### **Running as Background Service**

To run the scheduler as a background service:

```bash
# Start in background
nohup python3.11 documentation_scheduler.py --mode scheduled --interval 30 > /dev/null 2>&1 &

# Check if running
ps aux | grep documentation_scheduler

# Stop background process
pkill -f documentation_scheduler.py
```

### **Cron Job Setup**

To run updates via cron (every hour):

```bash
# Edit crontab
crontab -e

# Add this line for hourly updates
0 * * * * cd /home/ubuntu/hr_advisor_app/backend/src && python3.11 documentation_scheduler.py --mode immediate >> /home/ubuntu/hr_advisor_app/cron_updates.log 2>&1
```

### **Custom Integration**

The documentation agent can be integrated into other systems:

```python
from documentation_agent import DocumentationAgent

# Initialize agent
agent = DocumentationAgent("/path/to/project")

# Run single update
import asyncio
result = asyncio.run(agent.monitor_changes())

if result['requires_update']:
    update_result = asyncio.run(agent.update_documentation(result['changes']))
    print(f"Updates applied: {update_result['updates_applied']}")
```

## 🔧 **Troubleshooting**

### **Common Issues**

#### **"Git command failed" Error**
- Ensure you're in a Git repository
- Check Git is installed and accessible
- Verify repository has commit history

#### **"Specification file not found" Error**
- Ensure `FUNCTIONAL_SPECIFICATION.md` exists in project root
- Check file permissions are readable/writable
- Verify project root path is correct

#### **"No changes detected" Message**
- This is normal when no recent commits exist
- Check Git log to verify recent activity
- Adjust time window if needed (currently 1 hour)

### **Debug Mode**

For detailed debugging, modify the logging level:

```python
# In documentation_scheduler.py, change:
logging.basicConfig(level=logging.DEBUG)
```

### **Manual Testing**

Test the documentation agent directly:

```python
cd /home/ubuntu/hr_advisor_app/backend/src
python3.11 -c "
import asyncio
from documentation_agent import DocumentationAgent

agent = DocumentationAgent()
result = asyncio.run(agent.monitor_changes())
print('Changes detected:', result)
"
```

## 📈 **Performance Considerations**

### **Resource Usage**
- **CPU:** Low impact, runs briefly every interval
- **Memory:** Minimal, processes text files only
- **Disk:** Creates backup files, monitor disk space
- **Network:** None (local Git operations only)

### **Optimization Tips**
- Increase interval for less frequent updates
- Monitor log file size and rotate if needed
- Use immediate mode for development, scheduled for production
- Consider running during off-peak hours for large repositories

## 🔐 **Security Considerations**

### **File Permissions**
- Ensure documentation files are writable by the user
- Protect log files from unauthorized access
- Use appropriate file permissions for backup files

### **Git Repository Access**
- System requires read access to Git repository
- No remote Git operations are performed
- All operations are local file system based

## 📚 **Integration with Development Workflow**

### **Pre-commit Hooks**
Add to `.git/hooks/pre-commit`:

```bash
#!/bin/bash
cd /home/ubuntu/hr_advisor_app/backend/src
python3.11 documentation_scheduler.py --mode immediate
```

### **CI/CD Integration**
Add to deployment pipeline:

```yaml
# Example GitHub Actions step
- name: Update Documentation
  run: |
    cd backend/src
    python3.11 documentation_scheduler.py --mode immediate
    git add FUNCTIONAL_SPECIFICATION.md
    git commit -m "Auto-update documentation" || true
```

## 📞 **Support**

For issues with the documentation automation system:

1. Check the log file for error details
2. Verify all dependencies are installed
3. Test with immediate mode first
4. Review this guide for configuration options

The system is designed to be robust and self-recovering, with comprehensive error handling and logging to help diagnose any issues.

