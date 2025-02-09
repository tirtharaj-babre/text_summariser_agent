# Flask LLM Text Processing API

This is a Flask-based REST API that processes text input using OpenAI's GPT model for text analysis.

## Features
- Text processing with GPT-4o model
- Summary generation
- Keyword extraction
- Sentiment analysis
- Processing history
- Input validation
- Error handling

## Setup
1. Clone the repository
2. Create and activate a virtual environment:
   ```bash
   python3 -m venv .venv
   source venv/bin/activate
   ```
2. Install dependencies: `pip install -r requirements.txt`
3. Add your API Keys in `.env` file.
4. Run the application
   ```bash
   cd backend_app
   python3 main.py
   ```

## API Endpoints
- POST `/process`     : Process text input
- GET `/history`      : Retrieve processing history

## Instructions
1. Open `main.py` file. Add your text for anlysis in 'process_user_input' function.
2. Run the application: `python3 main.py`
3. Check the terminal for the results.
4. If you want to give further more text to analysis then type it in terminal itself otherewise type quit to exit.
5. Result will look like this
   ```bash
      ==================================================
      TEXT ANALYSIS RESULT
      ==================================================

      Timestamp: 2025-02-09 16:40:26

      Input Text:
      --------------------------------------------------
      """Don't buy guys this noice grow watch. No exchange policy work of this product and customer care say we'll pick this product within 24 hr and no any response from noice.
            Worst product and my experience with noise. Total time pass service."""
            

      Analysis Results:
      --------------------------------------------------
      Summary:
      The customer is dissatisfied with the Noice grow watch due to a lack of exchange policy and poor customer service, resulting in a negative experience. The product and service are described as inadequate and a waste of time.

      Keywords:
      - Noice
      - grow watch
      - exchange policy
      - customer service
      - worst product

      Sentiment: NEGATIVE

      ==================================================
   ```
