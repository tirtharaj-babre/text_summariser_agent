"""Text analysis module using OpenAI's GPT model."""
from typing import Dict, Tuple, Any, List
import logging
from openai import OpenAI
from config import Config

logger = logging.getLogger(__name__)

class TextAnalyzer:
    """Handles text analysis using OpenAI's GPT model."""
    
    def __init__(self, client: OpenAI, config: Config):
        """Initialize TextAnalyzer with OpenAI client and config."""
        self.client = client
        self.config = config

    def validate_text(self, text: str) -> Tuple[bool, str]:
        """
        Validate input text based on configured constraints.
        
        Args:
            text: Input text to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not isinstance(text, str):
            return False, "Input must be a string"
        
        text_length = len(text.strip())
        if text_length < self.config.MIN_TEXT_LENGTH:
            return False, f"Text must be at least {self.config.MIN_TEXT_LENGTH} characters long"
        if text_length > self.config.MAX_TEXT_LENGTH:
            return False, f"Text must not exceed {self.config.MAX_TEXT_LENGTH} characters"
        
        return True, ""

    def process_text(self, text: str) -> Dict[str, Any]:
        """
        Process text using OpenAI's GPT model.
        
        Args:
            text: Input text to analyze
            
        Returns:
            Dictionary containing analysis results
            
        Raises:
            Exception: If processing fails
        """
        try:
            prompt = self._create_analysis_prompt(text)
            response = self._get_model_response(prompt)
            return self._parse_response(response)
        except Exception as e:
            logger.error(f"Error processing text: {str(e)}")
            raise

    def _create_analysis_prompt(self, text: str) -> str:
        """Create structured prompt for the model."""
        return f"""Analyze the following text and provide:
                    1. Summary (max 2 sentences)
                    2. Keywords (max 5)
                    3. Sentiment (positive/negative/neutral)

                    Text: {text}

                    Please format the response as:
                    Summary: <summary>
                    Keywords: <keyword1>, <keyword2>, ...
                    Sentiment: <sentiment>"""

    def _get_model_response(self, prompt: str) -> str:
        """Get response from OpenAI model."""
        response = self.client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a text analysis assistant."},
                {"role": "user", "content": prompt}
            ],
            **self.config.model_config
        )
        return response.choices[0].message.content

    def _parse_response(self, response: str) -> Dict[str, Any]:
        """Parse model response into structured format."""
        lines = response.split('\n')
        result = {}
        
        for line in lines:
            if line.startswith('Summary:'):
                result['summary'] = line.replace('Summary:', '').strip()
            elif line.startswith('Keywords:'):
                keywords = line.replace('Keywords:', '').strip()
                result['keywords'] = [k.strip() for k in keywords.split(',')]
            elif line.startswith('Sentiment:'):
                result['sentiment'] = line.replace('Sentiment:', '').strip().lower()
        
        return result
