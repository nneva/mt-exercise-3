#! /bin/bash

scripts=`dirname "$0"`
base=$scripts/..

data=$base/data

mkdir -p $data

tools=$base/tools

# link default training data for easier access

mkdir -p $data/wikitext-2

for corpus in train valid test; do
    absolute_path=$(realpath $tools/pytorch-examples/word_language_model/data/wikitext-2/$corpus.txt)
    ln -snf $absolute_path $data/wikitext-2/$corpus.txt
done

# download a different interesting data set!

mkdir -p $data/dorian

mkdir -p $data/dorian/raw

wget https://www.gutenberg.org/cache/epub/174/pg174.txt
mv pg174.txt $data/dorian/raw/the_picture_of_dorian_gray.txt

# preprocess slightly

cat $data/dorian/raw/the_picture_of_dorian_gray.txt | python $base/scripts/preprocess_raw.py > $data/dorian/raw/the_picture_of_dorian_gray.cleaned.txt

# tokenize, fix vocabulary upper bound

cat $data/dorian/raw/the_picture_of_dorian_gray.cleaned.txt | python $base/scripts/preprocess.py --vocab-size 5000 --tokenize --language english --sent-tokenize > \
    $data/dorian/raw/the_picture_of_dorian_gray.preprocessed.txt

# split into train, valid and test

head -n 353 $data/dorian/raw/the_picture_of_dorian_gray.preprocessed.txt | tail -n 329 > $data/dorian/valid.txt
head -n 655 $data/dorian/raw/the_picture_of_dorian_gray.preprocessed.txt | tail -n 352 > $data/dorian/test.txt
tail -n 4859 $data/dorian/raw/the_picture_of_dorian_gray.preprocessed.txt | head -n 4744 > $data/dorian/train.txt
