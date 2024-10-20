from flask import Flask, render_template, request, send_file, redirect, url_for, flash
import os
import shutil
from pytube import Search
from moviepy.editor import VideoFileClip
from pydub import AudioSegment
import zipfile
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Function to download videos
def download_videos(singer_name, num_videos):
    search = Search(singer_name)
    videos = search.results[:num_videos]
    video_files = []
    
    if not os.path.exists('videos'):
        os.makedirs('videos')
    
    for i, video in enumerate(videos):
        stream = video.streams.filter(only_audio=False).first()
        video_path = stream.download(output_path='videos', filename=f"video_{i}.mp4")
        video_files.append(video_path)
    
    return video_files

# Function to convert video to audio and cut it
def convert_and_cut_videos(video_files, audio_duration):
    if not os.path.exists('audio'):
        os.makedirs('audio')
    
    audio_files = []
    for i, video_file in enumerate(video_files):
        video = VideoFileClip(video_file)
        audio_file = f"audio/audio_{i}.mp3"
        video.audio.write_audiofile(audio_file)
        
        audio = AudioSegment.from_mp3(audio_file)
        cut_audio = audio[:audio_duration * 1000]
        cut_audio.export(audio_file, format="mp3")
        audio_files.append(audio_file)
    
    return audio_files

# Function to merge audios
def merge_audios(audio_files, output_filename):
    combined = AudioSegment.from_mp3(audio_files[0])
    for audio_file in audio_files[1:]:
        next_audio = AudioSegment.from_mp3(audio_file)
        combined += next_audio
    combined.export(output_filename, format="mp3")

# Function to zip the output file
def zip_output(output_filename):
    zip_filename = "mashup.zip"
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        zipf.write(output_filename, os.path.basename(output_filename))
    return zip_filename

# Function to send the zipped file via email
def send_email(email_id, zip_filename):
    from_email = "isha.garg0821@gmail.com.com"
    from_password = "Dps@15126"
    
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = email_id
    msg['Subject'] = 'Mashup Audio'
    
    part = MIMEBase('application', 'octet-stream')
    with open(zip_filename, 'rb') as file:
        part.set_payload(file.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename={zip_filename}')
    msg.attach(part)
    
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(from_email, from_password)
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False

# Route for home page
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle the form submission
@app.route('/create_mashup', methods=['POST'])
def create_mashup():
    singer_name = request.form['singer_name']
    num_videos = int(request.form['num_videos'])
    audio_duration = int(request.form['audio_duration'])
    email_id = request.form['email_id']
    
    # Step 1: Download the videos
    video_files = download_videos(singer_name, num_videos)
    if not video_files:
        flash("No videos found or unable to download.")
        return redirect(url_for('index'))
    
    # Step 2: Convert and cut the videos to audio
    audio_files = convert_and_cut_videos(video_files, audio_duration)
    
    # Step 3: Merge the audios into a single file
    output_filename = "mashup_output.mp3"
    merge_audios(audio_files, output_filename)
    
    # Step 4: Zip the output file
    zip_filename = zip_output(output_filename)
    
    # Step 5: Send the email
    if send_email(email_id, zip_filename):
        flash(f"Mashup created and sent to {email_id} successfully!")
    else:
        flash("Failed to send email.")
    
    # Cleanup
    shutil.rmtree('videos')
    shutil.rmtree('audio')
    
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
