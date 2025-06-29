"""Configuration management utilities."""

from pathlib import Path
from typing import Any, Dict

import yaml
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings


class JiraConfig(BaseModel):
    """JIRA configuration model."""
    
    url: str = Field(..., description="JIRA instance URL")
    username: str = Field(..., description="JIRA username")
    api_token: str = Field(..., description="JIRA API token")
    project_key: str = Field(..., description="Default project key")


class LLMConfig(BaseModel):
    """LLM configuration model."""
    
    provider: str = Field(default="openai", description="LLM provider (openai, anthropic)")
    model: str = Field(default="gpt-4", description="Model name")
    temperature: float = Field(default=0.7, description="Temperature for generation")
    max_tokens: int = Field(default=1000, description="Maximum tokens for generation")


class VectorDBConfig(BaseModel):
    """Vector database configuration model."""
    
    provider: str = Field(default="chroma", description="Vector DB provider (chroma, faiss)")
    persist_directory: str = Field(default="./data/chroma_db", description="Persistence directory")


class AppSettings(BaseSettings):
    """Application settings from environment variables."""
    
    # JIRA settings
    jira_url: str = Field(..., env="JIRA_URL")
    jira_username: str = Field(..., env="JIRA_USERNAME")
    jira_api_token: str = Field(..., env="JIRA_API_TOKEN")
    jira_project_key: str = Field(..., env="JIRA_PROJECT_KEY")
    
    # LLM settings
    openai_api_key: str = Field(default="", env="OPENAI_API_KEY")
    anthropic_api_key: str = Field(default="", env="ANTHROPIC_API_KEY")
    
    # Vector DB settings
    chroma_persist_directory: str = Field(default="./data/chroma_db", env="CHROMA_PERSIST_DIRECTORY")
    faiss_index_path: str = Field(default="./data/faiss_index", env="FAISS_INDEX_PATH")
    
    # App settings
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    max_retries: int = Field(default=3, env="MAX_RETRIES")
    timeout_seconds: int = Field(default=30, env="TIMEOUT_SECONDS")
    debug: bool = Field(default=False, env="DEBUG")
    environment: str = Field(default="development", env="ENVIRONMENT")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


def load_config(config_path: Path) -> Dict[str, Any]:
    """Load configuration from a YAML file.
    
    Args:
        config_path: Path to the YAML configuration file
        
    Returns:
        Dictionary containing the configuration
        
    Raises:
        FileNotFoundError: If the configuration file doesn't exist
        yaml.YAMLError: If the YAML file is invalid
    """
    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    
    with open(config_path, 'r', encoding='utf-8') as file:
        config = yaml.safe_load(file)
    
    if config is None:
        raise ValueError(f"Empty or invalid YAML file: {config_path}")
    
    return config


def get_app_settings() -> AppSettings:
    """Get application settings from environment variables.
    
    Returns:
        AppSettings instance with loaded configuration
    """
    return AppSettings()
