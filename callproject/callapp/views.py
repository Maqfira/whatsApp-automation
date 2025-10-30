from django.http import HttpResponse, FileResponse
from gtts import gTTS
from twilio.twiml.voice_response import VoiceResponse
import os

def voice(request):
    # Generate audio from text
    text = "Hello! Thank you for calling our company. Please hold while we connect you."
    tts = gTTS(text)
    tts.save("hello.mp3")
    os.system("ffmpeg -y -i hello.mp3 callapp/static/hello.wav")

    # Create TwiML (XML) response
    response = VoiceResponse()
    response.play("https://your-ngrok-url.ngrok.io/static/hello.wav")  # update this later
    return HttpResponse(str(response), content_type="application/xml")


def serve_audio(request):
    file_path = "callapp/static/hello.wav"
    return FileResponse(open(file_path, 'rb'), content_type="audio/wav")

