"""OpenAI client for LLM interactions."""

import asyncio
from typing import List, Optional

from langchain.chat_models import ChatOpenAI
from langchain.schema import BaseMessage, AIMessage
from loguru import logger

from src.utils.config import get_app_settings


class OpenAIClient:
    """Async OpenAI client for LLM interactions."""
    
    def __init__(self, model: str = "gpt-4", temperature: float = 0.7):
        """Initialize the OpenAI client.
        
        Args:
            model: OpenAI model to use
            temperature: Temperature for generation
        """
        self.settings = get_app_settings()
        self.model = model
        self.temperature = temperature
        self._client: Optional[ChatOpenAI] = None
    
    @property
    def client(self) -> ChatOpenAI:
        """Get or create ChatOpenAI client instance.
        
        Returns:
            ChatOpenAI client instance
        """
        if self._client is None:
            self._client = ChatOpenAI(
                model=self.model,
                temperature=self.temperature,
                openai_api_key=self.settings.openai_api_key,
                max_tokens=1000,
                timeout=self.settings.timeout_seconds,
                max_retries=self.settings.max_retries,
            )
        return self._client
    
    async def agenerate(self, messages: List[BaseMessage]) -> AIMessage:
        """Generate response from messages asynchronously.
        
        Args:
            messages: List of messages for the conversation
            
        Returns:
            AI response message
            
        Raises:
            Exception: If generation fails
        """
        try:
            response = await self.client.agenerate([messages])
            
            if not response.generations or not response.generations[0]:
                raise ValueError("Empty response from OpenAI")
            
            generation = response.generations[0][0]
            return AIMessage(content=generation.text)
            
        except Exception as e:
            logger.error(f"OpenAI generation failed: {e}")
            raise
    
    async def generate_story_expansion(self, prompt: str) -> str:
        """Generate story expansion from prompt.
        
        Args:
            prompt: Expansion prompt
            
        Returns:
            Expanded story content
        """
        from langchain.schema import HumanMessage
        
        try:
            messages = [HumanMessage(content=prompt)]
            response = await self.agenerate(messages)
            
            logger.info("Story expansion generated successfully")
            return response.content
            
        except Exception as e:
            logger.error(f"Story expansion failed: {e}")
            raise
    
    async def generate_completion(self, prompt: str, max_tokens: Optional[int] = None) -> str:
        """Generate text completion from prompt.
        
        Args:
            prompt: Input prompt
            max_tokens: Maximum tokens to generate
            
        Returns:
            Generated text
        """
        try:
            # Temporarily override max_tokens if provided
            original_max_tokens = self.client.max_tokens
            if max_tokens:
                self.client.max_tokens = max_tokens
            
            from langchain.schema import HumanMessage
            messages = [HumanMessage(content=prompt)]
            response = await self.agenerate(messages)
            
            # Restore original max_tokens
            self.client.max_tokens = original_max_tokens
            
            return response.content
            
        except Exception as e:
            logger.error(f"Text completion failed: {e}")
            raise
