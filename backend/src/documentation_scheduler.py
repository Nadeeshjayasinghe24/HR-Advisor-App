#!/usr/bin/env python3
"""
AnNi AI - Documentation Scheduler

Automated scheduler for running documentation updates at regular intervals.
This script can be run as a cron job or background service to keep
documentation current with code changes.
"""

import asyncio
import sys
import os
import time
import logging
from datetime import datetime, timedelta
from pathlib import Path

# Add the backend src directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from documentation_agent import DocumentationAgent

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/home/ubuntu/hr_advisor_app/documentation_updates.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('DocumentationScheduler')

class DocumentationScheduler:
    """
    Scheduler for automated documentation updates.
    
    Runs the documentation agent at specified intervals and handles
    error recovery, logging, and status reporting.
    """
    
    def __init__(self, project_root: str = "/home/ubuntu/hr_advisor_app"):
        self.project_root = Path(project_root)
        self.agent = DocumentationAgent(project_root)
        self.last_run = None
        self.run_count = 0
        self.error_count = 0
        
    async def run_single_update(self) -> dict:
        """
        Run a single documentation update cycle.
        
        Returns:
            Dict with update results and status
        """
        try:
            logger.info("Starting documentation update cycle")
            start_time = datetime.now()
            
            # Monitor for changes
            change_info = await self.agent.monitor_changes()
            
            if change_info['status'] == 'error':
                logger.error(f"Error monitoring changes: {change_info['message']}")
                self.error_count += 1
                return {
                    'status': 'error',
                    'message': change_info['message'],
                    'duration': (datetime.now() - start_time).total_seconds()
                }
            
            if change_info['status'] == 'no_changes':
                logger.info("No changes detected, skipping update")
                return {
                    'status': 'no_changes',
                    'message': 'No documentation updates required',
                    'duration': (datetime.now() - start_time).total_seconds()
                }
            
            # Process changes
            changes = change_info['changes']
            logger.info(f"Processing {len(changes)} changes")
            
            # Update documentation
            update_result = await self.agent.update_documentation(changes)
            
            if update_result['status'] == 'success':
                logger.info(f"Documentation updated successfully: {update_result['updates_applied']} updates applied")
                self.run_count += 1
                self.last_run = datetime.now()
                
                return {
                    'status': 'success',
                    'updates_applied': update_result['updates_applied'],
                    'changes_processed': len(changes),
                    'backup_created': update_result.get('backup_created'),
                    'duration': (datetime.now() - start_time).total_seconds()
                }
            else:
                logger.error(f"Documentation update failed: {update_result['message']}")
                self.error_count += 1
                return {
                    'status': 'error',
                    'message': update_result['message'],
                    'duration': (datetime.now() - start_time).total_seconds()
                }
                
        except Exception as e:
            logger.error(f"Unexpected error in documentation update: {str(e)}")
            self.error_count += 1
            return {
                'status': 'error',
                'message': str(e),
                'duration': (datetime.now() - start_time).total_seconds() if 'start_time' in locals() else 0
            }
    
    async def run_scheduled_updates(self, interval_minutes: int = 30):
        """
        Run scheduled documentation updates at specified intervals.
        
        Args:
            interval_minutes: Update interval in minutes
        """
        logger.info(f"Starting scheduled documentation updates every {interval_minutes} minutes")
        
        while True:
            try:
                # Run update cycle
                result = await self.run_single_update()
                
                # Log results
                if result['status'] == 'success':
                    logger.info(f"Update cycle completed: {result['updates_applied']} updates in {result['duration']:.2f}s")
                elif result['status'] == 'no_changes':
                    logger.info(f"Update cycle completed: no changes in {result['duration']:.2f}s")
                else:
                    logger.error(f"Update cycle failed: {result['message']}")
                
                # Wait for next cycle
                await asyncio.sleep(interval_minutes * 60)
                
            except KeyboardInterrupt:
                logger.info("Scheduler stopped by user")
                break
            except Exception as e:
                logger.error(f"Scheduler error: {str(e)}")
                # Wait before retrying
                await asyncio.sleep(60)
    
    def get_status(self) -> dict:
        """
        Get current scheduler status.
        
        Returns:
            Dict with scheduler statistics and status
        """
        return {
            'last_run': self.last_run.isoformat() if self.last_run else None,
            'run_count': self.run_count,
            'error_count': self.error_count,
            'uptime': datetime.now().isoformat(),
            'project_root': str(self.project_root),
            'log_file': '/home/ubuntu/hr_advisor_app/documentation_updates.log'
        }
    
    async def run_immediate_update(self):
        """
        Run an immediate documentation update (for manual triggering).
        """
        logger.info("Running immediate documentation update")
        result = await self.run_single_update()
        
        print(f"\n=== Documentation Update Results ===")
        print(f"Status: {result['status']}")
        print(f"Duration: {result['duration']:.2f} seconds")
        
        if result['status'] == 'success':
            print(f"Updates Applied: {result['updates_applied']}")
            print(f"Changes Processed: {result['changes_processed']}")
            if result.get('backup_created'):
                print(f"Backup Created: {result['backup_created']}")
        elif result['status'] == 'error':
            print(f"Error: {result['message']}")
        else:
            print(f"Message: {result['message']}")
        
        return result

def main():
    """
    Main entry point for the documentation scheduler.
    """
    import argparse
    
    parser = argparse.ArgumentParser(description='AnNi AI Documentation Scheduler')
    parser.add_argument('--mode', choices=['immediate', 'scheduled'], default='immediate',
                       help='Run mode: immediate update or scheduled updates')
    parser.add_argument('--interval', type=int, default=30,
                       help='Update interval in minutes (for scheduled mode)')
    parser.add_argument('--status', action='store_true',
                       help='Show scheduler status and exit')
    
    args = parser.parse_args()
    
    scheduler = DocumentationScheduler()
    
    if args.status:
        status = scheduler.get_status()
        print("\n=== Documentation Scheduler Status ===")
        for key, value in status.items():
            print(f"{key.replace('_', ' ').title()}: {value}")
        return
    
    if args.mode == 'immediate':
        # Run immediate update
        asyncio.run(scheduler.run_immediate_update())
    else:
        # Run scheduled updates
        try:
            asyncio.run(scheduler.run_scheduled_updates(args.interval))
        except KeyboardInterrupt:
            print("\nScheduler stopped by user")

if __name__ == '__main__':
    main()

