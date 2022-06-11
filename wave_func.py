#-- coding: utf-8 --
import numpy as np
import wave
from numba import jit

@jit
def binary2float(frames, length, sampwidth):
    if sampwidth==1:
        data = np.frombuffer(frames, dtype=np.uint8)
        data = data - 128
    elif sampwidth==2:
        data = np.frombuffer(frames, dtype=np.int16)
    elif sampwidth==3:
        a8 = np.frombuffer(frames, dtype=np.uint8)
        tmp = np.empty([length, 4], dtype=np.uint8)
        tmp[:, :sampwidth] = a8.reshape(-1, sampwidth)
        tmp[:, sampwidth:] = (tmp[:, sampwidth-1:sampwidth] >> 7) * 255
        data = tmp.view("int32")[:, 0]
    elif sampwidth==4:
        data = np.frombuffer(frames, dtype=np.int32)
    data = data.astype(float)/(2**(8*sampwidth-1)) # Normalize (int to float)
    return data

@jit
def float2binary(data, sampwidth):
    data = (data*(2**(8*sampwidth-1)-1)).reshape(data.size, 1) # Normalize (float to int)
    if sampwidth==1:
        data = data+128
        frames = data.astype(np.uint8).tobytes()
    elif sampwidth==2:
        frames = data.astype(np.int16).tobytes()
    elif sampwidth==3:
        a32 = np.asarray(data, dtype = np.int32)
        a8 = (a32.reshape(a32.shape + (1,)) >> np.array([0, 8, 16])) & 255
        frames = a8.astype(np.uint8).tobytes()
    elif sampwidth==4:
        frames = data.astype(np.int32).tobytes()
    return frames
 
def read_wave(file_name, start=0, end=0):
    file = wave.open(file_name, "rb") # open file
    sampwidth = file.getsampwidth()
    nframes = file.getnframes()
    file.setpos(start)
    if end == 0:
        length = nframes-start
    else:
        length = end-start+1
    frames = file.readframes(length)
    file.close() # close file
    return binary2float(frames, length, sampwidth) # binary to float
 
def write_wave(file_name, data, sampwidth=3, fs=48000):
    file = wave.open(file_name, "wb") # open file
    # setting parameters
    file.setnchannels(1)
    file.setsampwidth(sampwidth)
    file.setframerate(fs)
    frames = float2binary(data, sampwidth) # float to binary
    file.writeframes(frames)
    file.close() # close file
 
def getParams(file_name):
    file = wave.open(file_name) # open file
    params = file.getparams()
    file.close() # close file
    return params
