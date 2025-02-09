
"""Configuration settings for the application."""
from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class Config:
    """Application configuration class."""
    OPENAI_MODEL: str = "gpt-4o"
    MAX_TEXT_LENGTH: int = 4000
    MIN_TEXT_LENGTH: int = 10
    TEMPERATURE: float = 0.7
    MAX_TOKENS: int = 500
    PORT: int = 5000
    SERVER_STARTUP_DELAY: int = 2

    @property
    def model_config(self) -> Dict[str, Any]:
        """Get model configuration parameters."""
        return {
            "model": self.OPENAI_MODEL,
            "temperature": self.TEMPERATURE,
            "max_tokens": self.MAX_TOKENS
        }
