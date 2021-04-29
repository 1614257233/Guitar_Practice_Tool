
"""
Connect guitar audio to computer, and play the note the computer asks
"""

import queue
import random
import time
import pyaudio
import threading
import sys
import numpy as np
from scipy import signal


print('Please Seclect Practice Mode:\n1:High E Excercise\n2:B String Excercise\n3:G String Excercise\n4:D String Excercise\n5:A String Excercise\n6:E String Excercise\n7:Complete Excercise\n')
print('Press Enter to see the answer; Input letter q and press Enter to exit the program.')
mode = ['High E Excercise', 'B String Excercise', 'G String Excercise',
        'D String Excercise', 'A String Excercise', 'E String Excercise', 'Complete Excercise']


# Frequencies got from https://www.researchgate.net/figure/Guitar-Fretboard-frequencies_tbl1_311707611

fingerboard_freq = np.array([[329.63, 349.23, 369.99, 392.00, 415.30, 440.00, 466.16, 493.88, 523.25, 554.37, 587.33, 622.25, 659.26],  # high e
                             [246.94, 261.63, 277.18, 293.66, 311.13, 329.63, 349.23, 369.99, 392.00, 415.30, 440.00, 466.16, 493.88],  # B
                             [196.00, 207.65, 220.00, 233.08, 246.94, 261.63, 277.18, 293.66, 311.13, 329.63, 349.23, 369.99, 392.00],  # G
                             [146.83, 155.56, 164.81, 174.61, 185.00, 196.00, 207.65, 220.00, 233.08, 246.94, 261.63, 277.18, 293.66],  # D
                             [110.00, 116.54, 123.47, 130.81, 138.59, 146.83, 155.56, 164.81, 174.61, 185.00, 196.00, 207.65, 220.00],  # A
                             [82.41, 87.31, 92.50, 98.00, 103.83, 110.00, 116.54, 123.47, 130.81, 138.59, 146.83, 155.56, 164.81]])     # E


freq_table = np.array([82.41, 87.31, 92.50, 98.00, 103.83, 110.00, 116.54, 123.47, 130.81, 138.59, 146.83, 155.56,
                       164.81, 174.61, 185.00, 196.00, 207.65, 220.00, 233.08, 246.94, 261.63, 277.18, 293.66, 311.13,
                       329.63, 349.23, 369.99, 392.00, 415.30, 440.00, 466.16, 493.88, 523.25, 554.37, 587.33, 622.25,
                       659.26, 698.46, 739.99, 783.99, 830.61, 880.00, 932.33, 987.77, 1046.50, 1108.73, 1174.66, 1244.51])

fingerboard_dict = ['E', 'F', 'F#/Gb', 'G', 'G#/Ab', 'A', 'A#/Bb', 'B', 'C', 'C#/Db', 'D', 'D#/Eb',
                    'E', 'F', 'F#/Gb', 'G', 'G#/Ab', 'A', 'A#/Bb', 'B', 'C', 'C#/Db', 'D', 'D#/Eb',
                    'E', 'F', 'F#/Gb', 'G', 'G#/Ab', 'A', 'A#/Bb', 'B', 'C', 'C#/Db', 'D', 'D#/Eb',
                    'E', 'F', 'F#/Gb', 'G', 'G#/Ab', 'A', 'A#/Bb', 'B', 'C', 'C#/Db', 'D', 'D#/Eb']


scale = 0
string = 0
string_user = 0
scale_user = 0
count = 0
max_freq = 0

fingerboard = [[5, 7, 8, 10, 0, 1, 3],
               [10, 0, 1, 3, 5, 6, 8],
               [2, 4, 5, 7, 9, 10, 0],
               [7, 9, 10, 0, 2, 3, 5],
               [0, 2, 3, 5, 7, 8, 10],
               [5, 7, 8, 10, 0, 1, 3]]

scales = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

CHUNK = 20000
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
data = []
DF = RATE / CHUNK
frames = []
counter = 1

rt_data = np.arange(0, CHUNK, 1)
fft_data = np.arange(0, CHUNK / 2 + 1, 1)

# pyaudio setup
p = pyaudio.PyAudio()
q = queue.Queue()


def audio_callback(in_data, frame_count, time_info, status):
    global ad_rdy_ev

    q.put(in_data)
    ad_rdy_ev.set()
    if counter <= 0:
        return (None, pyaudio.paComplete)
    else:
        return (None, pyaudio.paContinue)


stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                output=False,
                frames_per_buffer=CHUNK,
                stream_callback=audio_callback)

stream.start_stream()

# processing block
window = signal.hamming(CHUNK)


def read_audio_thead(q, stream, frames, ad_rdy_ev):
    global rt_data
    global fft_data
    global max_freq

    while stream.is_active():

        ad_rdy_ev.wait(timeout=1000)
        if not q.empty():
            # processing all the audio data here
            data = q.get()

            while not q.empty():
                q.get()

            rt_data = np.frombuffer(data, np.dtype('<i2'))
            rt_data = rt_data * window
            fft_temp_data = (np.fft.fft(rt_data) * 2 / CHUNK).reshape(CHUNK, 1)
            fft_data = np.abs(fft_temp_data[0:int(CHUNK / 2) + 1])
        ad_rdy_ev.clear()


ad_rdy_ev = threading.Event()

t = threading.Thread(target=read_audio_thead, args=(q, stream, frames, ad_rdy_ev))

t.daemon = True
t.start()

try:
    train_mode = int(input('Select Practice Mode')) - 1
    print('You selected %s and is going to start right now' % mode[train_mode])
except:
    sys.exit()
    print('Audio Input Error! Please restart the program!')

while(True):

    if(train_mode < 6):
        string = train_mode
    else:
        while string_user == string:
            string = random.randrange(0, 6)

    while scale_user == scale:

        scale = random.randrange(0, 7)

    pos = fingerboard[string][scale]
    check = False
    print('On %d String pPlay %s Note' % (string + 1, scales[scale]))
    while(check == False):

        if np.max(fft_data) > 100:
            max_freq = np.argmax(fft_data) * DF  # max value index
            minn = np.argmin(np.abs(freq_table - max_freq))

            if fingerboard_dict[minn] == scales[scale]:
                count = count + 1
                if count >= 2:
                    break
            else:
                count = 0
                print('\rYou Played It Wrong£¬You Played %s£¬You Are Asked To Play %s' % (fingerboard_dict[minn], scales[scale]), end=' ')

    print('\nCorrect ~', end=' ')
    print('Remember %s is at %d String,  %d Fret~\n' % (scales[scale], string + 1, fingerboard[string][scale]))
    time.sleep(1)
    print('Next Question£º', end=' ')
    string_user = string
    scale_user = scale

stream.stop_stream()
stream.close()
p.terminate()
print('Have a good day£¡\n')
