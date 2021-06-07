import numpy as np
import csv
import pandas as pd
from midiutil import MIDIFile
import os
import math

class Song:
  def __init__(self, csvName, dur, center):
    #self.videoName = videoName
    self.csvName = csvName
    self.dur = dur*960
    self.MyMIDI = MIDIFile(3, eventtime_is_ticks=True) # midi file we output to
    self.MyMIDI.addTempo(0, 0, 120) #made at 60BPM so the slide is played at 2 fps
    self.MyMIDI.addTempo(1, 0, 120) #made at 60BPM so each second is played at 2 fps
    self.MyMIDI.addTempo(2, 0, 120) #made at 60BPM so each second is played at 2 fps
    self.c2c = pd.read_csv(self.csvName, usecols = ['Cell To Cell']).to_numpy().astype(int)
    self.c2b = pd.read_csv(self.csvName, usecols = ['Background To Cell']).to_numpy().astype(int)
    self.num_cells = pd.read_csv(self.csvName, usecols = ['Number of Objects']).to_numpy().astype(int)
    self.num_cells_added = pd.read_csv(self.csvName, usecols = ['Change in Number of Objects']).to_numpy().astype(int)
    self.avg_area = pd.read_csv(self.csvName, usecols = ['Average Area']).to_numpy().astype(int)
    self.delta_mass = pd.read_csv(self.csvName, usecols = ['Change in Cell Mass']).to_numpy().astype(int)
    self.keyOfC = [83,81,79,77,76,74,72,71,69,67,65,64,62,60,59,57,55,53,52,50,48,47,45,43,41,40,38,36,35,33,31,29,28,26,24]
    self.pitches = {}

    if not os.path.isfile('learning_data.txt'):
        with open('learning_data.txt','w+') as file:
            self.c2c_max = self.c2c.max()
            self.c2c_min = self.c2c.min()
            self.c2b_max = self.c2b.max()
            self.c2b_min = self.c2b.min()
            self.avg_area_max = self.avg_area.max()
            self.avg_area_min = self.avg_area.min()
            self.num_cells_added_max = self.num_cells_added.max()
            self.num_cells_added_min = self.num_cells_added.min()
            self.delta_min = self.delta_mass.min()
            self.delta_max = self.delta_mass.max()
            file.write(str(self.c2c_max) + "," + str(self.c2b_max) \
            + "," + str(self.c2c_min) + "," + str(self.c2b_min) \
            + "," + str(self.avg_area_max) + "," + str(self.avg_area_min) \
            + "," + str(self.num_cells_added_max) + "," + str(self.num_cells_added_min) \
            + "," + str(self.delta_max) + "," + str(self.delta_min))
    else:
        with open('learning_data.txt','r+') as file:
            self.old_data = file.readline().split(',')
        with open('learning_data.txt','w+') as file:
            self.c2c_max = max(float(self.old_data[0]),self.c2c.max())
            self.c2c_min = min(float(self.old_data[2]),self.c2c.min())
            self.c2b_max = max(float(self.old_data[1]),self.c2b.max())
            self.c2b_min = min(float(self.old_data[3]),self.c2b.min())
            self.avg_area_max = max(float(self.old_data[4]),self.avg_area.max())
            self.avg_area_min = min(float(self.old_data[5]),self.avg_area.min())
            self.num_cells_added_max = max(float(self.old_data[6]),self.num_cells_added.min())
            self.num_cells_added_min = min(float(self.old_data[7]),self.num_cells_added.min())
            self.delta_max = max(float(self.old_data[8]),self.delta_mass.max())
            self.delta_min = min(float(self.old_data[9]),self.delta_mass.min())
            file.write(str(self.c2c_max) + "," + str(self.c2b_max) \
            + "," + str(self.c2c_min) + "," + str(self.c2b_min) \
            + "," + str(self.avg_area_max) + "," + str(self.avg_area_min) \
            + "," + str(self.num_cells_added_max) + "," + str(self.num_cells_added_min) \
            + "," + str(self.delta_max) + "," + str(self.delta_min))

  def makeDrums(self):
      time = 0
      max = self.num_cells_added.max()
      min = self.num_cells_added.min()
      for i in self.num_cells_added:
          if i[0]<0:
              self.MyMIDI.addNote(1, 0, 28, time, 1, int((127/min)*i[0]), annotation=None)
          if i[0]>0:
              self.MyMIDI.addNote(1, 0, 29, time, 1, int((127/max)*i[0]), annotation=None)
          time = time+960

  def makeMelody(self):
      #each note length corresponds to the size of the object
      time = 0
      max = self.avg_area_max
      min = self.avg_area_min
      for i in self.avg_area:
          pitch = int(self.find_nearest(self.keyOfC, 83 * self.movement(self.c2c[int(time/960)],self.c2b[int(time/960)])))
          len = int(self.dur*(float(self.avg_area[int(time/960)])/float(max))+1)
          vol = int(127 * (float(self.movement(self.c2c[int(time/960)],self.c2b[int(time/960)]) * 0.75) + (0.25*(float(self.avg_area[int(time/960)])/float(max)))))
          if ((pitch in self.pitches) and self.pitches[pitch]<=time) or not pitch in self.pitches:
              self.MyMIDI.addNote(0, 0, pitch, time, len, vol, annotation=None)
              self.pitches[pitch] = time+len
          time = time+960

  def arpeggio(self):
        time = 0
        offset = 0
        max_added = int(self.num_cells_added_max)
        min_added = int(self.num_cells_added_min)
        abs_max = int(max(abs(max_added),abs(min_added)))
        notes = [60,62,64]
        rates = [32,24,16,12,8,6,4,3,2,1]
        currentNote = 0
        for i in self.num_cells_added:
            index = int(round(float(9*(abs(i)/float(abs_max)))))
            rate = rates[index]
            for j in range(rate):
                if self.num_cells_added[i] < 0:
                    pitch = notes[currentNote]
                    currentNote = currentNote - 1
                    if currentNote < 0:
                        currentNote = 2
                else:
                    pitch = notes[currentNote]
                    currentNote = (currentNote + 1) % 3
                self.MyMIDI.addNote(2, 0, pitch, time, int(960/rate), 100, annotation=None)
                time = int(time+(960/rate))

  def movement(self, c,b):
      c_output = c/float(self.c2c_max)
      b_output = b/float(self.c2b_max)
      return (0.5*c_output) + (0.5*b_output)

  def find_nearest(self, array, value):
      array = np.asarray(array)
      idx = (np.abs(array - value)).argmin()
      return array[idx]

  def makeSong(self):
      self.makeMelody()
      self.makeDrums()
      self.arpeggio()
      with open(self.csvName.replace(".csv","")+"_sound.mid", 'wb') as output_file:#save the midi file
          self.MyMIDI.writeFile(output_file)
      return self.MyMIDI
