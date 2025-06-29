"""JIRA Agent implementation using LangGraph."""

import asyncio
from typing import Any, Dict, List, Optional

from langchain.schema import BaseMessage, HumanMessage
from langgraph.graph import Graph, StateGraph
from loguru import logger

from src.core.prompts.story_expansion import StoryExpansionPrompt
from src.core.tools.jira_client import JiraClient
from src.infrastructure.llm_clients.openai_client import OpenAIClient
from src.utils.config import get_app_settings


class AgentState:
    """State for the JIRA agent workflow."""
    
    def __init__(self):
        self.stories: List[Dict[str, Any]] = []
        self.current_story: Optional[Dict[str, Any]] = None
        self.expanded_story: Optional[str] = None
        self.jira_issue: Optional[Dict[str, Any]] = None
        self.error: Optional[str] = None


class JiraAgent:
    """Main JIRA agent that processes stories using LangGraph."""
    
    def __init__(self, config: Dict[str, Any], dry_run: bool = False):
        """Initialize the JIRA agent.
        
        Args:
            config: Configuration dictionary from YAML file
            dry_run: If True, don't actually create JIRA issues
        """
        self.config = config
        self.dry_run = dry_run
        self.settings = get_app_settings()
        
        # Initialize components
        self.llm_client = OpenAIClient()
        self.jira_client = JiraClient()
        self.prompt = StoryExpansionPrompt()
        
        # Build the workflow graph
        self.graph = self._build_graph()
        
        logger.info(f"JiraAgent initialized (dry_run={dry_run})")
    
    def _build_graph(self) -> StateGraph:
        """Build the LangGraph workflow.
        
        Returns:
            StateGraph representing the agent workflow
        """
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("load_stories", self._load_stories)
        workflow.add_node("process_story", self._process_story)
        workflow.add_node("expand_story", self._expand_story)
        workflow.add_node("create_jira_issue", self._create_jira_issue)
        workflow.add_node("handle_error", self._handle_error)
        
        # Add edges
        workflow.add_edge("load_stories", "process_story")
        workflow.add_edge("process_story", "expand_story")
        workflow.add_edge("expand_story", "create_jira_issue")
        workflow.add_edge("create_jira_issue", "process_story")
        workflow.add_edge("handle_error", "process_story")
        
        # Set entry point
        workflow.set_entry_point("load_stories")
        
        return workflow.compile()
    
    async def process_stories(self) -> None:
        """Process all stories from the configuration."""
        state = AgentState()
        
        try:
            # Run the workflow
            result = await self.graph.ainvoke(state)
            logger.info("All stories processed successfully")
            
        except Exception as e:
            logger.error(f"Error processing stories: {e}")
            raise
    
    def _load_stories(self, state: AgentState) -> AgentState:
        """Load stories from configuration.
        
        Args:
            state: Current agent state
            
        Returns:
            Updated agent state
        """
        stories = self.config.get("stories", [])
        state.stories = stories
        logger.info(f"Loaded {len(stories)} stories from configuration")
        return state
    
    def _process_story(self, state: AgentState) -> AgentState:
        """Process the next story in the queue.
        
        Args:
            state: Current agent state
            
        Returns:
            Updated agent state
        """
        if not state.stories:
            logger.info("No more stories to process")
            return state
        
        # Get next story
        state.current_story = state.stories.pop(0)
        logger.info(f"Processing story: {state.current_story.get('title', 'Untitled')}")
        
        return state
    
    async def _expand_story(self, state: AgentState) -> AgentState:
        """Expand the current story using LLM.
        
        Args:
            state: Current agent state
            
        Returns:
            Updated agent state
        """
        if not state.current_story:
            state.error = "No current story to expand"
            return state
        
        try:
            # Generate expansion prompt
            prompt = self.prompt.generate_expansion_prompt(state.current_story)
            
            # Get LLM response
            messages = [HumanMessage(content=prompt)]
            response = await self.llm_client.agenerate(messages)
            
            state.expanded_story = response.content
            logger.info("Story expanded successfully")
            
        except Exception as e:
            state.error = f"Error expanding story: {e}"
            logger.error(state.error)
        
        return state
    
    async def _create_jira_issue(self, state: AgentState) -> AgentState:
        """Create JIRA issue from expanded story.
        
        Args:
            state: Current agent state
            
        Returns:
            Updated agent state
        """
        if state.error:
            return state
        
        if not state.expanded_story or not state.current_story:
            state.error = "Missing expanded story or current story"
            return state
        
        try:
            # Prepare issue data
            issue_data = self._prepare_issue_data(state.current_story, state.expanded_story)
            
            if self.dry_run:
                logger.info(f"[DRY RUN] Would create JIRA issue: {issue_data}")
                state.jira_issue = {"key": "DRY-RUN-123", "dry_run": True}
            else:
                # Create actual JIRA issue
                state.jira_issue = await self.jira_client.create_issue(issue_data)
                logger.info(f"Created JIRA issue: {state.jira_issue.get('key')}")
            
        except Exception as e:
            state.error = f"Error creating JIRA issue: {e}"
            logger.error(state.error)
        
        return state
    
    def _handle_error(self, state: AgentState) -> AgentState:
        """Handle errors in the workflow.
        
        Args:
            state: Current agent state
            
        Returns:
            Updated agent state
        """
        if state.error:
            logger.error(f"Handling error: {state.error}")
            # Reset error state and continue with next story
            state.error = None
            state.current_story = None
            state.expanded_story = None
            state.jira_issue = None
        
        return state
    
    def _prepare_issue_data(self, story: Dict[str, Any], expanded_content: str) -> Dict[str, Any]:
        """Prepare JIRA issue data from story and expanded content.
        
        Args:
            story: Original story from configuration
            expanded_content: LLM-expanded story content
            
        Returns:
            Dictionary containing JIRA issue data
        """
        # Get global configuration
        global_config = self.config.get("global", {})
        
        issue_data = {
            "project": {"key": story.get("project", global_config.get("project", self.settings.jira_project_key))},
            "summary": story.get("title", "Generated Story"),
            "description": expanded_content,
            "issuetype": {"name": story.get("issue_type", "Story")},
        }
        
        # Add labels if specified
        labels = story.get("labels", global_config.get("labels", []))
        if labels:
            issue_data["labels"] = labels
        
        # Add components if specified
        components = story.get("components", global_config.get("components", []))
        if components:
            issue_data["components"] = [{"name": comp} for comp in components]
        
        # Add epic link if specified
        epic_key = story.get("epic", global_config.get("epic"))
        if epic_key:
            issue_data["customfield_10014"] = epic_key  # Epic Link field
        
        return issue_data
