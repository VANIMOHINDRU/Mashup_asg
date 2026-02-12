from flask import Flask, render_template, request
import os
import zipfile
import smtplib
import shutil
from email.message import EmailMessage
from yt_dlp import YoutubeDL
from pydub import AudioSegment

app = Flask(__name__)

# --------------------------------------------------
# CREATE MASHUP
# --------------------------------------------------
def create_mashup(singer, num_videos, duration):

    # Clean previous files
    shutil.rmtree("audios", ignore_errors=True)
    os.makedirs("audios", exist_ok=True)

    if os.path.exists("mashup.mp3"):
        os.remove("mashup.mp3")
    if os.path.exists("mashup.zip"):
        os.remove("mashup.zip")

    # Download audio only + limit duration
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'audios/%(title)s.%(ext)s',
        'quiet': True,
        'noplaylist': True,
        'match_filter': 'duration < 300'   # avoid 2 hour videos
    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([f"ytsearch{num_videos}:{singer} songs"])

    merged = AudioSegment.empty()

    for file in os.listdir("audios"):
        if file.endswith((".webm", ".m4a", ".mp3")):
            path = os.path.join("audios", file)
            audio = AudioSegment.from_file(path)
            merged += audio[:duration * 1000]

    output_file = "mashup.mp3"
    merged.export(output_file, format="mp3")

    # Create zip
    zip_name = "mashup.zip"
    with zipfile.ZipFile(zip_name, 'w') as zipf:
        zipf.write(output_file)

    return zip_name


# --------------------------------------------------
# SEND EMAIL
# --------------------------------------------------
def send_email(receiver, zip_file):

    sender = os.environ.get("EMAIL_SENDER")
    password = os.environ.get("EMAIL_PASSWORD")

    try:
        msg = EmailMessage()
        msg['Subject'] = "Your Mashup File"
        msg['From'] = sender
        msg['To'] = receiver
        msg.set_content("Please find your mashup attached.")

        with open(zip_file, 'rb') as f:
            msg.add_attachment(
                f.read(),
                maintype='application',
                subtype='zip',
                filename=zip_file
            )

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender, password)
            smtp.send_message(msg)

        return True

    except Exception as e:
        print("Email failed:", e)
        return False


# --------------------------------------------------
# ROUTE
# --------------------------------------------------
@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":
        try:
            singer = request.form["singer"]
            num_videos = int(request.form["videos"])
            duration = int(request.form["duration"])
            email = request.form["email"]

            # Cloud-safe validation
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
