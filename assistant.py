import sounddevice as sd
from scipy.io.wavfile import write
import speech_recognition as sr
import pyttsx3
import wikipedia
import numpy as np

# Initialize text-to-speech engine with a female voice
engine = pyttsx3.init()
voices = engine.getProperty('voices')
for voice in voices:
    if 'female' in voice.name.lower() or 'zira' in voice.id.lower():
        engine.setProperty('voice', voice.id)
        break
engine.setProperty('rate', 150)

def speak(text):
    print("🤖 Assistant:", text)
    engine.say(text)
    engine.runAndWait()

def record_audio(filename="input.wav", duration=5):
    fs = 44100
    print("🎙️ Speak now...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    recording_int16 = np.int16(recording * 32767)
    write(filename, fs, recording_int16)
    print("✅ Recording saved.")

def recognize_speech(filename="input.wav"):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio)
        print("🗣️ You said:", text)
        return text
    except sr.UnknownValueError:
        print("❌ Could not understand the audio.")
        return None
    except sr.RequestError:
        print("❌ Could not connect to the speech recognition service.")
        return None

def clean_query(query):
    query = query.lower()
    for phrase in ["who is", "what is", "tell me about", "define"]:
        query = query.replace(phrase, "")
    return query.strip()

def run_assistant():
    speak("Hello! I am your assistant. Ask me anything. Say 'stop' or 'exit' to quit.")
    while True:
        record_audio()
        query = recognize_speech()
        if query:
            if "stop" in query.lower() or "exit" in query.lower():
                speak("Goodbye!")
                break

            speak("You said: " + query)
            topic = clean_query(query)

            try:
                print(f"🔍 Searching Wikipedia for: '{topic}'")
                search_results = wikipedia.search(topic)
                print(f"🔎 Search results: {search_results}")

                if search_results:
                    best_match = search_results[0]
                    print(f"✅ Best match: {best_match}")
                    summary = wikipedia.summary(best_match, sentences=2)
                    speak(summary)
                else:
                    speak("I couldn’t find anything matching that topic.")
            except wikipedia.exceptions.DisambiguationError as e:
                print(f"⚠️ Disambiguation error: {e}")
                speak("That topic is too broad. Please be more specific.")
            except wikipedia.exceptions.PageError as e:
                print(f"⚠️ Page error: {e}")
                speak("I couldn't find a proper page for that.")
            except Exception as e:
                print(f"⚠️ Unexpected error: {e}")
                speak("Something went wrong while searching.")
        else:
            speak("I didn’t catch that. Please try again.")

if __name__ == "__main__":
    run_assistant()
