"""JIRA client for creating and managing issues."""

import asyncio
from typing import Any, Dict, List, Optional

import aiohttp
from jira import JIRA
from loguru import logger

from src.utils.config import get_app_settings


class JiraClient:
    """Async JIRA client for issue management."""
    
    def __init__(self):
        """Initialize the JIRA client."""
        self.settings = get_app_settings()
        self._client: Optional[JIRA] = None
        self._session: Optional[aiohttp.ClientSession] = None
    
    @property
    def client(self) -> JIRA:
        """Get or create JIRA client instance.
        
        Returns:
            JIRA client instance
        """
        if self._client is None:
            self._client = JIRA(
                server=self.settings.jira_url,
                basic_auth=(self.settings.jira_username, self.settings.jira_api_token)
            )
        return self._client
    
    async def create_issue(self, issue_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new JIRA issue.
        
        Args:
            issue_data: Dictionary containing issue fields
            
        Returns:
            Dictionary containing created issue information
            
        Raises:
            Exception: If issue creation fails
        """
        try:
            # Validate required fields
            self._validate_issue_data(issue_data)
            
            # Create the issue
            issue = await asyncio.get_event_loop().run_in_executor(
                None, 
                lambda: self.client.create_issue(fields=issue_data)
            )
            
            logger.info(f"Created JIRA issue: {issue.key}")
            
            return {
                "key": issue.key,
                "id": issue.id,
                "url": f"{self.settings.jira_url}/browse/{issue.key}",
                "summary": issue_data.get("summary"),
                "project": issue_data.get("project", {}).get("key"),
            }
            
        except Exception as e:
            logger.error(f"Failed to create JIRA issue: {e}")
            raise
    
    async def get_issue(self, issue_key: str) -> Dict[str, Any]:
        """Get JIRA issue by key.
        
        Args:
            issue_key: JIRA issue key (e.g., 'PROJ-123')
            
        Returns:
            Dictionary containing issue information
        """
        try:
            issue = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.client.issue(issue_key)
            )
            
            return {
                "key": issue.key,
                "id": issue.id,
                "summary": issue.fields.summary,
                "description": issue.fields.description,
                "status": issue.fields.status.name,
                "assignee": issue.fields.assignee.displayName if issue.fields.assignee else None,
                "reporter": issue.fields.reporter.displayName if issue.fields.reporter else None,
                "created": issue.fields.created,
                "updated": issue.fields.updated,
            }
            
        except Exception as e:
            logger.error(f"Failed to get JIRA issue {issue_key}: {e}")
            raise
    
    async def update_issue(self, issue_key: str, update_data: Dict[str, Any]) -> bool:
        """Update a JIRA issue.
        
        Args:
            issue_key: JIRA issue key
            update_data: Dictionary containing fields to update
            
        Returns:
            True if update was successful
        """
        try:
            await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.client.issue(issue_key).update(fields=update_data)
            )
            
            logger.info(f"Updated JIRA issue: {issue_key}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to update JIRA issue {issue_key}: {e}")
            raise
    
    async def search_issues(self, jql: str, max_results: int = 50) -> List[Dict[str, Any]]:
        """Search for JIRA issues using JQL.
        
        Args:
            jql: JQL query string
            max_results: Maximum number of results to return
            
        Returns:
            List of issue dictionaries
        """
        try:
            issues = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.client.search_issues(jql, maxResults=max_results)
            )
            
            return [
                {
                    "key": issue.key,
                    "id": issue.id,
                    "summary": issue.fields.summary,
                    "status": issue.fields.status.name,
                    "assignee": issue.fields.assignee.displayName if issue.fields.assignee else None,
                }
                for issue in issues
            ]
            
        except Exception as e:
            logger.error(f"Failed to search JIRA issues: {e}")
            raise
    
    def _validate_issue_data(self, issue_data: Dict[str, Any]) -> None:
        """Validate issue data before creation.
        
        Args:
            issue_data: Issue data dictionary
            
        Raises:
            ValueError: If required fields are missing
        """
        required_fields = ["project", "summary", "issuetype"]
        
        for field in required_fields:
            if field not in issue_data:
                raise ValueError(f"Required field '{field}' is missing from issue data")
        
        # Validate project format
        if not isinstance(issue_data["project"], dict) or "key" not in issue_data["project"]:
            raise ValueError("Project must be a dictionary with 'key' field")
        
        # Validate issue type format
        if not isinstance(issue_data["issuetype"], dict) or "name" not in issue_data["issuetype"]:
            raise ValueError("Issue type must be a dictionary with 'name' field")
    
    async def close(self) -> None:
        """Close the client and cleanup resources."""
        if self._session:
            await self._session.close()
        self._client = None
        logger.info("JIRA client closed")
