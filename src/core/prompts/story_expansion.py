"""Story expansion prompts for the JIRA agent."""

from typing import Any, Dict


class StoryExpansionPrompt:
    """Handles prompt generation for story expansion."""
    
    def __init__(self):
        """Initialize the prompt handler."""
        self.base_prompt = """
You are an expert product manager and technical writer specializing in creating detailed, 
actionable user stories for software development teams.

Your task is to expand the given story outline into a comprehensive JIRA story that includes:

1. **Clear User Story**: A well-structured user story following the "As a [user], I want [goal] so that [benefit]" format
2. **Detailed Description**: Comprehensive explanation of the feature/requirement
3. **Acceptance Criteria**: Specific, testable criteria that define when the story is complete
4. **Technical Considerations**: Any technical notes or considerations for implementation
5. **Definition of Done**: Clear criteria for story completion

Guidelines:
- Write in clear, professional language
- Make acceptance criteria specific and testable
- Consider edge cases and error scenarios
- Include relevant technical details without being overly prescriptive
- Ensure the story is sized appropriately (not too large for a single sprint)

Original Story Information:
Title: {title}
Description: {description}
Priority: {priority}
Labels: {labels}
Components: {components}

Please expand this into a comprehensive JIRA story following the structure above.
        """.strip()
    
    def generate_expansion_prompt(self, story: Dict[str, Any]) -> str:
        """Generate expansion prompt for a story.
        
        Args:
            story: Story dictionary containing title, description, etc.
            
        Returns:
            Formatted prompt string
        """
        return self.base_prompt.format(
            title=story.get("title", "Untitled Story"),
            description=story.get("description", "No description provided"),
            priority=story.get("priority", "Medium"),
            labels=", ".join(story.get("labels", [])) or "None",
            components=", ".join(story.get("components", [])) or "None",
        )
    
    def generate_refinement_prompt(self, original_story: str, feedback: str) -> str:
        """Generate prompt for story refinement based on feedback.
        
        Args:
            original_story: The original expanded story
            feedback: Feedback or requirements for refinement
            
        Returns:
            Formatted refinement prompt
        """
        refinement_prompt = """
Please refine the following JIRA story based on the provided feedback:

Original Story:
{original_story}

Feedback/Requirements:
{feedback}

Please provide the refined version of the story, maintaining the same structure but 
addressing the feedback provided. Focus on improving clarity, completeness, and 
actionability of the story.
        """.strip()
        
        return refinement_prompt.format(
            original_story=original_story,
            feedback=feedback
        )
