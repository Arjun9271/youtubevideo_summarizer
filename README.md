# YouTube Video Summarizer

## 🎥 Overview

YouTube Video Summarizer is a Streamlit-based web application that transforms lengthy YouTube videos into concise, insightful summaries. Using advanced AI technology, it extracts the key points and main ideas from video transcripts, saving users time and enhancing their understanding of video content.

## 🌟 Features

- **YouTube Video Link Input**: Simply paste the URL of any YouTube video.
- **Automatic Transcript Extraction**: Utilizes the YouTube Transcript API to fetch video transcripts.
- **AI-Powered Summarization**: Employs Google's Generative AI (Gemini model) to create comprehensive summaries.
- **Interactive UI**: Built with Streamlit for a user-friendly experience.
- **Custom Styling**: Enhanced visual appeal with custom CSS.
- **Summary Download**: Option to download the generated summary as a text file.
- **Video Thumbnail Display**: Shows the video thumbnail and basic info for easy reference.

## 🛠 Technologies Used

- Python
- Streamlit
- Google Generative AI (Gemini model)
- YouTube Transcript API
- dotenv

## 📋 Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.7+
- A Google API key with access to the Generative AI API

## 🚀 Installation & Setup

1. Clone the repository:
   ```
   git clone https://github.com/your-username/youtube-video-summarizer.git
   cd youtube-video-summarizer
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root and add your Google API key:
   ```
   GOOGLE_API_KEY=your_api_key_here
   ```

## 🖥 Usage

1. Run the Streamlit app:
   ```
   streamlit run app.py
   ```

2. Open your web browser and navigate to the provided local URL (usually `http://localhost:8501`).

3. Enter a YouTube video URL in the input field.

4. Click the "Generate Summary" button to process the video and generate a summary.

5. View the summary in the expandable section and optionally download it as a text file.

## 📝 How It Works

1. The app extracts the video ID from the provided YouTube URL.
2. It fetches the video transcript using the YouTube Transcript API.
3. The transcript is sent to the Google Generative AI model along with a detailed prompt.
4. The AI generates a comprehensive summary based on the transcript and prompt.
5. The summary is displayed to the user and can be downloaded.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check [issues page](https://github.com/your-username/youtube-video-summarizer/issues).

## 📜 License

This project is [MIT](https://choosealicense.com/licenses/mit/) licensed.

## 👏 Acknowledgements

- [Streamlit](https://streamlit.io/)
- [Google Generative AI](https://cloud.google.com/ai-platform/prediction/docs/overview)
- [YouTube Transcript API](https://github.com/jdepoix/youtube-transcript-api)

---
