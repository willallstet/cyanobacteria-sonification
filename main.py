from makeSong import Song
from midiutil import MIDIFile
fileName="/Users/williamallstetter/Desktop/data_sonification/videos/2020.12.8_fremyella_filament_to_hormogonia_0003/2020.12.8_fremyella_filament_to_hormogonia_0003"
exportSong = Song(fileName+".csv", 10, 60)
midiExport = exportSong.makeSong()
with open(fileName+"_sound.mid", 'wb') as output_file:#save the midi file
    midiExport.writeFile(output_file)
