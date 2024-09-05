import os
import torch
from openvoice import se_extractor
from openvoice.api import ToneColorConverter
from melo.api import TTS


ckpt_converter = 'checkpoints_v2/converter'
device = "cuda:0" if torch.cuda.is_available() else "cpu"
output_dir = 'outputs_api'

tone_color_converter = ToneColorConverter(f'{ckpt_converter}/config.json', device=device)
tone_color_converter.load_ckpt(f'{ckpt_converter}/checkpoint.pth')

os.makedirs(output_dir, exist_ok=True)

RESOURCE_FILE = 'divesh-voice.wav'
reference_speaker = './resources/' + RESOURCE_FILE # This is the voice whose tone is to be used

target_se, audio_name = se_extractor.get_se(reference_speaker, tone_color_converter, vad=False)

# Speed is adjustable

model = TTS(language='EN', device=device)
source_se = torch.load(f'checkpoints_v2/base_speakers/ses/en-br.pth', map_location=device)

def generate_voice(text, speed, filename):
    model.tts_to_file(text, 1, 'outputs_api/temp.wav', speed=speed)
    save_path = f'{output_dir}/{filename}.wav'

    encode_message = "@MyShell"
    tone_color_converter.convert(
        audio_src_path='outputs_api/temp.wav', 
        src_se=source_se, 
        tgt_se=target_se, 
        output_path=save_path,
        message=encode_message)
    return save_path

if __name__ == '__main__':
    generate_voice('''Hello! . Welcome to Nottingham Trent University's Open Day. I am a work in progress for the Real-time Open-day Bot for Information and Navigation, but you can call me ROBIN for short. I am an artificially intelligent chatbot and I am here to help you! I know all sorts of information about Nottingham,
    Nottingham Trent University, and the Department of Computer Science. Ask me any question and I will do my best to help you.''', 0.87, 'myshell')