#! /bin/bash

scripts=`dirname "$0"`
base=$(realpath $scripts/..)

models=$base/models
data=$base/data
tools=$base/tools

mkdir -p $models

num_threads=4
device=""

SECONDS=0

# dropout values used: 0.0, 0.175, 0.35, 0.525, 0.7, 0.875, rename model.pt accordingly

(cd $tools/pytorch-examples/word_language_model &&
    CUDA_VISIBLE_DEVICES=$device OMP_NUM_THREADS=$num_threads python main.py --data $data/dorian \
        --epochs 40 \
        --lr 20.0 \
        --log-interval 100 \
        --emsize 200 --nhid 200 --dropout 0.0 --tied \
        --save $models/model.pt
)

echo "time taken:"
echo "$SECONDS seconds"
