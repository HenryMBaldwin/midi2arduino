import argparse
import mido
from mido import MidiFile

midiDic = []
notesOn = []
lastTime = 0
highestFileNumber = 0
totalTime = 0
tempo = None

for midinum in range(128):
    midiDic.append(0)
    freq = 440 * float(2 ** float(float(midinum-69) / 12))
    midiDic[midinum] = freq

def midiNUM(num):
    return midiDic[num]

midiFile = MidiFile("/Users/henry/Dev/PycharmProjects/miditoarduino/midis/Dragonborn - Skyrim [MIDICollection.net].mid")
mergedMidiFile = MidiFile()
mergedMidiFile.tracks.append(mido.merge_tracks(midiFile.tracks))


for msg in mergedMidiFile:
    print msg

    msgDict = msg.dict()

    messageAdded = False
    noteIndex = -1
    totalTime += msg.time


    if msg.is_meta:
        metaDic = msg.dict()
        if 'tempo' in metaDic:
            tempo = metaDic['tempo']

    if msg.time != 0:
        for i in range(((len(notesOn) - 1) / 2) + 1):
            arduinoFile = open('/Users/henry/Dev/PycharmProjects/miditoarduino/Output/Arduino{}.txt'.format(i), 'a+')

            arduinoFile.write('  delay({});\n'.format((msg.time / 1.5) * 1000))
            arduinoFile.close()

    if 'note' in msgDict:
        if msg.type == 'note_on' and msg.velocity != 0:
            for index, io in enumerate(notesOn):
                if type(io) == int:
                    notesOn[index] = msg
                    noteIndex = index
                    messageAdded = True
                    break

            if not messageAdded:
                notesOn.append(msg)
                noteIndex = len(notesOn) - 1

            fileNumber = noteIndex / 2
            toneNumber = noteIndex % 2

            arduinoFile = open('/Users/henry/Dev/PycharmProjects/miditoarduino/Output/Arduino{}.txt'.format(fileNumber), 'a+')

            if fileNumber > highestFileNumber and totalTime != 0:
                highestFileNumber = fileNumber
                arduinoFile.write('  delay({});\n'.format((totalTime / 1.5) * 1000))

            arduinoFile.write('  tone{}.play({});\n'.format(toneNumber, midiNUM(msg.note)))
            arduinoFile.close()

        elif msg.type == 'note_off' or msg.velocity == 0:
            for index, item in enumerate(notesOn):
                if not type(item) == int:
                    if msg.note == item.note and msg.channel == item.channel:
                        notesOn[index] = 0
                        noteIndex = index
                        break

            fileNumber = noteIndex / 2
            toneNumber = noteIndex % 2

            arduinoFile = open('/Users/henry/Dev/PycharmProjects/miditoarduino/Output/Arduino{}.txt'.format(fileNumber),'a+')

            arduinoFile.write('  tone{}.stop();\n'.format(toneNumber))
            arduinoFile.close()


