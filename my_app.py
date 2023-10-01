from fastapi import FastAPI, HTTPException
from youtube_transcript_api import YouTubeTranscriptApi
import openai
import json

app = FastAPI()

# Load OpenAI API key from config.json
with open('config.json', 'r') as file:
    config = json.load(file)
    openai.api_key = config['OPENAI_API_KEY']

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

def text_to_json(text): 
    max_token_length = 2000
    chunks = chunk_text(text, max_token_length)
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
    return " ".join(results)

@app.post("/convert_to_recipe/")
async def convert_to_recipe(video_id: str):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['ko', 'en'])
        transcript_text = []
        for entry in transcript:
            converted_time = int(entry['start'])
            transcript_text.append(f"({converted_time}) : {entry['text']}")
        recipe_json = text_to_json("".join(transcript_text))
        return {"recipe": recipe_json}

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"An error occurred: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
