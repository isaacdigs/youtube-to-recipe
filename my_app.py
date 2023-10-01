from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
import openai
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load OpenAI API key from config
with open('config.json', 'r') as file:
    config = json.load(file)
    openai.api_key = config['OPENAI_API_KEY']

# Function to chunk text
def chunk_text(text, max_length):
    chunks = []
    while text:
        if len(text) > max_length:
            split_index = text[:max_length].rfind(' ')
            chunks.append(text[:split_index])
            text = text[split_index:]
        else:
            chunks.append(text)
            break
    return chunks

# function to convert to recipe JSON
def text_to_json(text): 
    max_token_length = 2000
    chunks = chunk_text(text, max_token_length)

    # prompt structure
    system_message = """
    You are a helpful assistant. Given the following YouTube transcript, convert it into a structured recipe in the following JSON format:

    {
      "author": "Name of the author (if mentioned)",
      "ingredients": {
        "ingredient":"amount",
      }
      "steps": {
        "timestamp":"step 1 of the instructions",
        "timestamp:"step 2 of the instructions",
      }
    }
    
    Make sure you leave out unnecessary comments and exclamations, and maintain the transcript's language.

    Transcript: 
    """

    # aggregate results from all chunks
    results = []
    for chunk in chunks:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": chunk}
            ]
        )
        results.append(response.choices[0].message['content'].strip())

    # Again, for simplicity, let's join all results.
    return " ".join(results)


@app.route('/transcript', methods=['POST'])
def get_transcript():
    video_id = request.json.get('videoId')
    
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['ko', 'en'])
        transcript_text = [{'time': int(entry['start']), 'text': entry['text']} for entry in transcript]
        return jsonify(transcript_text)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/recipe', methods=['POST'])
def get_recipe():
    data = request.json
    transcript = data.get('transcript', [])
    if not isinstance(transcript, list):
        return jsonify({"error": "Invalid data. 'transcript' should be a list of strings."}), 400
    
    transcript_text = "".join(transcript)
    recipe_json = text_to_json(transcript_text)
    return jsonify({"recipe": recipe_json})


if __name__ == "__main__":
    app.run(debug=True)


# Test video IDs 
# ZMdYi7wG6JA
# qWbHSOplcvY
# 4qYZuxc-8KY
# BHP60TVc4VE