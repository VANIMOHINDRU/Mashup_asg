# Mashup Generator Assignment
📌 Overview

This project consists of two required programs:

Program 1: Command Line Mashup Generator

Program 2: Web-Based Mashup Service

The system downloads songs of a given singer from YouTube, extracts audio, trims each to a fixed duration, merges them into a single mashup file, and delivers the result.

# Program 1 — Command Line Mashup
📄 File Name
102303064.py

# How to Run
``` bash
python 102303064.py <SingerName> <NumberOfVideos> <AudioDuration> <OutputFileName>
``` 
📌 Example
``` bash
python 102303064.py "Sharry Maan" 20 30 output.mp3
```

# Constraints

-Number of videos must be greater than 10
-Duration must be greater than 20 seconds
-Proper error handling included for:
-Incorrect arguments
-Invalid input types
-Runtime exceptions

# Functionality

-Downloads N videos of given singer
-Extracts best available audio
-Cuts first Y seconds from each file
-Merges all clips into a single MP3 file

## Program 2 — Web Mashup Service
🖥️ Web App Features

User provides:
-Singer Name
-Number of Videos (>10)
-Duration (>20 sec)
-Valid Email ID

# Output

Mashup is generated
-Compressed into ZIP format
-Sent to the user via email

# Email Delivery

Email validation included
-File sent using SendGrid API
-Error handling implemented


# Deployment

The web application is deployed and accessible online.
Example:

https://your-app-name.onrender.com

# Technologies Used

-Python
-Flask
-yt-dlp
-pydub
-SendGrid API
-HTML

# Installation (For Local Setup)
pip install -r requirements.txt

Run web app:
-python app.py

# Error Handling

-Invalid email detection
-Invalid numeric input detection
-Exception handling for download and email errors
Parameter validation enforced

