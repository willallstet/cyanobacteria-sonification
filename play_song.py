import live
import os
import math

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

set = live.Set()
set.scan(scan_clip_names = True, scan_devices = True)
track = set.tracks[0]
style = track.devices[0]
rate = track.devices[3]
style = track.devices[0]

while bool(self.clip_playing):
    time = 0
    max = self.num_cells_added.max()
    min = self.num_cells_added.min()
    for i in self.num_cells_added:
        set.wait_for_next_beat()
        if not time > len(num_cells_added):
            if(self.num_cells_added[time]<0):
                rate = math.floor((abs(self.num_cells_added[time]/min)*9)+3)
            if(self.num_cells_added[time]>0):
                rate = math.floor((abs(self.num_cells_added[time]/max)*9)+3)
        time = time+1
