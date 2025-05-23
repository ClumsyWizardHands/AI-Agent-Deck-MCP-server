"""Configuration management for Agent Swarm MCP Server."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Required environment variables
    CLAUDE_API_KEY: str
    
    # Optional with defaults
    MASTER_PROMPT_PATH: str = "./prompts/master_prompt.txt"
    
    class Config:
        """Pydantic configuration."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# Instantiate settings
settings = Settings()
