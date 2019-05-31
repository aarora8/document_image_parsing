#!/bin/bash
# This script runs the example_4 script in parallel.

nj=30
cmd=queue.pl
echo "$0 $@"

. ./cmd.sh
. ./path.sh
. ./utils/parse_options.sh || exit 1;

input_dir=$1
output_dir=$2
logdir=$output_dir/log
scp=$input_dir/room_info

mkdir -p $logdir
mkdir -p $output_dir

# make $featdir an absolute pathname
output_dir=`perl -e '($dir,$pwd)= @ARGV; if($dir!~m:^/:) { $dir = "$pwd/$dir"; } print $dir; ' $output_dir ${PWD}`
for n in $(seq $nj); do
    split_scps="$split_scps $output_dir/room_info.$n.scp"
done

# split images.scp
utils/split_scp.pl $scp $split_scps || exit 1;

$cmd JOB=1:$nj $logdir/extract_rir.JOB.log \
  local/example_5.py $output_dir/room_info.JOB.scp $output_dir
