import numpy as np
import matplotlib.pyplot as plt
import scipy
from midiutil.MidiFile import MIDIFile

import random

def main():

    choice = 0
    
    tracks = []
    rngs = [(1, 127)]
    # Sample_width, tempo, volume, pitch, time, duration, track_name, notes_to_write, midi_bounds
    settings = [100, 120, 127, 60, 1, 1, "wav to midi", 100, (60, 100)]

    while True:
        choice = menu(tracks)
    
        if(choice == 1):
            tracks = readWAV(tracks)
        elif(choice == 2):
            settings, rngs = setup(settings, tracks, rngs)
        elif(choice == 3):
            rng_setup()
        elif(choice == 4):
            process(tracks, rngs, settings)
        elif(choice == 5):
            for item in settings:
                print(item)

            print()

            for item in rngs:
                print(item)
        elif(choice == 6):
            plot(tracks)
        elif(choice == 7):
            exit(0)


def menu(tracks):
    choice = 0
    while(choice not in [1, 2, 3, 4, 5, 6, 7]):
        print()
        print("What would  you like to do?")
        print("1) Load WAV file")
        print("2) Configure process")
        print("3) Configure RNG")
        print("4) Start process")
        print("5) Display configuration")
        print("6) Plot track")
        print("7) Quit")
        choice = input(" > ")
        if(choice.isdigit()):
            choice = int(choice)
    print()
    return choice

def readWAV(tracks):
    file = input("Enter wav filename: ")
    print()
    sample_rate, audio_data = scipy.io.wavfile.read(file)

    print("Number of channels:", len(audio_data.shape))
    print("Sample rate:", sample_rate)
    print("Data length:", audio_data.shape[0])
    print("Time:", audio_data.shape[0] / sample_rate)
    print("Max:", np.max(audio_data))

    audio_data = audio_data / np.max(audio_data)
    print("normalized:", np.max(audio_data))
    a = ""
    b = ""

    while(not(a.isdigit() and b.isdigit()) or int(a) > int(b) or int(a) < 0):

        print("Please enter midi bounds, so lowest and highest note/pitch/velocity:")
        a = input("Lower bound: ")
        b = input("Upper bound: ")

    if(len(audio_data.shape) == 1):
        tracks.append((sample_rate, audio_data, file, (int(a),int(b))))
    elif(len(audio_data.shape) == 2):
        tracks.append((sample_rate, audio_data[:,0], file+" L", (int(a),int(b))))
        tracks.append((sample_rate, audio_data[:,1], file+" R", (int(a),int(b))))
    else:
        print("WAV with more than 2 channels not supported!")

    return tracks

def setup(settings, tracks, rngs):
    choice = 0
    new_value = 0
    names = ["sample width", "tempo", "velocity", "pitch", "time", "duration"]
    while(choice not in [1, 2, 3, 4, 5, 6, 7, 8]):
        print()
        if choice != 0:
            print("Bad entry, try again!")
            print()
        print("Please choose an value to change:")
        print(f"1) Sample width [{settings[0]}]")
        print(f"2) tempo [{settings[1]}]")
        print(f"3) velocity [{settings[2]}]")
        print(f"4) pitch [{settings[3]}]")
        print(f"5) time [{settings[4]}]")
        print(f"6) duration [{settings[5]}]")
        print(f"7) track name [{settings[6]}]")
        print(f"8) Note to write [{settings[7]}]")
        #print(f"9) Midi bounds [{settings[8]}, {settings[9]}]")
        choice = input(" > ")
        if(choice.isdigit()):
            choice = int(choice)

    while (new_value not in [1, 2, 3] and choice not in [7, 8, 9]):
        print("1) constant driver")
        print("2) WAV driver")
        print("3) random number driver")
        new_value = input(f"What would you like to chage the {names[choice - 1]} driver to?")
        if(new_value.isdigit()):
            new_value = int(new_value)

    if(new_value == 1):
        update = input("Please enter the new value:")
        if(update.isdigit() and int(update) > 0):
            settings[choice - 1] = int(update)
    elif(new_value == 2):
        print("Please select the WAV driver")
        i = 1
        for driver in tracks:
            print(f"{i}) WAV driver {i} [name: {driver[2]}, sample rate: {driver[0]}, channels: {len(driver[1].shape)}, bounds: {driver[3]}]")
            i = i + 1
        
        if(i == 1):
            print("No loaded WAV files! Please load a file.")
        else:
            my_driver = input(" > ")
            if(my_driver.isdigit() and int(my_driver) > 0 and int(my_driver) < i):
                settings[choice - 1] = "WAV" + str(my_driver)
    elif(new_value == 3):
        i = 1
        print("Select random generator")
        for rng in rngs:
            print(f"{i}) RNG driver {i} [min: {rngs[i-1][0]}, max: {rngs[i-1][1]}]")
            i = i + 1
        print(f"c) Create new RNG driver")
        my_rng = input(" > ")
        if(my_rng.isdigit() and int(my_rng) > 0 and int(my_rng) < i):
            settings[choice - 1] = "RNG" + str(my_rng)
        elif(my_rng == "c"):
            settings[choice-1] = "RNG" + str(i)
            rngs.append(make_rng())

    if(choice == 7):
        settings[choice-1] = input("Enter new track name: ")
    elif(choice == 8):
        value = input("Enter number of notes to write: ")
        if(value.isdigit() and int(value) > 0):
            settings[choice-1] = int(value)
        else:
            print("Bad value, skipping.")
    elif(choice == 9):
        a = ""
        b = ""
        while(not (a.isdigit() and b.isdigit()) or int(a) < 0 or int(b) < 0 or int(a) > int(b)):
            a = input("Lower bound: ")
            b = input("Upper bound: ")
        settings[choice - 1] = (int(a), int(b))
    return (settings, rngs)

