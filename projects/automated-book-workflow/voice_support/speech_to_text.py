import os
import io
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
from google.cloud import speech
from google.cloud import texttospeech
import pyttsx3
from dotenv import load_dotenv

load_dotenv()

# Set up Google credentials (expects GOOGLE_APPLICATION_CREDENTIALS env var)
CHAPTER_PATH = os.path.join("output", "chapter_spun.txt")
AUDIO_FILE = "user_feedback.wav"
SAMPLE_RATE = 16000
DURATION = 10  # seconds

def record_audio(filename=AUDIO_FILE, duration=DURATION, fs=SAMPLE_RATE):
    print(f"Recording for {duration} seconds...")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()
    wav.write(filename, fs, audio)
    print(f"Audio saved to {filename}")
    return filename

def transcribe_audio(filename=AUDIO_FILE):
    client = speech.SpeechClient()
    with io.open(filename, "rb") as audio_file:
        content = audio_file.read()
    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=SAMPLE_RATE,
        language_code="en-US",
    )
    response = client.recognize(config=config, audio=audio)
    transcript = " ".join([result.alternatives[0].transcript for result in response.results])
    print(f"Transcript: {transcript}")
    return transcript

def read_chapter_tts(path=CHAPTER_PATH, use_pyttsx3=True):
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    if use_pyttsx3:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    else:
        tts_client = texttospeech.TextToSpeechClient()
        synthesis_input = texttospeech.SynthesisInput(text=text)
        voice = texttospeech.VoiceSelectionParams(language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL)
        audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.LINEAR16)
        response = tts_client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
        with open("chapter_tts.wav", "wb") as out:
            out.write(response.audio_content)
        print("Playing chapter_tts.wav...")
        sd.play(wav.read("chapter_tts.wav")[1], SAMPLE_RATE)
        sd.wait()

def main():
    # Read out the latest chapter
    print("Reading out the latest chapter...")
    read_chapter_tts()
    # Record and transcribe feedback
    print("Please provide your audio feedback after the beep...")
    record_audio()
    transcribe_audio()

if __name__ == "__main__":
    main()
