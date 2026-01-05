from fastapi import FastAPI, WebSocket
from phonikud_tts import Phonikud, phonemize, Piper
import soundfile as sf
import re
import os

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

@app.websocket("/ws/tts")
async def websocket_tts(websocket: WebSocket):
    await websocket.accept()
    while True:
        text = await websocket.receive_text()
        filename = speak(text)
        await websocket.send_text(f"Audio generated: {filename}")



# from phonikud_tts import Phonikud, phonemize, Piper
# import soundfile as sf , re
# from playsound import playsound
#
# phonikud = Phonikud('phonikud-1.0.int8.onnx')
# piper_he = Piper('tts-model.onnx', 'tts-model.config.json')
#
# # English pipeline
# piper_en = Piper("en_US-amy-medium.onnx", "en_US-amy-medium.onnx.json")
#
# def is_hebrew(text):
#     return re.search(r'[\u0590-\u05FF]', text) is not None
#
#
# def speak(text, filename="audio.wav"):
#     if is_hebrew(text):
#         # Hebrew flow
#         with_diacritics = phonikud.add_diacritics(text)
#         phonemes = phonemize(with_diacritics)
#         samples, sample_rate = piper_he.create(phonemes, is_phonemes=True)
#     else:
#         # English flow
#         samples, sample_rate = piper_en.create(text, is_phonemes=False)
#
#     sf.write(filename, samples, sample_rate)
#     playsound(filename)
#     print(f"Spoken: {text}")
#
# if __name__ == "__main__":
#     #speak("שלום עולם! מה קורה?", "hebrew.wav")
#     speak("Hello world! How are you today? , i am an voice assistant for your help how can i help you today?", "english.wav")






# from phonikud_tts import Phonikud, phonemize, Piper
# import soundfile as sf
# from playsound import playsound
#
# phonikud = Phonikud('phonikud-1.0.int8.onnx')
# piper = Piper('tts-model.onnx', 'tts-model.config.json')
#
# def speak(text, filename="audio.wav"):
#     with_diacritics = phonikud.add_diacritics(text)
#     phonemes = phonemize(with_diacritics)
#     samples, sample_rate = piper.create(phonemes, is_phonemes=True)
#     sf.write(filename, samples, sample_rate)
#     playsound(filename)
#     print(f"Spoken: {text}")
#
# if __name__ == "__main__":
#     speak(""""תופעות טבע רבות שלא היו מובנות לאדם, נחקרו ונעשו מובנות ומוסברות. בתוך כך התבטל ערכם"
# של חלק מההסברים אודות האמונה שהיו מקובלים בדורות הקודמים. בעבר, כאשר השמיים נעצרו
# ולא ירדו גשמים – החיטה לא צמחה ומאגרי המים התרוקנו, ואנשים מתו ברעב ובצמא. כאשר
# התפשטה מגפה – אנשים רבים נפלו חללים, בלא שהיתה להם כמעט דרך להתגונן מפני המוות
# שארב להם. גם בשגרת החיים האדם היה חשוף לסכנות חמורות, כנשיכת נחש והתפתחות מחלות
# זיהומיות. מתוך מצוקתו פנה האדם אל ה‘ בתפילה שיעזור לו, ואנשי הדת עודדו את האנשים
# להתפלל ולקיים מצוות, כדי שה‘ יושיעם""""")
