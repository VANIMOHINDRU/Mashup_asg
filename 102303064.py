import sys
import os
import shutil
from yt_dlp import YoutubeDL
from pydub import AudioSegment

# --------------------------------------------------
# CREATE MASHUP FUNCTION
# --------------------------------------------------
def create_mashup(singer, num_videos, duration, output_file):

    # Remove old folder if exists
    shutil.rmtree("audios", ignore_errors=True)
    os.makedirs("audios", exist_ok=True)

    # Filter videos longer than 5 minutes
    def duration_filter(info, *, incomplete):
        if info.get("duration") and info["duration"] > 300:
            return "Video too long"
        return None

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'audios/%(title)s.%(ext)s',
        'quiet': False,
        'noplaylist': True,
        'match_filter': duration_filter
    }

    # Download videos
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([f"ytsearch{num_videos}:{singer} songs"])

    merged = AudioSegment.empty()

    # Convert + cut + merge
    for file in os.listdir("audios"):
        if file.endswith((".webm", ".m4a", ".mp3")):
            path = os.path.join("audios", file)
            audio = AudioSegment.from_file(path)
            merged += audio[:duration * 1000]

    # Export final output
    merged.export(output_file, format="mp3")

    print(f"\nMashup created successfully: {output_file}")


# --------------------------------------------------
# MAIN PROGRAM
# --------------------------------------------------
if __name__ == "__main__":

    # Check number of parameters
    if len(sys.argv) != 5:
        print("Usage: python <program.py> <SingerName> <NumberOfVideos> <AudioDuration> <OutputFileName>")
        sys.exit(1)

    try:
        singer = sys.argv[1]
        num_videos = int(sys.argv[2])
        duration = int(sys.argv[3])
        output_file = sys.argv[4]

        # Assignment constraints
        if num_videos <= 10:
            print("Error: Number of videos must be greater than 10.")
            sys.exit(1)

        if duration <= 20:
            print("Error: Duration must be greater than 20 seconds.")
            sys.exit(1)

        create_mashup(singer, num_videos, duration, output_file)

    except ValueError:
        print("Error: Number of videos and duration must be integers.")
        sys.exit(1)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        sys.exit(1)
