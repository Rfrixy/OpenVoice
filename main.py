from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
import wave
import numpy as np
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)


import voicegen


app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

def generate_wav(frequency: float, duration: float, filename: str):
    sample_rate = 44100
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    audio = 0.5 * np.sin(2 * np.pi * frequency * t)
    audio = (audio * 32767).astype(np.int16)
    with wave.open(filename, 'wb') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 2 bytes per sample
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(audio.tobytes())


@app.get("/generate-wav/")
async def generate_wav_file(
    frequency: float = Query(..., title="Frequency", description="Frequency of the sine wave in Hz"),
    duration: float = Query(..., title="Duration", description="Duration of the sine wave in seconds")
):
    filename = "output.wav"
    generate_wav(frequency, duration, filename)
    return FileResponse(filename, media_type='audio/wav', filename=filename)

@app.get("/generate-voice/")    
async def generate_voice_file(
    text = Query(..., title="text", description="Frequency of the sine wave in Hz"),
):
    filename = "output.wav"
    output_file_src = voicegen.generate_voice(text, 0.87, filename)
    return FileResponse(output_file_src, media_type='audio/wav', filename=filename)