
import requests
def ttsmaker_speak(text):
    try:
        res = requests.post("https://api.ttsmaker.com/v1/create-tts-order", json={
            "text": text,
            "voice_id": "en-US-SamanthaNeural",
            "lang": "en",
            "speed": 1.0,
            "audio_format": "mp3"
        })
        return res.json().get("audio_url", None)
    except:
        return None

