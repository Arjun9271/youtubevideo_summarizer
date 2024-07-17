import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
import re
import time

# Load environment variables
load_dotenv()

# Configure Google Generative AI
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

# Custom CSS to enhance the UI
st.markdown("""
<style>
    .reportview-container {
        background: linear-gradient(to right, #f5f7fa, #c3cfe2);
    }
    .main {
        background-color: rgba(255,255,255,0.8);
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        transition-duration: 0.4s;
        cursor: pointer;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .stTextInput>div>div>input {
        border-radius: 5px;
    }
    .css-1v3fvcr {
        background-color: transparent;
    }
</style>
""", unsafe_allow_html=True)

# Prompt for the AI model
prompt = '''
You are an expert YouTube Video Summarizer AI. Your task is to analyze the provided transcript 
and create a comprehensive summary of the video content. Follow these guidelines:

1. Provide a thorough overview of the video's main topic or purpose (3-4 sentences).
2. Identify and list the key points or main ideas discussed in the video (5-8 bullet points).
3. Elaborate on important facts, statistics, or examples mentioned, providing context if necessary.
4. Summarize any conclusions, insights, or call-to-action from the video (3-4 sentences).
5. Mention any notable speakers or experts featured in the video, including their relevance or expertise.
6. If applicable, briefly describe any demonstrations, experiments, or case studies presented.
7. Note any significant debates, controversies, or alternative viewpoints discussed in the video.

Your summary should be comprehensive, informative, and well-structured. Aim for a total length of approximately 500 words. 
Ensure that your summary captures the depth and breadth of the video content, providing readers with a thorough understanding 
of the material without the need to watch the full video.

Please provide the summary based on the following transcript:
'''

@st.cache_data
def extract_video_id(youtube_url):
    """Extract the video ID from various YouTube URL formats."""
    patterns = [
        r'(?:https?:\/\/)?(?:www\.)?(?:youtube\.com|youtu\.be)\/(?:watch\?v=)?(?:embed\/)?(?:v\/)?(?:shorts\/)?(?P<id>[^\/\?\&]+)',
        r'(?:https?:\/\/)?(?:www\.)?(?:youtube\.com|youtu\.be)\/(?:watch\?v=)?(?:embed\/)?(?:v\/)?(?:shorts\/)?(?P<id>[^\/\?\&]+).*t=(?P<time>\d+)',
    ]
    
    for pattern in patterns:
        match = re.match(pattern, youtube_url)
        if match:
            return match.group('id')
    
    return None

@st.cache_data
def extract_transcript_details(youtube_video_url):
    """Extract transcript details from a YouTube video."""
    try:
        video_id = extract_video_id(youtube_video_url)
        if not video_id:
            return "Invalid YouTube URL. Unable to extract video ID."
        
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)
        
        transcript = ''
        for i in transcript_text:
            transcript += ' ' + i['text']
        return transcript
    
    except TranscriptsDisabled:
        return "Transcripts are disabled for this video. Unable to generate summary."
    except Exception as e:
        return f"An error occurred: {str(e)}"

@st.cache_data
def generate_gemeni_content(transcript_text, prompt):
    """Generate content using Google's Gemini model."""
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt + transcript_text)
    return response.text

# Streamlit UI
st.title('🎥 YouTube Video Summarizer')
st.markdown("Transform lengthy videos into concise, insightful notes!")

# Input section
st.subheader("📌 Input Your YouTube Video")
youtube_link = st.text_input('Enter the YouTube Video Link:', placeholder="https://www.youtube.com/watch?v=...")

# Display video thumbnail and info
if youtube_link:
    video_id = extract_video_id(youtube_link)
    if video_id:
        col1, col2 = st.columns([2, 1])
        with col1:
            st.image(f'http://img.youtube.com/vi/{video_id}/0.jpg', use_column_width=True)
        with col2:
            st.markdown(f"**Video ID:** {video_id}")
            st.markdown(f"[Open in YouTube](https://www.youtube.com/watch?v={video_id})")
    else:
        st.error("❌ Invalid YouTube URL. Unable to display video thumbnail.")

# Process button
if st.button('🚀 Generate Summary'):
    if not youtube_link:
        st.warning("⚠️ Please enter a YouTube video link first.")
    else:
        with st.spinner('🔍 Extracting video transcript...'):
            transcript_text = extract_transcript_details(youtube_link)
        
        if transcript_text.startswith("Transcripts are disabled") or transcript_text.startswith("An error occurred") or transcript_text.startswith("Invalid YouTube URL"):
            st.error(f"❌ {transcript_text}")
        else:
            with st.spinner('🧠 Generating summary...'):
                summary = generate_gemeni_content(transcript_text, prompt)
                time.sleep(1)  # Simulating processing time for better UX
            
            st.success("✅ Summary generated successfully!")
            
            # Display summary in an expandable section
            with st.expander("📝 View Summary", expanded=True):
                st.markdown(summary)
            
            # Option to download summary
            st.download_button(
                label="📥 Download Summary",
                data=summary,
                file_name="video_summary.txt",
                mime="text/plain"
            )

