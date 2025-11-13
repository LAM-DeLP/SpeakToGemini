from scipy.io.wavfile import write
import sounddevice as sd
from gtts import gTTS
import numpy as np
import os
os.environ["PATH"] += os.pathsep + r"ffmpeg-7.1.1\\bin"
import whisper
model = whisper.load_model("base") #MyGPU is 'NVIDIA GeForce RTX 3060 Laptop GPU' cuda 10.0~13.0 avialable
class AudioRecorder:
    def __init__(self):
        self.is_recording = False
        self.data = []

    def start(self,fs=int(sd.query_devices(sd.default.device[0])['default_samplerate']),CHANNELS=1):
        self.is_recording = True
        self.audio_data = []
        with sd.InputStream(samplerate=fs, channels=CHANNELS, callback=self.callback):
            while self.is_recording:
                sd.sleep(100)
        if self.audio_data:
            audio = np.concatenate(self.audio_data, axis=0)
            write("temp_audio_in.wav", fs, audio)

    def callback(self,indata, frames, time, status):
        if self.is_recording:
            self.audio_data.append(indata.copy())
        else:
            raise sd.CallbackStop  # 録音終了
        
    def stop(self):
        self.is_recording = False

class AudioTextProcessor:
    def speach_to_text(self,wav_file):
        result = model.transcribe(wav_file,task="transcribe",language="en")
        return result["text"]

    def text_to_speech(self,text: str):
        speaching_text = text
        tts = gTTS(speaching_text, lang='en')
        filename = "temp_audio_out.mp3"
        tts.save(filename)
        os.system(f"{filename}")

def main():
    pass
if __name__ == "__main__":
    main()
