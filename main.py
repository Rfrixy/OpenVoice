from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
import wave
import numpy as np
import os

import sys
import os

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Add the current directory to the Python path
sys.path.append(current_dir)


import voicegen


app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

def generate_wav(frequency: float, duration: float, filename: str):
    # Sampling rate
    sample_rate = 44100
    
    # Generate the waveform data
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    audio = 0.5 * np.sin(2 * np.pi * frequency * t)
    
    # Ensure the audio data is in the correct format
    audio = (audio * 32767).astype(np.int16)
    
    # Write the waveform data to a WAV file
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
    # Generate the WAV file
    filename = "output.wav"
    generate_wav(frequency, duration, filename)
    
    # Return the WAV file as a response
    return FileResponse(filename, media_type='audio/wav', filename=filename)

@app.get("/generate-voice/")    
async def generate_voice_file(
    text = Query(..., title="text", description="Frequency of the sine wave in Hz"),
):
    # Generate the WAV file
    filename = "output.wav"
    output_file_src = voicegen.generate_voice(text, 1, filename)
    # Return the WAV file as a response
    return FileResponse(output_file_src, media_type='audio/wav', filename=filename)