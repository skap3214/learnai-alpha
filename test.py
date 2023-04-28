"https://www.youtube.com/watch?v=Cmv1Q5GwqJU&ab_channel=CatharynBaird"

#extract transcript from youtube video

from text_grabber import Text

text_grabber = Text()

transcript = text_grabber.youtube("https://www.youtube.com/watch?v=Cmv1Q5GwqJU&ab_channel=CatharynBaird")

print(transcript)