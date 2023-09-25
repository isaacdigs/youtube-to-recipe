# YouTube Recipe Extractor

This application lets you input a YouTube video ID, fetches its transcript, and then converts the transcript into a structured recipe format in JSON. The primary usage is to extract cooking recipes from cooking-related videos, especially those in Korean or English.

## Features

- Extracts transcript from any public YouTube video.
- Converts the transcript into a structured recipe in JSON format.
- Maintains the transcript's original language during conversion.

## Setup & Installation

### Prerequisites
- Python 3.x
- OpenAI API Key (GPT-3.5-turbo)

### Steps:
1. Clone the repository:
   ```bash
   git clone https://github.com/isaacdigs/youtube-to-recipe.git
   ```

2. Navigate to the cloned directory:
   ```bash
   cd youtube-to-recipe
   ```

3. Install the required packages:
   ```bash
   pip install streamlit youtube_transcript_api openai
   ```

4. Create a `config.json` file in the root directory with the following structure:
   ```json
   {
       "OPENAI_API_KEY": "YOUR_OPENAI_API_KEY"
   }
   ```
   Replace `YOUR_OPENAI_API_KEY` with your actual OpenAI API key.

5. Run the Streamlit app:
   ```bash
   streamlit run main.py
   ```

6. Open the displayed URL in your browser, and you're good to go!

## Usage

1. Enter a valid YouTube Video ID into the input field.
   
   Example video IDs: 
   - ZMdYi7wG6JA
   - qWbHSOplcvY
   - 4qYZuxc-8KY
   - BHP60TVc4VE

2. View the extracted transcript displayed below the input field.

3. Click the "Convert to JSON recipe" button to see the recipe structure.

## Limitations

- The application primarily supports Korean and English video transcripts. Other languages might not work as expected.
- The quality of the extracted recipe depends on the clarity and structure of the original video's transcript.

## Contributing

If you find any bugs or have feature requests, feel free to create issues or submit pull requests.

## License

[MIT](LICENSE)

---