from phonikud_tts import Phonikud, phonemize, Piper
import soundfile as sf
from playsound import playsound

phonikud = Phonikud('phonikud-1.0.int8.onnx')
piper = Piper('tts-model.onnx', 'tts-model.config.json')

def speak(text, filename="audio.wav"):
    with_diacritics = phonikud.add_diacritics(text)
    phonemes = phonemize(with_diacritics)
    samples, sample_rate = piper.create(phonemes, is_phonemes=True)
    sf.write(filename, samples, sample_rate)
    playsound(filename)
    print(f"Spoken: {text}")

if __name__ == "__main__":
    speak(""""תופעות טבע רבות שלא היו מובנות לאדם, נחקרו ונעשו מובנות ומוסברות. בתוך כך התבטל ערכם"
של חלק מההסברים אודות האמונה שהיו מקובלים בדורות הקודמים. בעבר, כאשר השמיים נעצרו
ולא ירדו גשמים – החיטה לא צמחה ומאגרי המים התרוקנו, ואנשים מתו ברעב ובצמא. כאשר
התפשטה מגפה – אנשים רבים נפלו חללים, בלא שהיתה להם כמעט דרך להתגונן מפני המוות
שארב להם. גם בשגרת החיים האדם היה חשוף לסכנות חמורות, כנשיכת נחש והתפתחות מחלות
זיהומיות. מתוך מצוקתו פנה האדם אל ה‘ בתפילה שיעזור לו, ואנשי הדת עודדו את האנשים
להתפלל ולקיים מצוות, כדי שה‘ יושיעם""""")
