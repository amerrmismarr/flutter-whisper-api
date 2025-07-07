import pyaudio
import wave
import requests
import time
import os

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "temp.wav"

def record_audio():
    print("🔊 Starting audio recording setup...")
    try:
        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
    except Exception as e:
        print(f"❌ Error initializing microphone: {e}")
        return False

    print("🎙️ * recording")
    frames = []

    try:
        for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)
    except Exception as e:
        print(f"❌ Error during recording: {e}")
        stream.stop_stream()
        stream.close()
        p.terminate()
        return False

    print("✅ * done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    try:
        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
    except Exception as e:
        print(f"❌ Error saving WAV file: {e}")
        return False

    return True

def send_to_server():
    if not os.path.exists(WAVE_OUTPUT_FILENAME):
        print("⚠️ No audio file to send.")
        return

    try:
        with open(WAVE_OUTPUT_FILENAME, "rb") as f:
            response = requests.post("http://127.0.0.1:8000/transcribe", files={"file": f})
        print("📝 Transcription:", response.json().get("text"))
    except Exception as e:
        print(f"❌ Error sending to server: {e}")

print("🚀 Starting audio loop...")

while True:
    print("\n⏳ New cycle...")
    if record_audio():
        send_to_server()
    else:
        print("⚠️ Skipping server send due to recording error.")
    time.sleep(1)
