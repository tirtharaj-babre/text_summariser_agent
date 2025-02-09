"""Main application module."""
import threading
import time
import logging
from typing import NoReturn, List, Dict, Any
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
from dotenv import load_dotenv
import os
from openai import OpenAI
from config import Config
from text_analyzer import TextAnalyzer
from output_formatter import OutputFormatter

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize configuration
config = Config()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Initialize analyzer and formatter
analyzer = TextAnalyzer(client, config)
formatter = OutputFormatter()

# In-memory storage
processed_history: List[Dict[str, Any]] = []

@app.route('/process', methods=['POST'])
def process_text() -> tuple:
    """Process incoming text and return analysis results."""
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({'error': 'Missing text field'}), 400
            
        text = data['text']
        
        is_valid, error_message = analyzer.validate_text(text)
        if not is_valid:
            return jsonify({'error': error_message}), 400

        analysis_result = analyzer.process_text(text)
        
        result = {
            'timestamp': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
            'input_text': text,
            'analysis': analysis_result
        }
        
        processed_history.append(result)
        
        return jsonify(result), 200

    except Exception as e:
        logger.error(f"Error in process_text: {str(e)}")
        return jsonify({'error': str(e)}), 500

def run_flask() -> None:
    """Run the Flask server."""
    app.run(debug=False, port=config.PORT)

def process_user_input() -> NoReturn:
    """Handle user input and process text."""
    time.sleep(config.SERVER_STARTUP_DELAY)
    
    # Type your text here to get summary and check the sentimate
    test_data = {
        'text': """Don't buy guys this noice grow watch. No exchange policy work of this product and customer care say we'll pick this product within 24 hr and no any response from noice.
        Worst product and my experience with noise. Total time pass service.
        """
    }
    
    try:
        response = requests.post(
            f'http://localhost:{config.PORT}/process',
            json=test_data
        )
        if response.status_code == 200:
            formatter.format_result(response.json())
    except Exception as e:
        logger.error(f"Error in initial test: {str(e)}")

    # Interactive loop
    while True:
        try:
            user_input = input("\nEnter text to analyze (or 'quit' to exit): ").strip()
            if user_input.lower() == 'quit':
                break
            
            if user_input:
                response = requests.post(
                    f'http://localhost:{config.PORT}/process',
                    json={'text': user_input}
                )
                if response.status_code == 200:
                    formatter.format_result(response.json())
                else:
                    print(f"\nError: {response.json().get('error', 'Unknown error occurred')}")
                    
        except KeyboardInterrupt:
            print("\nShutting down...")
            break
        except Exception as e:
            logger.error(f"Error processing input: {str(e)}")
            print(f"\nError: {str(e)}")

if __name__ == '__main__':
    try:
        # Start Flask in a separate thread
        server_thread = threading.Thread(target=run_flask)
        server_thread.daemon = True
        server_thread.start()

        # Run the interactive input processor
        process_user_input()
        
    except Exception as e:
        logger.error(f"Application error: {str(e)}")
