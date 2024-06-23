import mido
from mido import MidiFile
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
from io import BytesIO
import zipfile
import os

app = FastAPI()

midiDic = []
notesOn = []
lastTime = 0
highestFileNumber = 0
totalTime = 0
tempo = None

for midinum in range(128):
    midiDic.append(0)
    freq = 440 * float(2 ** float(float(midinum - 69) / 12))
    midiDic[midinum] = freq

def midiNUM(num):
    return midiDic[num]

@app.post("/api/convert")
async def convert(file: UploadFile = File(...)):
    global notesOn, lastTime, highestFileNumber, totalTime, tempo
    notesOn = []
    lastTime = 0
    highestFileNumber = 0
    totalTime = 0
    tempo = None

    contents = await file.read()
    midiFile = MidiFile(file=BytesIO(contents))  # Corrected this line
    mergedMidiFile = MidiFile()
    mergedMidiFile.tracks.append(mido.merge_tracks(midiFile.tracks))

    output_files = {}
    for msg in mergedMidiFile:
        msgDict = msg.dict()

        messageAdded = False
        noteIndex = -1
        totalTime += msg.time

        if msg.is_meta:
            metaDic = msg.dict()
            if 'tempo' in metaDic:
                tempo = metaDic['tempo']

        if msg.time != 0:
            for i in range((len(notesOn) - 1) // 2 + 1):
                if i not in output_files:
                    output_files[i] = BytesIO()

                output_files[i].write(f'  delay({(msg.time / 1.5) * 1000});\n'.encode('utf-8'))

        if 'note' in msgDict:
            if msg.type == 'note_on' and msg.velocity != 0:
                for index, io in enumerate(notesOn):
                    if isinstance(io, int):
                        notesOn[index] = msg
                        noteIndex = index
                        messageAdded = True
                        break

                if not messageAdded:
                    notesOn.append(msg)
                    noteIndex = len(notesOn) - 1

                fileNumber = noteIndex // 2
                toneNumber = noteIndex % 2

                if fileNumber not in output_files:
                    output_files[fileNumber] = BytesIO()

                if fileNumber > highestFileNumber and totalTime != 0:
                    highestFileNumber = fileNumber
                    output_files[fileNumber].write(f'  delay({(totalTime / 1.5) * 1000});\n'.encode('utf-8'))

                output_files[fileNumber].write(f'  tone{toneNumber}.play({midiNUM(msg.note)});\n'.encode('utf-8'))

            elif msg.type == 'note_off' or msg.velocity == 0:
                for index, item in enumerate(notesOn):
                    if not isinstance(item, int):
                        if msg.note == item.note and msg.channel == item.channel:
                            notesOn[index] = 0
                            noteIndex = index
                            break

                fileNumber = noteIndex // 2
                toneNumber = noteIndex % 2

                if fileNumber not in output_files:
                    output_files[fileNumber] = BytesIO()

                output_files[fileNumber].write(f'  tone{toneNumber}.stop();\n'.encode('utf-8'))

    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for i, content in output_files.items():
            content.seek(0)
            zip_file.writestr(f'Arduino{i}.txt', content.read())

    zip_buffer.seek(0)
    return StreamingResponse(zip_buffer, media_type='application/zip', headers={"Content-Disposition": "attachment; filename=output.zip"})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
