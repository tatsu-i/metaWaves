from AccelBrainBeat.brainbeat.monaural_beat import MonauralBeat
from pydub import AudioSegment
import numpy as np
import wave_func as wf
import os

total_time_min = 30
total_time = 60*total_time_min

file_name = "/tmp/beta.wav"
brain_beat = MonauralBeat()

brain_beat.save_beat(
    output_file_name="/tmp/1.wav",
    frequencys=(446, 482),
    play_time=total_time,
    volume=0.3
)
brain_beat.save_beat(
    output_file_name="/tmp/2.wav",
    frequencys=(567, 607),
    play_time=total_time,
    volume=0.3
)
sound1 = AudioSegment.from_file("/tmp/1.wav")
sound2 = AudioSegment.from_file("/tmp/2.wav")
output = sound1.overlay(sound2, position=0)
output.export("wav/覚醒用_ベータ波_モノラル_音量注意.wav", format="wav")
