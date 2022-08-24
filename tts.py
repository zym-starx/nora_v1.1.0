import numpy as np
import IPython.display as ipd
import riva.client
from pydub import AudioSegment
from datetime import date, datetime

def tts(query):
    auth = riva.client.Auth(uri='localhost:50051')

    riva_tts = riva.client.SpeechSynthesisService(auth)

    if (query == ""):
        query = "Have you ever heard of 'Among Us', Gregory?"

    now = datetime.now()
    current_date = now.strftime("%d/%m/%y")
    current_time = now.strftime("%H:%M:%S")

    current_date = current_date.replace("/", "-")
    current_time = current_time.replace(":", "-")

    datestr = "noraAnswer_" + current_time + "_" + current_date + ".wav"
    path = "C:/Users/Ömer KAVLAKOĞLU/Desktop/Unreal engine/Nora_v110/Script/nora_v1.1.0/testsounds/" + datestr 

    sample_rate_hz = 44100
    resp = riva_tts.synthesize(
        text = query,
        language_code = "en-US",
        encoding = riva.client.AudioEncoding.LINEAR_PCM,    # Currently only LINEAR_PCM is supported
        sample_rate_hz = sample_rate_hz,                    # Generate 44.1KHz audio
        voice_name = "English-US-Female-1"         # The name of the voice to generate
    )
    audio_samples = np.frombuffer(resp.audio, dtype=np.int16)
    audio_samples = ipd.Audio(audio_samples, rate=sample_rate_hz)
    audio = AudioSegment(audio_samples.data, frame_rate=sample_rate_hz, sample_width=2, channels=1)
    #audio.export("testrun.mp3", format="wav", bitrate="64k")

    #song = AudioSegment("/testsounds/file.mp3", format="mp3")
    audio.export(path, format="wav")

    #with open('/tmp/test.wav', 'wb') as f:
    #    f.write(audio.data)
    return datestr

