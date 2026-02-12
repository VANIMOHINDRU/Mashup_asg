from flask import Flask, render_template, request
import os
import zipfile
import shutil
import base64
from yt_dlp import YoutubeDL
from pydub import AudioSegment

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition

app = Flask(__name__)

# --------------------------------------------------
# CREATE MASHUP (UNCHANGED LOGIC)
# --------------------------------------------------
def create_mashup(singer, num_videos, duration):

    shutil.rmtree("audios", ignore_errors=True)
    os.makedirs("audios", exist_ok=True)

    if os.path.exists("mashup.mp3"):
        os.remove("mashup.mp3")
    if os.path.exists("mashup.zip"):
        os.remove("mashup.zip")

    def duration_filter(info, *, incomplete):
        if info.get("duration") and info["duration"] > 300:
            return "Video too long"
        return None

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'audios/%(title)s.%(ext)s',
        'quiet': True,
        'noplaylist': True,
        'match_filter': duration_filter
    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([f"ytsearch{num_videos}:{singer} songs"])

    merged = AudioSegment.empty()

    for file in os.listdir("audios"):
        if file.endswith((".webm", ".m4a", ".mp3")):
            path = os.path.join("audios", file)
            audio = AudioSegment.from_file(path)
            merged += audio[:duration * 1000]

    merged.export("mashup.mp3", format="mp3")

    with zipfile.ZipFile("mashup.zip", 'w') as zipf:
        zipf.write("mashup.mp3")

    return "mashup.zip"


# --------------------------------------------------
# SEND EMAIL (FIXED FOR RENDER)
# --------------------------------------------------
def send_email(receiver, zip_file):

    try:
        api_key = os.environ.get("SENDGRID_API_KEY")
        sender = os.environ.get("EMAIL_SENDER")

        message = Mail(
            from_email=sender,
            to_emails=receiver,
            subject="Your Mashup File",
            html_content="<strong>Please find your mashup attached.</strong>"
        )

        with open(zip_file, "rb") as f:
            data = f.read()
            encoded_file = base64.b64encode(data).decode()

        attachment = Attachment(
            FileContent(encoded_file),
            FileName("mashup.zip"),
            FileType("application/zip"),
            Disposition("attachment")
        )

        message.attachment = attachment

        sg = SendGridAPIClient(api_key)
        sg.send(message)

        return True

    except Exception as e:
        print("Email failed:", e)
        return False


# --------------------------------------------------
# ROUTE (UNCHANGED)
# --------------------------------------------------
@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":
        try:
            singer = request.form["singer"]
            num_videos = int(request.form["videos"])
            duration = int(request.form["duration"])
            email = request.form["email"]

            if num_videos < 3:
                return "Minimum 3 videos required."

            if duration < 15:
                return "Minimum 15 seconds required."

            zip_file = create_mashup(singer, num_videos, duration)

            if send_email(email, zip_file):
                return "Mashup created and email sent successfully!"
            else:
                return "Mashup created, but email failed."

        except Exception as e:
            return f"Error occurred: {str(e)}"

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
