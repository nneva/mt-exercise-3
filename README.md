# MT Exercise 3: Pytorch RNN Language Models

This repository shows how to implement command line input prompt and train Neural Language Models using [Pytorch example code](https://github.com/pytorch/examples/tree/master/word_language_model).

# Requirements

- This only works on a Unix-like system, with bash.
- Python 3 must be installed on your system, i.e. the command `python3` must be available
- Make sure virtualenv is installed on your system. To install, e.g.

        pip install virtualenv


# Steps

🧑‍🤝‍🧑 **Clone this repository in the desired place:**

    git clone https://github.com/nneva/prompt-rnn-lm
    cd prompt-rnn-lm

💻 **Create a new virtualenv that uses Python 3.** 

Please make sure to run this command outside of any virtual Python environment:

    ./scripts/make_virtualenv.sh

- **Important**: Activate the env by executing the `source` command that is output by the shell script above.

🛠️ **Download and install required software:**

    ./scripts/install_packages.sh


⬇️ **Download and preprocess data:**

To download data you can use command below.

    ./scripts/download_data.sh

- Example data set used for this project was downloaded from [Project Gutenberg](https://www.gutenberg.org/cache/epub/174/pg174.txt ). 

- You shoud preprocess your data with script `preprocess_raw.py` and tokennize it with script `preprocess.py`


🤸 **Train a model:**

To train your model execute the following command:

    ./scripts/train.sh 

 - The training process can be interrupted at any time, and the best checkpoint will always be saved.

- Approximate (average) time needed for the training of each model is 20 minutes with 4 threads.

Recommended hyperparameters settings:

- Number of `epochs` **40**. 

- `Learning rate` default: **20.0**.

- Other settings: `word embeddings size` and `number of hidden units per layer` are set to **200**.


# Inference
You can use one of the pretrained models to generate text. To do so:

🧑‍🤝‍🧑 **Clone repository**

    git clone https://github.com/nneva/examples


and run script. 

    ./scripts/generate.sh


File with generated text will be saved at  **samples/sample.txt**.




📝 **Test command line prompt for text generation**


This time make sure that the script `generate.sh` has flag `--input True`.

```bash
    (cd $examples/word_language_model &&
    CUDA_VISIBLE_DEVICES=$device OMP_NUM_THREADS=$num_threads python generate.py \
        --data $data/dorian \
        --words 500 \
        --checkpoint $models/model_0_35.pt \
        --outf $samples/sample.txt \
        --temperature 0.6 \
        --input True
    )
```

After running the script in your command line you will see the following message:

    Please specifiy words to start generation from:

You can now type the words of your choice and the generation will continue from there.
              




