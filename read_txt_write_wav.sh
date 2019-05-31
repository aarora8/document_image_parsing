#!/bin/bash
# Copyright 2016  Tom Ko
# Apache 2.0
# Script to simulate room impulse responses (RIRs)

# This script uses the image method based on an implementation
# by Habets et al to simulate the room impulse responses (RIRs).
# It samples the room parameters and receiver position in the room
# and then randomly generate a number of RIRs according to different speaker positions.
# To use this script you need to have MATLAB installed and
# download the RIR generator from
# https://github.com/ehabets/RIR-Generator/blob/master/rir_generator.cpp

# This script reads RIR in .txt format and writes it into .wav format
# Usage: prep_sim_rirs.sh <output-dir>
# E.g. prep_sim_rirs.sh data/simulated_rir_largeroom

input_dir=$1
output_dir=$2
prefix="medium-"       # prefix to the RIR id
sampling_rate=16000     # Sampling rate of the output RIR waveform
output_bit=16
mkdir -p $output_dir

cat >./genrir.m <<EOF
output_dir = '$output_dir';
input_dir = '$input_dir';
RIRset_prefix = '$prefix';
BitsPerSample = $output_bit;
fs = $sampling_rate;
listing = dir(input_dir);
isub = [listing(:).isdir];
nameFolds = {listing(isub).name};
nameFolds(ismember(nameFolds,{'.','..'})) = [];
for i = 1:length(nameFolds)
  directorycell = nameFolds(i);
  directoryname = directorycell{1};
  list = dir(strcat(input_dir, '/', directoryname, '/*.txt'));
  mkdir(output_dir,directoryname)
  for j = 1:length(list)
    txtfilename = list(j).name;
    %strcat(input_dir, '/', directoryname, '/', txtfilename)
    fileID = fopen(strcat(input_dir, '/', directoryname,'/', txtfilename),'r');
    RIR = fscanf(fileID,'%f');
    [filepath,filename,ext] = fileparts(txtfilename);
    wavfilename = strcat(output_dir, '/', directoryname, '/', filename, '.wav');
    audiowrite(wavfilename, RIR, fs, 'BitsPerSample', BitsPerSample);
  end
end
EOF
matlab -nosplash -nodesktop < ./genrir.m
rm genrir.m
