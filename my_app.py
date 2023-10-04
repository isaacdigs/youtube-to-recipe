# ----- General imports -----

from fastapi import FastAPI, HTTPException
from starlette.responses import JSONResponse
from youtube_transcript_api import YouTubeTranscriptApi
import openai
import json

# ----- imports for debugging -----
import traceback
import logging

# ----- Configuration -----
with open("config.json", "r") as file:
    config = json.load(file)
    openai.api_key = config["OPENAI_API_KEY"]

logging.basicConfig(level=logging.ERROR)
app = FastAPI()

# Prompts
INGREDIENT_PROMPT = """
You are a helpful assistant. Given the following YouTube transcript, extract and list down all the ingredients in the following JSON format:

{
  "ingredients": {
    "ingredient1":"amount1",
    "ingredient2":"amount2",
    ...
  }
}

Transcript: 
"""
INSTRUCTIONS_PROMPT = """
You are a helpful assistant. Given the following YouTube transcript, convert it into a structured set of cooking instructions in the following JSON format:

{
  "steps": {
    "timestamp1":"step 1 of the instructions",
    "timestamp2":"step 2 of the instructions",
    ...
  }
}

Transcript: 
"""

# ----- Utility Functions -----
def chunk_text(text, max_length):
    words = text.split()
    chunks = []
    chunk = ""
    for word in words:
        if len(chunk) + len(word) <= max_length:
            chunk += word + " "
        else:
            chunks.append(chunk.strip())
            chunk = word + " "
    if chunk:
        chunks.append(chunk.strip())
    return chunks

def extract_from_transcript(text, prompt):
    max_token_length = 2000
    chunks = chunk_text(text, max_token_length - len(prompt) - 50)  # Buffer space
    results = []
    for chunk in chunks:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": chunk}
                ]
            )
            results.append(response.choices[0].message['content'].strip())
        except:
            raise HTTPException(status_code=500, detail="OpenAI processing error")
    return " ".join(results)

# ----- API Endpoints -----
@app.post("/get_ingredients/")
async def get_ingredients(video_id: str):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
        transcript_text = " ".join([entry['text'] for entry in transcript])
        ingredients_json = extract_from_transcript(transcript_text, INGREDIENT_PROMPT)
        return JSONResponse(content=json.loads(ingredients_json))
    except Exception as e:
        traceback_str = traceback.format_exc()
        logging.error(traceback_str)
        raise HTTPException(status_code=500, detail=f"Error processing ingredients: {traceback_str}")

@app.post("/get_instructions/")
async def get_instructions(video_id: str):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
        transcript_text = " ".join([entry['text'] for entry in transcript])
        instructions_json = extract_from_transcript(transcript_text, INSTRUCTIONS_PROMPT)
        return JSONResponse(content=json.loads(instructions_json))
    except Exception as e:
        traceback_str = traceback.format_exc()
        logging.error(traceback_str)
        raise HTTPException(status_code=500, detail=f"Error processing instructions: {traceback_str}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

# Test video IDs 
# ZMdYi7wG6JA
# qWbHSOplcvY
# 4qYZuxc-8KY
# BHP60TVc4VE
