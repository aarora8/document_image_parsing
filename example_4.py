#!/usr/bin/env python3
import roomsimove_single
import numpy as np
import argparse
import os
import random
import soundfile as sf

parser = argparse.ArgumentParser(description="""Creates line images from page image.""")
parser.add_argument('database_path', type=str,
                    help='Path to the downloaded (and extracted) mdacat data')
parser.add_argument('out_dir', type=str, help='Where to write output files.')
args = parser.parse_args()
sampling_rate = 16000

### main ###
text_fh = open(args.database_path, 'r')
text_data = text_fh.read().strip().split("\n")
id = 0
for line in text_data:
  id +=1
  print(line)
  line = line.split(" ")
  room_x = float(line[1])
  room_y = float(line[2])
  room_z = float(line[3])
  mic_x = float(line[4])
  mic_y = float(line[5])
  mic_z = float(line[6])
  #source_x = float(line[7])
  #source_y = float(line[8])
  #source_z = float(line[9])
  absorption = float(line[7])
  room_dim = [room_x, room_y, room_z] # in meters
  mic_pos = [mic_x, mic_y, mic_z] # in  meters
  #source_pos = [source_x, source_y, source_z] # in  meters
  room = roomsimove_single.Room(room_dim, abs_coeff=absorption)
  mic = roomsimove_single.Microphone(mic_pos, 1,orientation=[0.0, 0.0, 0.0], direction='omnidirectional')
  mics = [mic]
  sim_rir = roomsimove_single.RoomSim(sampling_rate, room, mics)

  rir = sim_rir.create_rir(source_pos)
  #print(len(rir))
  roomID = line[0].split("-")[1]
  rir_dir = os.path.join(args.out_dir, roomID)
  rir_filename = os.path.join(args.out_dir, roomID, str(id) + '.wav')
  if not os.path.exists(rir_dir):
    os.makedirs(rir_dir)
  sf.write(rir_filename, rir, sampling_rate)
