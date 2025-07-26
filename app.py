import streamlit as st
import os
from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from dotenv import load_dotenv
from urllib.parse import urlparse, parse_qs

# Configure Streamlit page
st.set_page_config(page_title="Youtube video summarizer", page_icon="🎬")

# Load environment variables
load_dotenv()

# Initialize Gemini
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-2.5-pro')

def get_video_id(url):
    """Extract video ID from YouTube URL"""
    try:
        parsed_url = urlparse(url)
        if 'youtube.com' in parsed_url.netloc:
            return parse_qs(parsed_url.query).get('v', [None])[0]
        elif 'youtu.be' in parsed_url.netloc:
            return parsed_url.path.lstrip('/')
    except Exception as e:
        st.error(f"Error extracting video ID: {str(e)}")
    return None

def get_transcript(video_id):
    """Get transcript from YouTube video using YouTube Transcript API"""
    try:
        transcript_list = YouTubeTranscriptApi().fetch(video_id, languages=['de', 'en'])
        full_text = ' '.join([item.text for item in transcript_list])
        return full_text
    except Exception as e:
        st.error(f"Error getting transcript for video ID {video_id}: {e}")
        return None

def generate_summary(text):
    """Generate summary using Gemini"""
    if not text:
        return "No text to summarize"

    prompt = f"""Please provide a concise, factual summary of the following educational/informational content.
Focus on the main points and key information.

Content:
{text}

Summary:"""

    try:
        response = model.generate_content(
            prompt,
            generation_config={
                "max_output_tokens": 2000,
                "temperature": 0.3,
                "top_p": 0.8,
            },
            safety_settings={
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE
            }
        )
        if not response.text and hasattr(response, 'prompt_feedback') and hasattr(response.prompt_feedback, 'block_reason'):
            block_reason = str(getattr(response.prompt_feedback, 'block_reason', 'unknown'))
            return f"Could not generate summary: Blocked by safety filters. Reason: {block_reason}"
        return response.text
    except Exception as e:
        error_msg = str(e)
        if "block_reason" in error_msg or "PROHIBITED_CONTENT" in error_msg:
            return "Could not generate summary: Content was blocked by safety filters."
        st.error(f"Error generating summary: {error_msg}")
        return None

def main():
    st.title("🎬 YouTube Video Summarizer")

    video_url = st.text_input("Enter YouTube URL:")

    if st.button("Generate Summary"):
        if video_url:
            video_id = get_video_id(video_url)
            if not video_id:
                st.error("Invalid YouTube URL format")
                return

            with st.spinner("Fetching transcript..."):
                transcript = get_transcript(video_id)

            if transcript:
                with st.spinner("Generating summary..."):
                    summary = generate_summary(transcript)

                if summary:
                    st.success("Summary generated!")
                    st.write("### Summary:")
                    st.write(summary)
                    
                    # Display video player
                    #st.write("### Video Player:")
                    st.video(video_url)
        else:
            st.error("Please enter a YouTube URL")

if __name__ == "__main__":
    main()
