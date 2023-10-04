# YouTube Cooking Assistant API

This FastAPI application extracts ingredients and cooking instructions from YouTube video transcripts using OpenAI's GPT-3.5-turbo model.

## Setup

1. **Dependencies**:
   Ensure you have the required Python packages installed:

   ```bash
   pip install fastapi[all] youtube_transcript_api openai uvicorn
   ```

2. **Configuration**:
   Create a `config.json` in the root directory with the following structure:

   ```json
   {
       "OPENAI_API_KEY": "Your-OpenAI-API-Key"
   }
   ```

   Replace `Your-OpenAI-API-Key` with your actual OpenAI API key.

## How It Works

1. **Initialization**:
   - Import necessary modules and packages.
   - Load the OpenAI API key from `config.json`.
   - Set up logging to handle errors.
   - Initialize the FastAPI application.

2. **Prompt Definitions**:
   - `INGREDIENT_PROMPT`: Extracts ingredients from the YouTube transcript.
   - `INSTRUCTIONS_PROMPT`: Converts the transcript into structured cooking instructions.

3. **Utility Functions**:
   - `chunk_text`: Breaks long texts into smaller chunks that are manageable for GPT-3.5-turbo.
   - `extract_from_transcript`: Processes the YouTube transcript based on a given prompt and returns the model's response.

4. **API Endpoints**:
   - `POST /get_ingredients/`: Accepts a YouTube video ID, fetches the transcript, and returns the extracted ingredients in a structured JSON format.
   - `POST /get_instructions/`: Accepts a YouTube video ID, fetches the transcript, and returns the structured cooking instructions in JSON format.

## Running the API

To run the API locally:

```bash
uvicorn my_app:app --host 0.0.0.0 --port 8000
```

Replace `my_app` with the name of your python script if it's different.

## Testing

The application has been tested with a few YouTube video IDs, such as:
- `ZMdYi7wG6JA`
- `qWbHSOplcvY`
- `4qYZuxc-8KY`
- `BHP60TVc4VE`

## Error Handling

Error handling mechanisms are in place to manage potential issues with the OpenAI API or with fetching YouTube transcripts. Detailed error logs help in identifying and troubleshooting issues.

## Future Enhancements

1. Incorporate a caching mechanism to store results for previously processed videos.
2. Enhance the NLP model training for better accuracy in ingredients and instruction extraction.