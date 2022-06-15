from AccelBrainBeat.brainbeat.monaural_beat import MonauralBeat
from pydub import AudioSegment
import numpy as np
import wave_func as wf
import os


total_time_min = 60
total_time = 60*total_time_min

file_name = "/tmp/delta.wav"
brain_beat = MonauralBeat()
brain_beat.save_beat(
    output_file_name="/tmp/1.wav",
    frequencys=(99, 101),
    play_time=total_time,
    volume=0.3
)
brain_beat.save_beat(
    output_file_name="/tmp/2.wav",
    frequencys=(49.5, 50.5),
    play_time=total_time,
    volume=0.3
)
sound1 = AudioSegment.from_file("/tmp/1.wav")
sound2 = AudioSegment.from_file("/tmp/2.wav")
output = sound1.overlay(sound2, position=0)
output.export("wav/睡眠導入_デルタ波_モノラル.wav", format="wav")
