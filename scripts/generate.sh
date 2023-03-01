#! /bin/bash

scripts=`dirname "$0"`
base=$(realpath $scripts/..)

models=$base/models
data=$base/data
examples=$base/examples
samples=$base/samples

mkdir -p $samples

num_threads=4
device=""

(cd $examples/word_language_model &&
    CUDA_VISIBLE_DEVICES=$device OMP_NUM_THREADS=$num_threads python generate.py \
        --data $data/dorian \
        --words 500 \
        --checkpoint $models/model_0_35.pt \
        --outf $samples/sample.txt \
        --temperature 0.6 \
        --input True
)
