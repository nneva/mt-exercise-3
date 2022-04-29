# MT Exercise 3: Pytorch RNN Language Models

This repository shows how to train Neural Language Models using [Pytorch example code](https://github.com/pytorch/examples/tree/master/word_language_model).

# Requirements

- This only works on a Unix-like system, with bash.
- Python 3 must be installed on your system, i.e. the command `python3` must be available
- Make sure virtualenv is installed on your system. To install, e.g.

        pip install virtualenv


# Steps

🧑‍🤝‍🧑 **Clone this repository in the desired place:**

    git clone https://github.com/nneva/mt-exercise-3
    cd mt-exercise-3

💻 **Create a new virtualenv that uses Python 3.** 

Please make sure to run this command outside of any virtual Python environment:

    ./scripts/make_virtualenv.sh

- **Important**: Activate the env by executing the `source` command that is output by the shell script above.

🛠️ **Download and install required software:**

    ./scripts/install_packages.sh

If needed, run once a following download in `preprocess.py`

    nltk.download('punkt')

⬇️ **Download and preprocess data:**

    ./scripts/download_data.sh

- Data set used was downloaded from the following link: https://www.gutenberg.org/cache/epub/174/pg174.txt .

- Script `preprocess_raw.py` is slightly adjusted to match formatting of the new data set.

- Tokenization in `preprocess.py` is adjusted to match tokenization of the example file(s).


🤸 **Train a model:**

    ./scripts/train.sh | tee -a infographic/output.txt

 - The training process can be interrupted at any time, and the best checkpoint will always be saved.

- There is no output during the training. The output will be displayed at the end of the training for each model, and saved in file **infographic/output.txt** for all models.

- Approximate (average) time needed for the training of each model is 20 minutes with 4 threads.

- Initilize the training manually for each model using paramateres listed below, and rename model accordingly.

- `Dropout` values used for the training are: **0.0**, **0.175**, **0.35**, **0.525**, **0.7**, **0.875**. 

    **Important:** Models should be trained ordered by dropout value, from lowest to highest.

- Number of `epochs` for each model is **40**. 

- `Learning rate` used is default: **20.0**.

- Other settings: `word embeddings size` and `number of hidden units per layer` are set to **200**.

📈 **Graphical representation of results:**

For graphical representation of the training results run a following command:

    ./scripts/visualize.sh

- Exact location of the generated tables and graphs will be printed out into the terminal.

🪄 **Generate (sample) some text from a trained model with:**

    ./scripts/generate.sh

- Model chosen for generation has the lowest `test perplexity` among the models trained, **62.89**, and is trained with the `dropout` value of **0.35**.

🧑‍🤝‍🧑 **Clone repository `pytorch/examples`:**

    git clone https://github.com/nneva/examples

- **Important:** Place cloned reposotory in the directory `mt-exercise-3`.

📝 **Test command line prompt for text generation with:**

    python examples/word_language_model/generate.py --data data/dorian --words 500 --checkpoint models/model_0_35.pt --seed 1211 --temperature 1.4 --input "< desired input >"

- Argument `--input` is optional.

- Lines modified: 30 and 31, and from 56 to 142.


              




