## Install instructions

1. Create a venv
2. Make sure requirements.txt and requirements2.txt are both installed
3. ensure you have ffmeg installed - on windows, you can use chocolatey: https://chocolatey.org/install https://community.chocolatey.org/packages/ffmpeg
4. ffmpeg should also be on the sys path after installation
5. Make sure you add checkpointsv2 to the directory as outlined here https://github.com/myshell-ai/OpenVoice/blob/main/docs/USAGE.md#openvoice-v2, you also need checkpoints if you want openvoice v1
6. Run `python -m unidic download`
https://github.com/Alienpups/OpenVoice/blob/main/docs/USAGE_WINDOWS.md
7. Run `fastapi dev main.py` to run the voice generation server locally or `fastpi run main.py` to serve it
8. After 'Application startup complete' visit http://localhost:8000/ to confirm hello world response
9. Optionally deploy or use ngrok to serve locally & update the main hub code to use this api
