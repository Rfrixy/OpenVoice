##..##..##..##..##..##...####...######..#####..
##..##..###.##..##..##..##......##......##..##.
##..##..##.###..##..##...####...####....##..##.
##..##..##..##..##..##......##..##......##..##.
 ####...##..##...####....####...######..#####..

### THIS IS AN UNUSED TEST FILE THAT WAS USED TO TEST CHATTTS ###

# Import necessary libraries and configure settings
import torch
import torchaudio
torch._dynamo.config.cache_size_limit = 64
torch._dynamo.config.suppress_errors = True
torch.set_float32_matmul_precision('high')

import ChatTTS
from IPython.display import Audio

# Initialize and load the model: 
chat = ChatTTS.Chat()
chat.load(compile=True,) # Set to True for better performance

# Define the text input for inference (Support Batching)
texts = [
    "Hello I am a work in progress chatbot for Nottingham Trent University",
    ]


rand_spk = chat.sample_random_speaker()
print(rand_spk) # save it for later timbre recovery

params_infer_code = ChatTTS.Chat.InferCodeParams(
    spk_emb = rand_spk, # add sampled speaker 
    temperature = .3,   # using custom temperature
    top_P = 0.7,        # top P decode
    top_K = 20,         # top K decode
)


# Perform inference and play the generated audio
wavs = chat.infer(texts,
                  params_infer_code=params_infer_code,)
Audio(wavs[0], rate=24_000, autoplay=True)

# Save the generated audio 
torchaudio.save("chattsoutput.wav", torch.from_numpy(wavs[0]), 24000)