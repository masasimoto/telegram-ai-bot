import requests

def ttsmaker_speak(text):
    try:
        response = requests.post("https://api.ttsmaker.com/v1/create-tts-order", json={
            "Text": text,
            "VoiceType": "id-ID-ArdiNeural",  # suara cowok formal
            "Lang": "id-ID",
            "Rate": 1,
            "Volume": 0,
            "Pitch": 1,
            "BackgroundSound": "",
            "AudioFormat": "mp3"
        }, timeout=30)

        res = response.json()
        return res.get("DownloadUrl")
    except Exception as e:
        print(f"[TTS ERROR] {e}")
        return None
