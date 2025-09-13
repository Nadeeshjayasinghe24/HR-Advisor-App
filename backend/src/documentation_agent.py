"""
AnNi AI - Documentation Automation Agent

This agent automatically updates the functional specification document
whenever new features are added or existing features are modified.
"""

import os
import json
import asyncio
from datetime import datetime
from typing import Dict, List, Any, Optional
import subprocess
import re
from pathlib import Path

class DocumentationAgent:
    """
    Automated documentation maintenance agent for AnNi AI platform.
    
    Monitors code changes and automatically updates functional specification
    to keep documentation current with platform capabilities.
    """
    
    def __init__(self, project_root: str = "/home/ubuntu/hr_advisor_app"):
        self.project_root = Path(project_root)
        self.spec_file = self.project_root / "FUNCTIONAL_SPECIFICATION.md"
        self.last_update = datetime.now()
        self.version = "1.0"
        
        # File patterns to monitor for changes
        self.monitored_patterns = [
            "backend/src/*.py",
            "frontend/src/components/*.jsx",
            "backend/src/models/*.py",
            "*.md",
            "package.json",
            "requirements.txt"
        ]
        
        # Change categories for documentation updates
        self.change_categories = {
            'agent': 'Agent system modifications',
            'feature': 'New feature implementation',
            'api': 'API endpoint changes',
            'model': 'Database schema updates',
            'config': 'Configuration changes',
            'ui': 'User interface updates'
        }
    
    async def monitor_changes(self) -> Dict[str, Any]:
        """
        Monitor Git repository for changes that require documentation updates.
        
        Returns:
            Dict containing change information and update requirements
        """
        try:
            # Get recent commits
            result = subprocess.run(
                ['git', 'log', '--oneline', '--since="1 hour ago"'],
                cwd=self.project_root,
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                return {'status': 'error', 'message': 'Git command failed'}
            
            commits = result.stdout.strip().split('\n') if result.stdout.strip() else []
            
            if not commits:
                return {'status': 'no_changes', 'commits': []}
            
            # Analyze commits for documentation-relevant changes
            changes = await self.analyze_commits(commits)
            
            return {
                'status': 'changes_detected',
                'commits': commits,
                'changes': changes,
                'requires_update': len(changes) > 0
            }
            
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    async def analyze_commits(self, commits: List[str]) -> List[Dict[str, Any]]:
        """
        Analyze commits to identify changes requiring documentation updates.
        
        Args:
            commits: List of commit messages
            
        Returns:
            List of change descriptions with categories
        """
        changes = []
        
        for commit in commits:
            if not commit.strip():
                continue
                
            commit_hash, message = commit.split(' ', 1)
            
            # Get changed files for this commit
            result = subprocess.run(
                ['git', 'show', '--name-only', '--format=', commit_hash],
                cwd=self.project_root,
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                continue
                
            changed_files = result.stdout.strip().split('\n')
            
            # Categorize changes
            change_info = await self.categorize_changes(message, changed_files)
            
            if change_info:
                changes.append({
                    'commit': commit_hash,
                    'message': message,
                    'files': changed_files,
                    'category': change_info['category'],
                    'description': change_info['description'],
                    'impact': change_info['impact']
                })
        
        return changes
    
    async def categorize_changes(self, message: str, files: List[str]) -> Optional[Dict[str, Any]]:
        """
        Categorize changes based on commit message and changed files.
        
        Args:
            message: Commit message
            files: List of changed files
            
        Returns:
            Change categorization information
        """
        message_lower = message.lower()
        
        # Agent system changes
        if any('agent' in f for f in files) or 'agent' in message_lower:
            return {
                'category': 'agent',
                'description': f'Agent system update: {message}',
                'impact': 'high'
            }
        
        # New feature implementation
        if any(keyword in message_lower for keyword in ['add', 'implement', 'create', 'new']):
            return {
                'category': 'feature',
                'description': f'New feature: {message}',
                'impact': 'high'
            }
        
        # API changes
        if any('main.py' in f or 'api' in f for f in files):
            return {
                'category': 'api',
                'description': f'API modification: {message}',
                'impact': 'medium'
            }
        
        # Database model changes
        if any('models' in f or 'model' in f for f in files):
            return {
                'category': 'model',
                'description': f'Data model update: {message}',
                'impact': 'medium'
            }
        
        # UI/Component changes
        if any('.jsx' in f or 'component' in f for f in files):
            return {
                'category': 'ui',
                'description': f'UI component update: {message}',
                'impact': 'low'
            }
        
        # Configuration changes
        if any(f in ['package.json', 'requirements.txt', '.env'] for f in files):
            return {
                'category': 'config',
                'description': f'Configuration update: {message}',
                'impact': 'low'
            }
        
        return None
    
    async def update_documentation(self, changes: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Update functional specification based on detected changes.
        
        Args:
            changes: List of change descriptions
            
        Returns:
            Update status and details
        """
        try:
            # Read current specification
            if not self.spec_file.exists():
                return {'status': 'error', 'message': 'Specification file not found'}
            
            with open(self.spec_file, 'r', encoding='utf-8') as f:
                current_content = f.read()
            
            # Generate updates based on changes
            updates = await self.generate_updates(changes, current_content)
            
            if not updates:
                return {'status': 'no_updates', 'message': 'No documentation updates required'}
            
            # Apply updates to specification
            updated_content = await self.apply_updates(current_content, updates)
            
            # Update version and timestamp
            updated_content = await self.update_metadata(updated_content)
            
            # Write updated specification
            with open(self.spec_file, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            
            # Create backup
            backup_file = self.spec_file.parent / f"FUNCTIONAL_SPECIFICATION_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
            with open(backup_file, 'w', encoding='utf-8') as f:
                f.write(current_content)
            
            return {
                'status': 'success',
                'updates_applied': len(updates),
                'backup_created': str(backup_file),
                'changes_processed': len(changes)
            }
            
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    async def generate_updates(self, changes: List[Dict[str, Any]], current_content: str) -> List[Dict[str, Any]]:
        """
        Generate documentation updates based on code changes.
        
        Args:
            changes: List of detected changes
            current_content: Current specification content
            
        Returns:
            List of documentation updates to apply
        """
        updates = []
        
        for change in changes:
            category = change['category']
            description = change['description']
            impact = change['impact']
            
            # Generate update based on category
            if category == 'agent':
                update = await self.generate_agent_update(change, current_content)
            elif category == 'feature':
                update = await self.generate_feature_update(change, current_content)
            elif category == 'api':
                update = await self.generate_api_update(change, current_content)
            elif category == 'model':
                update = await self.generate_model_update(change, current_content)
            elif category == 'ui':
                update = await self.generate_ui_update(change, current_content)
            elif category == 'config':
                update = await self.generate_config_update(change, current_content)
            else:
                continue
            
            if update:
                updates.append(update)
        
        return updates
    
    async def generate_agent_update(self, change: Dict[str, Any], content: str) -> Optional[Dict[str, Any]]:
        """Generate update for agent system changes."""
        return {
            'section': 'Agent System Architecture',
            'type': 'addition',
            'content': f"\n### Recent Update: {change['description']}\n**Date:** {datetime.now().strftime('%Y-%m-%d')}\n**Impact:** {change['impact'].title()}\n\n",
            'priority': 'high'
        }
    
    async def generate_feature_update(self, change: Dict[str, Any], content: str) -> Optional[Dict[str, Any]]:
        """Generate update for new feature additions."""
        return {
            'section': 'Core Features',
            'type': 'addition',
            'content': f"\n### New Feature: {change['description']}\n**Added:** {datetime.now().strftime('%Y-%m-%d')}\n**Status:** Recently implemented\n\n",
            'priority': 'high'
        }
    
    async def generate_api_update(self, change: Dict[str, Any], content: str) -> Optional[Dict[str, Any]]:
        """Generate update for API changes."""
        return {
            'section': 'API Endpoints',
            'type': 'modification',
            'content': f"\n<!-- API Update: {change['description']} - {datetime.now().strftime('%Y-%m-%d')} -->\n",
            'priority': 'medium'
        }
    
    async def generate_model_update(self, change: Dict[str, Any], content: str) -> Optional[Dict[str, Any]]:
        """Generate update for data model changes."""
        return {
            'section': 'Data Models & Relationships',
            'type': 'modification',
            'content': f"\n<!-- Model Update: {change['description']} - {datetime.now().strftime('%Y-%m-%d')} -->\n",
            'priority': 'medium'
        }
    
    async def generate_ui_update(self, change: Dict[str, Any], content: str) -> Optional[Dict[str, Any]]:
        """Generate update for UI component changes."""
        return {
            'section': 'Core Features',
            'type': 'modification',
            'content': f"\n<!-- UI Update: {change['description']} - {datetime.now().strftime('%Y-%m-%d')} -->\n",
            'priority': 'low'
        }
    
    async def generate_config_update(self, change: Dict[str, Any], content: str) -> Optional[Dict[str, Any]]:
        """Generate update for configuration changes."""
        return {
            'section': 'System Architecture',
            'type': 'modification',
            'content': f"\n<!-- Config Update: {change['description']} - {datetime.now().strftime('%Y-%m-%d')} -->\n",
            'priority': 'low'
        }
    
    async def apply_updates(self, content: str, updates: List[Dict[str, Any]]) -> str:
        """
        Apply generated updates to specification content.
        
        Args:
            content: Current specification content
            updates: List of updates to apply
            
        Returns:
            Updated specification content
        """
        updated_content = content
        
        # Sort updates by priority
        priority_order = {'high': 0, 'medium': 1, 'low': 2}
        updates.sort(key=lambda x: priority_order.get(x['priority'], 3))
        
        for update in updates:
            section = update['section']
            update_type = update['type']
            update_content = update['content']
            
            # Find section in content
            section_pattern = f"## (🎯|🤖|🏗️|📊|🔌) \*\*{re.escape(section)}\*\*"
            section_match = re.search(section_pattern, updated_content)
            
            if section_match:
                # Insert update after section header
                insert_pos = section_match.end()
                updated_content = (
                    updated_content[:insert_pos] + 
                    update_content + 
                    updated_content[insert_pos:]
                )
            else:
                # Add to end of document if section not found
                updated_content += f"\n\n## 📝 **Recent Updates**\n{update_content}"
        
        return updated_content
    
    async def update_metadata(self, content: str) -> str:
        """
        Update version and timestamp metadata in specification.
        
        Args:
            content: Specification content
            
        Returns:
            Content with updated metadata
        """
        # Update version
        version_parts = self.version.split('.')
        version_parts[-1] = str(int(version_parts[-1]) + 1)
        new_version = '.'.join(version_parts)
        
        # Update version in content
        content = re.sub(
            r'\*\*Version:\*\* \d+\.\d+',
            f'**Version:** {new_version}',
            content
        )
        
        # Update last updated date
        content = re.sub(
            r'\*\*Last Updated:\*\* [A-Za-z]+ \d{4}',
            f'**Last Updated:** {datetime.now().strftime("%B %Y")}',
            content
        )
        
        # Update version history
        version_entry = f"| {new_version} | {datetime.now().strftime('%b %Y')} | Automated feature updates and enhancements | Auto-update |"
        
        # Find version history table and add entry
        version_pattern = r'(\| Version \| Date \| Changes \| Author \|\n\|---------|------|---------|--------\|\n)'
        if re.search(version_pattern, content):
            content = re.sub(
                version_pattern,
                f'\\1{version_entry}\n',
                content
            )
        
        self.version = new_version
        return content
    
    async def run_continuous_monitoring(self, interval_minutes: int = 60):
        """
        Run continuous monitoring for documentation updates.
        
        Args:
            interval_minutes: Monitoring interval in minutes
        """
        print(f"Starting AnNi AI Documentation Agent - Monitoring every {interval_minutes} minutes")
        
        while True:
            try:
                # Check for changes
                change_info = await self.monitor_changes()
                
                if change_info['status'] == 'changes_detected' and change_info['requires_update']:
                    print(f"Changes detected: {len(change_info['changes'])} updates required")
                    
                    # Update documentation
                    update_result = await self.update_documentation(change_info['changes'])
                    
                    if update_result['status'] == 'success':
                        print(f"Documentation updated successfully: {update_result['updates_applied']} updates applied")
                    else:
                        print(f"Documentation update failed: {update_result['message']}")
                
                elif change_info['status'] == 'no_changes':
                    print("No changes detected - documentation up to date")
                
                else:
                    print(f"Monitoring status: {change_info['status']}")
                
                # Wait for next check
                await asyncio.sleep(interval_minutes * 60)
                
            except Exception as e:
                print(f"Documentation agent error: {str(e)}")
                await asyncio.sleep(300)  # Wait 5 minutes on error
    
    async def manual_update(self) -> Dict[str, Any]:
        """
        Manually trigger documentation update.
        
        Returns:
            Update status and results
        """
        print("Manual documentation update triggered")
        
        # Check for changes
        change_info = await self.monitor_changes()
        
        if change_info['status'] == 'changes_detected':
            # Update documentation
            update_result = await self.update_documentation(change_info['changes'])
            return update_result
        else:
            return {'status': 'no_changes', 'message': 'No updates required'}

# Global documentation agent instance
documentation_agent = DocumentationAgent()

async def start_documentation_monitoring():
    """Start the documentation monitoring service."""
    await documentation_agent.run_continuous_monitoring(interval_minutes=60)

async def trigger_manual_update():
    """Trigger a manual documentation update."""
    return await documentation_agent.manual_update()

if __name__ == "__main__":
    # Run documentation agent
    asyncio.run(start_documentation_monitoring())

