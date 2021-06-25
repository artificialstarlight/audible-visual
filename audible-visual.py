from PIL import Image
from midiutil.MidiFile import MIDIFile
import sys

path = sys.argv[1]
#path = "test.jpg"
outfile = sys.argv[2]

img = Image.open(path)
pixels = list(img.getdata())
width, height = img.size
pixels = [pixels[i * width:(i + 1) * width] for i in range(height)]

A0_NOTE = 21
C8_NOTE = 108

def linear_interpolate(min, max, note):
  return int(min + note * (max - min))

notes = []
for p in pixels:
    for pixel in p:
        avg = (pixel[0] + pixel[1] + pixel[2])//3
        avg = avg/2
        normalized = avg/255
        note = linear_interpolate(A0_NOTE,C8_NOTE,normalized)
        notes.append(note)
   
mf = MIDIFile(1)   
track = 0  

time = 0
mf.addTrackName(track, time, "Test")
mf.addTempo(track, time, 120)

channel = 0
volume = 100
for time,note in enumerate(notes):
    pitch = note
    duration = 1
    mf.addNote(track, channel, pitch, time, duration, volume)

# write it to disk
with open(outfile, 'wb') as outf:
    mf.writeFile(outf)
