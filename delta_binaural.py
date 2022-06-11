from AccelBrainBeat.brainbeat.binaural_beat import BinauralBeat
from pydub import AudioSegment
import numpy as np
import wave_func as wf
import os


total_time_min = 60
total_time = 60*total_time_min
samprate = 44100

length = 2 ** 17
tmp = np.random.random(size=length) * 2 - 1
S = np.fft.rfft(tmp)
fil = 1 / (np.arange(len(S))+1) 
S = S * fil
s = np.fft.irfft(S)
s /= np.max(np.abs(s))
c = np.concatenate([s for n in range(60)])

wf.write_wave("/tmp/pinknoise.wav", c, fs=samprate)

noise = AudioSegment.empty()
for n in range(total_time_min):
    noise += AudioSegment.from_wav("/tmp/pinknoise.wav")

noise = noise.set_channels(2)
noise = noise - 15
noise = noise[:60*1000*total_time_min]
noise.export("pinknoise.wav", format="wav")



file_name = "/tmp/delta.wav"
brain_beat = BinauralBeat()
brain_beat.save_beat(
    output_file_name="/tmp/1.wav",
    frequencys=(100, 104),
    play_time=total_time,
    volume=0.3
)
brain_beat.save_beat(
    output_file_name="/tmp/2.wav",
    frequencys=(50, 52),
    play_time=total_time,
    volume=0.3
)
sound1 = AudioSegment.from_file("/tmp/1.wav")
sound2 = AudioSegment.from_file("/tmp/2.wav")
output = sound1.overlay(sound2, position=0)
output.export(file_name, format="wav")


sound1 = AudioSegment.from_file("/tmp/1.wav")
sound2 = AudioSegment.from_file("/tmp/2.wav")
output = sound1.overlay(sound2, position=0)
output.export(file_name, format="wav")

combined_wav = AudioSegment.empty()
combined_wav += AudioSegment.from_wav(file_name)
output = noise.overlay(combined_wav, position=0)

output.export("delta_noise.wav", format="wav")
