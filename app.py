import asyncio
import re
from fastapi import FastAPI, WebSocket
from phonikud_tts import Phonikud, phonemize, Piper
import soundfile as sf

app = FastAPI()

# Hebrew pipeline
phonikud = Phonikud("phonikud-1.0.int8.onnx")
piper_he = Piper("tts-model.onnx", "tts-model.config.json")

# English pipeline
piper_en = Piper("en_US-amy-medium.onnx", "en_US-amy-medium.onnx.json")

def is_hebrew(text):
    return re.search(r'[\u0590-\u05FF]', text) is not None

def speak(text, filename="output.wav"):
    if is_hebrew(text):
        with_diacritics = phonikud.add_diacritics(text)
        phonemes = phonemize(with_diacritics)
        samples, sample_rate = piper_he.create(phonemes, is_phonemes=True)
    else:
        samples, sample_rate = piper_en.create(text, is_phonemes=False)

    sf.write(filename, samples, sample_rate)
    return filename

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    try:
        while True:
            text = await ws.receive_text()
            filename = speak(text)
            await ws.send_json({
                "status": "success",
                "message": f"Audio generated: {filename}"
            })
    except Exception as e:
        await ws.send_json({
            "status": "error",
            "message": str(e)
        })
        await ws.close()
