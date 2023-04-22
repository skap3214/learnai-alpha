import os
from PyPDF2 import PdfReader, PdfMerger
import whisper_timestamped as whisper
from pytube import YouTube
import ffmpeg
class ToText:
    '''
    to convert a type of file to text, call the type of file as the method name.
    e.g: If you want to convert a youtube video to text:
    ToText.youtube

    Supported file types:
    - youtube
    '''
    API_KEY = "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"
    #create a method called youtube which takes in a URL as a parameter
    def youtube(self,video_URL,timestamp_yes = False, as_string = True):
        '''
        timestamp_yes:
        this param is set to False as default. If you set it as True, the method will return a tuple of two elements(transcript, timestamps)

        as_string:
        this param is set to True as defualt. If you set it as False, the method will return a list of words. otherwise it returns the transcript as a string.
        '''
        output_file = "audio.mp3"
        # Get the YouTube object
        yt = YouTube(video_URL)

        # Download the highest quality audio stream
        audio_stream = yt.streams.filter(only_audio=True, subtype='mp4').first()

        # Download the audio file
        audio_file = audio_stream.download(filename='temp_audio')

        # Convert the downloaded audio file to MP3
        input_audio = ffmpeg.input(audio_file)
        ffmpeg.output(input_audio, output_file, format='mp3').run()
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
                timestamps.append((start,end))
        os.remove("audio.mp3")
        os.remove(audio_file)
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
        #TODO: NOT TESTED
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

