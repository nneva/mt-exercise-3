#! /bin/env/python

import argparse
import logging
import sys
import time

from collections import Counter
from itertools import chain

from nltk.tokenize import sent_tokenize, WordPunctTokenizer
import nltk


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--vocab-size", type=int, help="Size of vocabulary", required=True)
    parser.add_argument("--tokenize", action="store_true", help="Assume input strings are not tokenized yet.", required=False)
    parser.add_argument("--unk-string", type=str, help="String to use for out-of-vocabulary tokens.", default="<unk>", required=False)
    parser.add_argument("--sent-tokenize", action="store_true", help="Assume sentences span several lines.", required=False)
    parser.add_argument("--language", type=str, help="Language full name.", default="english")

    args = parser.parse_args()

    return args


def main():

    tic = time.time()

    args = parse_args()

    logging.basicConfig(level=logging.DEBUG)
    logging.debug(args)

    if args.tokenize:
        tokenizer = WordPunctTokenizer()

    if args.sent_tokenize:
        text = sys.stdin.read()
        lines = sent_tokenize(text, language=args.language)
    else:
        lines = sys.stdin.readlines()

    all_tokens = []

    for line in lines:
        if args.tokenize:
            t = tokenizer.tokenize(line)
        else:
            t = line.split()
        all_tokens.append(t)

    flat_tokens = chain.from_iterable(all_tokens)

    counter = Counter(flat_tokens)

    # try to free up memory early
    # nice :)
    del flat_tokens

    logging.debug("Vocabulary size before/after/max_allowed = %d/%d/%d" % (len(counter.keys()), min(args.vocab_size, len(counter.keys())), args.vocab_size))

    vocabulary = [token for token, frequency in counter.most_common(args.vocab_size)]

    for tokens in all_tokens:
        output_tokens = []
        for token in tokens:
            if token in vocabulary:
                output_tokens.append(token)
            else:
                output_tokens.append(args.unk_string)

        output_string = " ".join(output_tokens)
        sys.stdout.write(output_string + "\n")

    toc = time.time() - tic

    logging.debug("Time taken: %f seconds" % toc)
    

if __name__ == '__main__':
    main()
