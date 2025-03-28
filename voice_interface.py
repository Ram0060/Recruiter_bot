from gtts import gTTS
import os
import tempfile
import platform
import speech_recognition as sr
from faster_whisper import WhisperModel


def speak_text(text: str, lang="en"):
    """
    Converts text to speech and plays it.

    Parameters:
        text (str): The text to speak
        lang (str): Language code (default: "en")
    """
    # Generate speech from text using Google TTS
    tts = gTTS(text=text, lang=lang)

    # Save the audio to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        temp_audio_path = fp.name
        tts.save(temp_audio_path)

    # 🔊 Play the audio file based on OS
    if platform.system() == "Darwin":  # macOS
        os.system(f"afplay {temp_audio_path}")
    elif platform.system() == "Linux":
        os.system(f"mpg123 {temp_audio_path}")
    elif platform.system() == "Windows":
        os.system(f'start {temp_audio_path}')
    # Note: No cleanup here — temp file will persist unless manually removed.


def transcribe_speech(model_size="small") -> str:
    """
    Records audio from the microphone and transcribes it using Fast Whisper.
    
    Parameters:
        model_size (str): Size of the Whisper model to use (default: "small")
    
    Returns:
        str: The transcribed text from the user's speech.
    """
    recognizer = sr.Recognizer()
    recognizer.pause_threshold = 1.8  # Slight pause before auto-cutoff

    with sr.Microphone() as source:
        print("🎙️ Calibrating mic for background noise... Please wait.")
        recognizer.adjust_for_ambient_noise(source, duration=1.2)
        print("✅ Mic ready! Please speak your answer now.")

        try:
            # Record audio input with timeouts to prevent hanging
            # 5s timeout to start speaking, 15s max per response
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=15)
        except sr.WaitTimeoutError:
            print("❌ Timed out waiting for your voice. Try speaking sooner next time.")
            return ""

    # Save the captured audio to disk for Whisper
    with open("temp_audio.wav", "wb") as f:
        f.write(audio.get_wav_data())

    # Load the Fast Whisper model
    model = WhisperModel(model_size)

    # Transcribe audio to text
    segments, _ = model.transcribe("temp_audio.wav")
    transcript = " ".join([segment.text for segment in segments])

    print(f"📝 Transcribed Text: {transcript}")
    return transcript
