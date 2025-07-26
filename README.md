# YouTube Video Summarizer

A Streamlit web application that generates concise summaries of YouTube videos by extracting their transcripts and using Google's Gemini AI for summarization.

## Features

- Extracts transcripts from any YouTube video with available captions
- Uses Google's Gemini AI to generate concise summaries
- Simple and intuitive web interface
- Handles errors gracefully with user-friendly messages

## Prerequisites

- Python 3.8 or higher
- Google Gemini API key

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/youtube-videosummarizer.git
   cd youtube-videosummarizer
   ```

2. Create and activate a virtual environment:
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate
   
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root and add your Gemini API key:
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   ```
   
   Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

## Usage

1. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

2. Open your web browser and navigate to `http://localhost:8501`

3. Enter a YouTube video URL and click "Generate Summary"

4. View the generated summary of the video's transcript

## How It Works

1. The app extracts the video ID from the YouTube URL
2. It fetches the video's transcript using the YouTube Transcript API
3. The transcript is sent to Google's Gemini AI for summarization
4. The generated summary is displayed to the user

## Dependencies

- streamlit - Web application framework
- google-generativeai - Google's Gemini AI client library
- youtube-transcript-api - For fetching YouTube video transcripts
- python-dotenv - For loading environment variables

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

- [Google Gemini AI](https://ai.google/)
- [Streamlit](https://streamlit.io/)
- [YouTube Transcript API](https://github.com/jdepoix/youtube-transcript-api)
