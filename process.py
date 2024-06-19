import numpy as np
import matplotlib.pyplot as plt
import scipy
from midiutil.MidiFile import MIDIFile

import random

def main():
    file = input("Enter wav filename:")
    sample_rate, audio_data = scipy.io.wavfile.read(file)

    print("Number of channels:", len(audio_data.shape))
    print("Sample rate:", sample_rate)
    print("Data length:", audio_data.shape[0])
    print("Time:", audio_data.shape[0] / sample_rate)
    print("Max:", np.max(audio_data))

    audio_data = audio_data / np.max(audio_data)
    print("normalized:", np.max(audio_data))

    sample_width = int(input("Enter sampling width: "))
 
    tempo = 0
    while not (tempo > 1):
        tempo = int(input("Enter tempo: "))
    volume = int(input("Enter velocity (-1 for wav sample control, -2 for random)"))
    pitch = int(input("Enter pitch (-1 for wav sample control, -2 for random)"))
    time = int(input("Enter beat/time (-1 for sample control, -2 for random increase)"))
    duration = int(input("Enter the duration (-1 for wav sample control, -2 for random)"))

    i = 0

    mf = MIDIFile(1)
    track = 0

    mf.addTrackName(track, 0, "WAV to MIDI")
    mf.addTempo(track, 0, tempo)

    channel = 0
    note_count = 0
    sample_time = 0

    while i < audio_data.shape[0]:
        if(len(audio_data.shape)) > 1:
            sample = audio_data[i, 0]
        else:
            sample = audio_data[i]

        if volume == -1:
            sample_volume = int(np.abs(sample)*127)
        elif volume == -2:
            sample_volume = random.randrange(1, 127)
        else:
            sample_volume = volume
        
        if pitch == -1:
            sample_pitch = int(np.abs(sample)*107) + 20
        elif pitch == -2:
            sample_pitch = random.randrange(24, 127)
        else:
            sample_pitch = pitch

        if time == -1:
            sample_time = sample_time + int(np.abs(sample)*10)
        elif time == -2:
            sample_time = sample_time + random.randrange(0, 10)
        else:
            sample_time = sample_time + time

        if duration == -1:
            sample_duration = int(np.abs(sample)*10)
        elif duration == -2:
            sample_duration = random.randrange(1, 10)
        else:
            sample_duration = duration

        #print("track", track, "cahnnel", channel, "pitch", sample_pitch, "Volume", sample_volume, "time", sample_time, "duration", sample_duration, "volume", sample_volume)
        mf.addNote(track, channel, sample_pitch, sample_time, sample_duration, sample_volume)

        note_count = note_count + 1
        i = i + sample_width

    print("Wrote", note_count, "notes")

    with open("output.mid", 'wb') as outf:
        mf.writeFile(outf)

    plt.plot(np.arange(len(audio_data)) / sample_rate, audio_data/np.max(audio_data))
    plt.show()

    return

main()
