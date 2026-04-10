from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
from dotenv import load_dotenv
import xml.etree.ElementTree as ET

load_dotenv()

video_id = "X0btK9X0Xnk"  # Gangnam Style

try:
    transcripts = YouTubeTranscriptApi.list_transcripts(video_id)

    try:
        transcript = transcripts.find_manually_created_transcript(["hi"])
    except:
        transcript = transcripts.find_generated_transcript(["hi"])

    data = transcript.fetch()
    text = " ".join(item["text"] for item in data)

    print("✅ Transcript fetched successfully\n")
    print(text[:1000])

except ET.ParseError:
    print("❌ YouTube blocked transcript XML (rate-limit / bot protection)")

except Exception as e:
    print("❌ Transcript not available:", e)
