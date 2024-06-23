# MIDI2Arduino

MIDI2Arduino is a tool to convert MIDI files to be played on one of the most accessible Arduino platforms, the Arduino UNO.

Check it out [here](https://midi2arduino.vercel.app/)

![image](https://github.com/HenryMBaldwin/midi2arduino/assets/67980579/e02c27f4-b3ab-438d-bd05-101c876f4ac3)

## About

This transpiler converts midi to arduino code using the the Arduino Tone library. Due to the number of hardware timers on the Arduino UNO, only two tones can be generated on one Arduino UNO at a time. This means multiple files and Arduinos may be necessary to play a full MIDI file depending on the song. This transpiler will output the minimum number of code files in a .zip necessary to represent the given .mid. The transpiling is done via a Python script deployed as an API alongside the SvelteKit front-end on Vercel.

## Usage

Just drop a MIDI file into the file drop zone and click convert and download. This will download a zip containing the txt file(s) with the Arduino code in them. Each file needs to be played back on a separate Ardiino UNO. To sync the start of multiple Arduinos playback, it is recommended that a single button is wired to all Arduinos and programmed to start playback. Because of this, the outputted files will be txt files so the code can be easily copied rather than Arduino code files. 

This project was made with the classic [Arduino and pizoelectric speaker project in mind](https://docs.arduino.cc/built-in-examples/digital/toneMelody/).
