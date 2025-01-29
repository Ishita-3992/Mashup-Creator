## Python-based Mashup Creator

### Objective:

The primary goal of this project is to create a system that automates the process of downloading multimedia content from YouTube, converting it into audio, trimming it to a specific duration, and then merging multiple audio clips into a single audio mashup.

### Features:

Video Download: Downloads videos from YouTube using a specified URL.
Audio Conversion: Converts downloaded videos into audio files.
Trim Audio: Allows trimming of audio to a specified duration.
Merge Audio: Combines multiple trimmed audio files into a single audio mashup.
Email Delivery: The final audio mashup can be sent to the user via email.

### Technologies Used:

Python: The core language for building the functionality.
Pytube: Library used to download videos from YouTube.
MoviePy: Library used to handle video and audio processing (conversion, trimming, and merging).
Flask: For creating a web interface to interact with the system.
Email Libraries: For sending the final audio mashup via email.

### How It Works:

Download Video: The user provides a YouTube video URL, and the video is downloaded.
Convert to Audio: The downloaded video is converted into an audio file (MP3).
Trim Audio: The user specifies the start and end times, and the audio file is trimmed accordingly.
Merge Audio: Multiple trimmed audio files are merged into one final audio mashup.
Email: The final mashup file is emailed to the user.

### Conclusion:
This project provides an automated solution to create custom audio mashups from YouTube videos, saving users the time and effort of manually downloading, trimming, and merging the content.
