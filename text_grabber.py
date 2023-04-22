import os
import re
from youtube_transcript_api import YouTubeTranscriptApi
#import whisper_timestamped as whisper
from pytube import YouTube

class ToText:
    '''
    to convert a type of file to text, call the type of file as the method name.
    e.g: If you want to convert a youtube video to text:
    ToText.youtube
    '''
    #create a method called youtube which takes in a URL as a parameter
    # def youtube(self,video_URL,timestamp_yes = False, as_string = True):
    #     '''
    #     timestamp_yes:
    #     this param is set to False as default. If you set it as True, the method will return a tuple of two elements(transcript, timestamps)
    #
    #     as_string:
    #     this param is set to True as defualt. If you set it as False, the method will return a list of words. otherwise it returns the transcript as a string.
    #     '''
    #     #Use pytube to download the audio from the URL
    #     video = YouTube(video_URL)
    #     audio = video.streams.filter(only_audio=True).first()
    #     new_file = "audio" + '.mp3'
    #     audio.download(filename=new_file)
    #     os.rename(new_file, "audio.mp3")
    #     # Load the audio file
    #     audio = whisper.load_audio("audio.mp3")
    #
    #     # Load the pre-trained model
    #     model = whisper.load_model("tiny", device="cpu")
    #
    #     # Transcribe the audio
    #     result = whisper.transcribe(model, audio, language="en")
    #
    #
    #     # Save the result to a JSON file
    #     timestamps = []
    #     transcript = []
    #     segments = result['segments']
    #     for dict in segments:
    #         words = dict['words']
    #         for dict_1 in words:
    #             word = dict_1['text']
    #             start = dict_1['start']
    #             end = dict_1['end']
    #             transcript.append(word)
    #             timestamps.append((start,end))
    #     os.remove("audio.mp3")
    #     if as_string:
    #         transcript = " ".join(transcript)
    #     if timestamp_yes:
    #         return transcript, timestamps
    #     else:
    #         return transcript

    def yt_transcript(self, url):
        """
        Takes a URL to a YouTube video and returns the transcript text.
        """
        pattern = r"(?:/|%3D|v=)([0-9A-Za-z_-]{11})(?:[%#?&]|$)"
        match = re.search(pattern, url)
        if match:
            video_id = match.group(1)
        else:
            print("Error: Invalid YouTube URL.")
            return False

        transcript = YouTubeTranscriptApi.get_transcript(str(video_id).strip(),
                                                         languages=["en", "en-GB", "en-US"])
        corpus = " ".join([t["text"] for t in transcript])
        return corpus

