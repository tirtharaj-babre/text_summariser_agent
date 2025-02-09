"""Module for formatting analysis results."""
from typing import Dict, Any


class OutputFormatter:
    """Handles formatting of analysis results for display."""
    
    @staticmethod
    def format_result(result: Dict[str, Any]) -> None:
        """
        Print analysis result in a formatted way.
        
        Args:
            result: Analysis result dictionary to format
        """
        print("\n" + "="*50)
        print("TEXT ANALYSIS RESULT")
        print("="*50)
        
        print(f"\nTimestamp: {result['timestamp']}")
        
        print("\nInput Text:")
        print("-"*50)
        print(result['input_text'])
        
        print("\nAnalysis Results:")
        print("-"*50)
        print(f"Summary:\n{result['analysis']['summary']}")
        print(f"\nKeywords:")
        for keyword in result['analysis']['keywords']:
            print(f"- {keyword}")
        print(f"\nSentiment: {result['analysis']['sentiment'].upper()}")
        
        print("\n" + "="*50 + "\n")