# Footer
st.markdown("---")
st.markdown("<p align='center' style='animation: pulse 2s infinite;'>Made with ❤️ by AI Enthusiast</p>",
   unsafe_allow_html=True)

st.markdown("""
<style>
@keyframes pulse {
    0% { transform: scale(1); }
    50% { transform: scale(1.3); }
    100% { transform: scale(1); }
}
</style>
""", unsafe_allow_html=True)

# import streamlit as st
# from dotenv import load_dotenv
# import os
# import google.generativeai as genai
# from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
# import re
# import time
# import streamlit.components.v1 as components

# # Load environment variables
# load_dotenv()

# # Configure Google Generative AI
# genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

# # Custom CSS and JS to enhance the UI
# st.markdown("""
# <style>
#     @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');
    
#     body {
#         font-family: 'Roboto', sans-serif;
#         background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
#         color: #333;
#     }
#     .main {
#         background-color: rgba(255,255,255,0.9);
#         padding: 30px;
#         border-radius: 15px;
#         box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
#     }
#     h1 {
#         color: #2c3e50;
#         text-align: center;
#         font-weight: 700;
#         margin-bottom: 30px;
#         text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
#     }
#     .stButton>button {
#         background-color: #3498db;
#         color: white;
#         font-weight: bold;
#         border: none;
#         border-radius: 25px;
#         padding: 12px 24px;
#         text-align: center;
#         text-decoration: none;
#         display: inline-block;
#         font-size: 18px;
#         margin: 10px 2px;
#         transition: all 0.3s ease;
#         box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
#     }
#     .stButton>button:hover {
#         background-color: #2980b9;
#         transform: translateY(-2px);
#         box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15);
#     }
#     .stTextInput>div>div>input {
#         border-radius: 25px;
#         border: 2px solid #3498db;
#         padding: 10px 15px;
#         font-size: 16px;
#         transition: all 0.3s ease;
#     }
#     .stTextInput>div>div>input:focus {
#         border-color: #2980b9;
#         box-shadow: 0 0 0 2px rgba(41, 128, 185, 0.2);
#     }
#     .css-1v3fvcr {
#         background-color: transparent;
#     }
#     .stExpander {
#         background-color: #ffffff;
#         border-radius: 10px;
#         box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
#         margin-bottom: 20px;
#     }
#     .streamlit-expanderHeader {
#         font-weight: bold;
#         color: #2c3e50;
#     }
# </style>
# """, unsafe_allow_html=True)

# # Add custom JavaScript for dynamic effects
# st.markdown("""
# <script>
#     document.addEventListener('DOMContentLoaded', (event) => {
#         // Add hover effect to buttons
#         const buttons = document.querySelectorAll('.stButton button');
#         buttons.forEach(button => {
#             button.addEventListener('mouseover', () => {
#                 button.style.transform = 'scale(1.05)';
#             });
#             button.addEventListener('mouseout', () => {
#                 button.style.transform = 'scale(1)';
#             });
#         });
        
#         // Add typing effect to the title
#         const title = document.querySelector('h1');
#         const text = title.textContent;
#         title.textContent = '';
#         let i = 0;
#         const typeWriter = () => {
#             if (i < text.length) {
#                 title.textContent += text.charAt(i);
#                 i++;
#                 setTimeout(typeWriter, 100);
#             }
#         };
#         typeWriter();
#     });
# </script>
# """, unsafe_allow_html=True)

# # Prompt for the AI model
# prompt = '''
# You are Youtube Video Summarizer. You will be taking the 
# transcript text and summarizing the entire video and 
# providing the important summary in points within 250 words.
# Please provide the summary of text given here:
# '''

# @st.cache_data
# def extract_video_id(youtube_url):
#     """Extract the video ID from various YouTube URL formats."""
#     patterns = [
#         r'(?:https?:\/\/)?(?:www\.)?(?:youtube\.com|youtu\.be)\/(?:watch\?v=)?(?:embed\/)?(?:v\/)?(?:shorts\/)?(?P<id>[^\/\?\&]+)',
#         r'(?:https?:\/\/)?(?:www\.)?(?:youtube\.com|youtu\.be)\/(?:watch\?v=)?(?:embed\/)?(?:v\/)?(?:shorts\/)?(?P<id>[^\/\?\&]+).*t=(?P<time>\d+)',
#     ]
    