def process(tracks, rngs, settings):
    print("Using the following recipie:")
    print(f"Sample width: {settings[0]}")
    print(f"Tempo: {settings[1]}")
    print(f"Velocity: {settings[2]}")
    print(f"Pitch: {settings[3]}")
    print(f"Time: {settings[4]}")
    print(f"duration: {settings[5]}")

    i = 0

    mf = MIDIFile(1)
    track = 0

    mf.addTrackName(track, 0, settings[6])
    mf.addTempo(track, 0, settings[1])

    channel = 0
    note_count = 0
    sample_time = 0
    samples = [0, 0, 0, 0]

    while note_count < settings[7]:
        for num in range(0, 4):
            if "WAV" in str(settings[num+2]):
                samples[num] = waver(settings, tracks, settings[num+2], i)
            elif "RNG" in str(settings[num+2]):
                samples[num] = rnger(rngs,settings[num+2])
            else:
                samples[num] = settings[num+2]
        
        for samp in samples:
            if(samp <= 0 or samp > 127):
                print("Invalid sample! Clipping samples.")
                print(samp)
                input()
                samples = np.clip(samples, 1, 127)
        #print("volume, pitch, time, duration")
        #print(samples)
        
        mf.addNote(track, channel, samples[1], sample_time, samples[3], samples[0])
        sample_time = sample_time + samples[2]

        note_count = note_count + 1
        i = i + settings[0]

    print(f"Done! Wrote {note_count} notes")

    with open("output.mid", 'wb') as outf:
        mf.writeFile(outf)

    return

def make_rng():
    a = "a"
    b = "b"
    while(not a.isdigit() and not b.isdigit()):
        if(a != "a" or b != "b"):
            print("Bad value, try again.")
            print()
        a = input("Enter lower bound: ")
        b = input("Enter upper bound: ")
    return (int(a), int(b))

def rnger(rngs, selected):
    return random.randint(rngs[int(selected[-1])-1][0], rngs[int(selected[-1])-1][1])

def waver(settings, tracks, selected, i):
    choose = tracks[int(selected[-1])-1][1]
    bound = tracks[int(selected[-1])-1][3]
    return int(np.abs(choose[i % len(choose)-1] * (bound[1]-bound[0])) + 1 + bound[0])

def plot(tracks):
    print("Select a track to plot:")
    i = 1
    plot = -1
    for driver in tracks:
        print(f"{i}) WAV driver {i} [name: {driver[2]}, sample rate: {driver[0]}, channels: {len(driver[1].shape)}]")
        i = i + 1
        
    if(i == 1):
        print("No loaded WAV files! Please load a file.")
    else:
        my_driver = input(" > ")
        if(my_driver.isdigit() and int(my_driver) > 0 and int(my_driver) < i):
            plot = tracks[int(my_driver)-1]

    if(plot != -1):
        plt.plot(np.arange(len(plot[1])) / plot[0], plot[1])
        plt.show()


main()
