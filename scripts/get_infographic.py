#! /bin/env/python

import argparse
import matplotlib.pyplot as plt
import pandas as pd
import re
import seaborn as sns
from typing import Tuple, List


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--input-file", type=str, 
                        help="File path of the input file.", required=True)
    parser.add_argument("--save-charts", type=str, 
                        help="Path to save charts.", required=True)
    parser.add_argument("--save-tables", type=str, 
                        help="Path to save tables.", required=True)

    args = parser.parse_args()

    return args


def get_ppl(text: str) -> List[Tuple[str, List[str]]]:
    """Extract perplexity values for each of the perplexities: 
                training, validation, and test.
    :param text: A file containing data from the training output.
    :return: Corresponding values for each of the perplexities as a list of tuples.
    """
    PPLs = []
    pattern = r".+(.+[0-9]+[0-9]+\.[0-9]+)"
    patterns = ["\|\sppl", "\|\svalid\sppl", "\|\stest\sppl"]
    PPL = ["Train. perplexity", "Valid. perplexity", "Test perplexity"]

    for name, part in zip(PPL, patterns):
        ppl = re.findall(part + pattern, text)
        PPLs.append((name, ppl))

    return PPLs


def get_data_frame(dropout: List[str], epochs:List[str], 
                    ppl: Tuple[str, List[str]]) -> pd.DataFrame:
    """Generate data frame for creating tables and graphs:
        :param dropout: List containing dropout values to define columns.
        :param epochs: List containong the epochs to define rows.
        :param ppl: Tuple containing name of the perplexity and its corresponding values.
        :return: Data frame for each of the perplexities.
    """
    idx = 0
    df = pd.DataFrame(columns= [ppl[0]] + ["Dropout" + " " + do for do in dropout])

    if len(ppl[1]) == 240:
        df[ppl[0]] = pd.Series(epochs)
        for do in dropout:
            df["Dropout" + " " + do] = pd.Series(ppl[1][idx:idx + 40])
            idx += 40
    else:
        # Due to mismatch in a number of rows, data frame for test perplexity is generated differently.
        df.loc[""] = ["End of training"] + ppl[1]

    return df


def save_charts(chart:str, table: pd.DataFrame, ppl: Tuple[str, List[str]]):
    """Generate line chart for train. and valid. perplexity.
        :param chart: Path to save a line chart as string.
        :param table: Data frame for the corresponding perplexity.
        :param ppl: uple containing name of the perplexity and its corresponding values.
    """
    sns.set(font_scale=1.5, style="darkgrid")
    # Values are actually str, converted to numbers with pd.to_numeric.
    table = table.drop(ppl[0], axis=1).apply(pd.to_numeric)
    # This line couldn't be shorter, affects the performance.
    sns.relplot(data=table, kind="line", palette="tab10", height=9, aspect=1.5).set(title=ppl[0], ylabel="Perplexity", xlabel="Epoch")
    plt.savefig(chart + "/{}.png".format(ppl[0].lower().replace(" ", "_")))


def main():

    dropout = ["0.0", "0.175", "0.35", "0.525", "0.7", "0.875"]
    epochs = ["epoch " + str(idx) for idx in range(1, 41)]

    args = parse_args()

    with open(args.input_file, "r") as f:
        text = f.read()
    # Extract perplexity values.
    ppls = get_ppl(text)

    chart = args.save_charts
    tab = args.save_tables

    for ppl in ppls:
        # Create a data frame for each perplexity.
        table = get_data_frame(dropout, epochs, ppl)
        # Choose .md format to generate a table. 
        table.to_markdown(tab + "/{}.md".format(ppl[0].lower().replace(" ", "_")), index=False)
        # Save line charts for train. and valid. perplexity.
        if len(ppl[1]) == 240:
            save_charts(chart, table, ppl)

    print("\033[92m" + "Charts and tables are in directories infographic/charts and infographic/tables." + "\033[0m")

    
if __name__ == '__main__':
    main()