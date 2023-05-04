import os
import re
from PyPDF2 import PdfReader, PdfMerger
import whisper_timestamped as whisper
from pytube import YouTube
import ffmpeg
import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
import subprocess
from moviepy.editor import *
class Text:
    '''
    to convert a type of file to text, call the type of file as the method name.
    e.g: If you want to convert a youtube video to text:
    ToText.youtube

    Supported file types:
    - youtube
    '''
    API_KEY = st.secrets["OPENAI_API_KEY"]
    #create a method called youtube which takes in a URL as a parameter
    def youtube(self, video_url):
        '''
        video_url:
        this param is a youtube video url.
        '''
        try:
            return self._caption_youtube(video_url)
        except:
            return self._whispter_youtube(video_url)
    def _extract_youtube_id(self, video_url):
        if "youtube" not in video_url:
            raise ValueError("Invalid YouTube URL")
        youtube_id = re.search(r'v=([^&]+)', video_url).group(1)
        return youtube_id.strip()

    def _get_text_timed(self, youtube_id):
        try:
            return YouTubeTranscriptApi.get_transcript(youtube_id, languages=['en', 'en-GB', 'en-US'])
        except:
            raise ValueError("Unable to transcribe YouTube URL")

    def _timed_to_string(self, timed_text):
        return ' '.join([t['text'] for t in timed_text])

    def _caption_youtube(self, video_url):
        youtube_id = self._extract_youtube_id(video_url)
        timed_text = self._get_text_timed(youtube_id)
        return self._timed_to_string(timed_text)

    def _whispter_youtube(self,video_url,timestamp_yes = False, as_string = True):
        '''
        timestamp_yes:
        this param is set to False as default. If you set it as True, the method will return a tuple of two elements(transcript, timestamps)

        as_string:
        this param is set to True as defualt. If you set it as False, the method will return a list of words. otherwise it returns the transcript as a string.
        '''
        output_filename = "audio.mp3"
        command = f'python3 -m pip install --force-reinstall https://github.com/yt-dlp/yt-dlp/archive/master.tar.gz && yt-dlp -x --audio-format mp3 -o "{output_filename}" {video_url}'
        subprocess.call(command, shell=True)
        
        # Load the audio file
        audio = whisper.load_audio("audio.mp3")

        # Load the pre-trained model
        model = whisper.load_model("tiny", device="cpu")

        # Transcribe the audio
        result = whisper.transcribe(model, audio, language="en")

        # Save the result to a JSON file
        timestamps = []
        transcript = []
        segments = result['segments']
        for dict in segments:
            words = dict['words']
            for dict_1 in words:
                word = dict_1['text']
                start = dict_1['start']
                end = dict_1['end']
                transcript.append(word)
                timestamps.append((start, end))

        os.remove("audio.mp3")

        if as_string:
            transcript = " ".join(transcript)

        if timestamp_yes:
            return transcript, timestamps
        else:
            return transcript
    
    def mp4(self,video_name,timestamp_yes = False, as_string = True):
        video = VideoFileClip(video_name)
        audio = video.audio
        audio.write_audiofile("audio.mp3")
        audio = whisper.load_audio("audio.mp3")

        # Load the pre-trained model
        model = whisper.load_model("tiny", device="cpu")

        # Transcribe the audio
        result = whisper.transcribe(model, audio, language="en")

        # Save the result to a JSON file
        timestamps = []
        transcript = []
        segments = result['segments']
        for dict in segments:
            words = dict['words']
            for dict_1 in words:
                word = dict_1['text']
                start = dict_1['start']
                end = dict_1['end']
                transcript.append(word)
                timestamps.append((start, end))

        os.remove("audio.mp3")

        if as_string:
            transcript = " ".join(transcript)

        if timestamp_yes:
            return transcript, timestamps
        else:
            return transcript

    def pdf(self,pdf_list):
        '''
        pdf_list:
        this param is a list of pdf files.
        '''
        merger = PdfMerger()
        
        for pdf in pdf_list:
            merger.append(pdf)
        merger.write("merged.pdf")
        merged_pdf = "merged.pdf"
        reader = PdfReader(merged_pdf)
        raw_text = ''
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if text:
                raw_text += text
        return raw_text