#     for pattern in patterns:
#         match = re.match(pattern, youtube_url)
#         if match:
#             return match.group('id')
    
#     return None

# @st.cache_data
# def extract_transcript_details(youtube_video_url):
#     """Extract transcript details from a YouTube video."""
#     try:
#         video_id = extract_video_id(youtube_video_url)
#         if not video_id:
#             return "Invalid YouTube URL. Unable to extract video ID."
        
#         transcript_text = YouTubeTranscriptApi.get_transcript(video_id)
        
#         transcript = ''
#         for i in transcript_text:
#             transcript += ' ' + i['text']
#         return transcript
    
#     except TranscriptsDisabled:
#         return "Transcripts are disabled for this video. Unable to generate summary."
#     except Exception as e:
#         return f"An error occurred: {str(e)}"

# @st.cache_data
# def generate_gemeni_content(transcript_text, prompt):
#     """Generate content using Google's Gemini model."""
#     model = genai.GenerativeModel('gemini-pro')
#     response = model.generate_content(prompt + transcript_text)
#     return response.text

# # Streamlit UI
# st.title('🎥 YouTube Video Summarizer')
# st.markdown("Transform lengthy videos into concise, insightful notes!")

# # Input section with animated placeholder
# youtube_link = st.text_input('Enter the YouTube Video Link:', placeholder="https://www.youtube.com/watch?v=...")

# # Display video thumbnail and info with enhanced styling
# if youtube_link:
#     video_id = extract_video_id(youtube_link)
#     if video_id:
#         col1, col2 = st.columns([2, 1])
#         with col1:
#             st.image(f'http://img.youtube.com/vi/{video_id}/0.jpg', use_column_width=True)
#         with col2:
#             st.markdown(f"**Video ID:** `{video_id}`")
#             st.markdown(f"[🔗 Open in YouTube](https://www.youtube.com/watch?v={video_id})")
#     else:
#         st.error("❌ Invalid YouTube URL. Unable to display video thumbnail.")

# # Process button with loading animation
# if st.button('🚀 Generate Summary', key='generate_button'):
#     if not youtube_link:
#         st.warning("⚠️ Please enter a YouTube video link first.")
#     else:
#         with st.spinner('🔍 Extracting video transcript...'):
#             transcript_text = extract_transcript_details(youtube_link)
        
#         if transcript_text.startswith("Transcripts are disabled") or transcript_text.startswith("An error occurred") or transcript_text.startswith("Invalid YouTube URL"):
#             st.error(f"❌ {transcript_text}")
#         else:
#             with st.spinner('🧠 Generating summary...'):
#                 summary = generate_gemeni_content(transcript_text, prompt)
#                 time.sleep(1)  # Simulating processing time for better UX
            
#             st.success("✅ Summary generated successfully!")
            
#             # Display summary in an expandable section with custom styling
#             with st.expander("📝 View Summary", expanded=True):
#                 st.markdown(f"<div style='background-color: #f0f8ff; padding: 20px; border-radius: 10px; box-shadow: inset 0 0 10px rgba(0,0,0,0.1);'>{summary}</div>", unsafe_allow_html=True)
            
#             # Option to download summary with enhanced button
#             st.download_button(
#                 label="📥 Download Summary",
#                 data=summary,
#                 file_name="video_summary.txt",
#                 mime="text/plain",
#                 key='download_button'
#             )

# # Footer with animation
# st.markdown("---")
# st.markdown(
#     "<p align='center' style='animation: pulse 2s infinite;'>Made with ❤️ by AI Enthusiasts</p>",
#     unsafe_allow_html=True
# )

# Add a pulsing animation
# st.markdown("""
# <style>
# @keyframes pulse {
#     0% { transform: scale(1); }
#     50% { transform: scale(); }
#     100% { transform: scale(1); }
# }
# </style>
# """, unsafe_allow_html=True)

# # # Add a loading animation component
# components.html(
#     """
#     <script src="https://cdn.jsdelivr.net/npm/lottie-web@5.7.14/build/player/lottie.min.js"></script>
#     <div id="lottie-container" style="width: 200px; height: 200px; margin: auto;"></div>
#     <script>
#         var animation = lottie.loadAnimation({
#             container: document.getElementById('lottie-container'),
#             renderer: 'svg',
#             loop: true,
#             autoplay: true,
#             path: 'https://assets2.lottiefiles.com/packages/lf20_szlepvdh.json'
#         });
#     </script>
# #     """
# )