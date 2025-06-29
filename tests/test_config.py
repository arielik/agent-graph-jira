"""Test configuration for JIRA agent."""

import pytest
from unittest.mock import patch, MagicMock

from src.utils.config import load_config, get_app_settings, AppSettings


class TestConfig:
    """Test configuration utilities."""
    
    def test_load_config_valid_file(self, tmp_path):
        """Test loading a valid YAML configuration file."""
        # Create test YAML file
        config_content = """
global:
  project: "TEST"
  labels:
    - "test"

stories:
  - title: "Test Story"
    description: "Test description"
        """
        
        config_file = tmp_path / "test_config.yaml"
        config_file.write_text(config_content)
        
        # Load configuration
        config = load_config(config_file)
        
        # Assertions
        assert config["global"]["project"] == "TEST"
        assert config["global"]["labels"] == ["test"]
        assert len(config["stories"]) == 1
        assert config["stories"][0]["title"] == "Test Story"
    
    def test_load_config_file_not_found(self, tmp_path):
        """Test loading a non-existent configuration file."""
        config_file = tmp_path / "nonexistent.yaml"
        
        with pytest.raises(FileNotFoundError):
            load_config(config_file)
    
    @patch('src.utils.config.AppSettings')
    def test_get_app_settings(self, mock_settings):
        """Test getting application settings."""
        mock_instance = MagicMock()
        mock_settings.return_value = mock_instance
        
        result = get_app_settings()
        
        assert result == mock_instance
        mock_settings.assert_called_once()


class TestAppSettings:
    """Test application settings."""
    
    @patch.dict('os.environ', {
        'JIRA_URL': 'https://test.atlassian.net',
        'JIRA_USERNAME': 'test@example.com',
        'JIRA_API_TOKEN': 'test-token',
        'JIRA_PROJECT_KEY': 'TEST',
    })
    def test_app_settings_from_env(self):
        """Test loading settings from environment variables."""
        settings = AppSettings()
        
        assert settings.jira_url == 'https://test.atlassian.net'
        assert settings.jira_username == 'test@example.com'
        assert settings.jira_api_token == 'test-token'
        assert settings.jira_project_key == 'TEST'
