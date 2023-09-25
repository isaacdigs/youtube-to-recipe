import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
import openai

# Open AI setting
openai.api_key = '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'

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


# Streamlit app title
st.title("YouTube Recipe Extractor")

# Input field for the YouTube video ID
video_id = st.text_input("Enter YouTube Video ID:")

# JSON_converter function
def convert_to_json(text):
    st.subheader("Recipe (JSON):")
    recipe_json = text_to_json("".join(text))
    st.write(recipe_json)

# Check if a video ID is provided
if video_id:
    try:
        # Extract transcript for the given video ID (not URL)
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['ko', 'en'])

        # Display the transcript
        st.subheader("Transcript:")
        transcript_text = []
        for entry in transcript:
            # Convert time to desired format (seconds) for youtube timestamp url
            # format: https://youtu.be/(video_id)?t=(time in seconds)
            converted_time = int(entry['start'])
            transcript_text.append(f"({converted_time}) : {entry['text']}")

        st.write("".join(transcript_text))
        if st.button("Convert to JSON recipe"):
            convert_to_json(transcript_text)

    except Exception as e:
        st.error(f"An error occurred while fetching the transcript: {str(e)}")

# Test video IDs 
# ZMdYi7wG6JA
# qWbHSOplcvY
# 4qYZuxc-8KY
# BHP60TVc4VE