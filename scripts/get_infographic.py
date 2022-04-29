#! /bin/env/python

import argparse
import matplotlib.pyplot as plt
import pandas as pd
import re
import seaborn as sns
from typing import Tuple, List

# not aesthetically pleasing script, but magic of Python
# further remarks in README.md/Graphical representation of the training results

#TODO: comments and docs

def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--input-file", type=str, help="File path of the input file.", required=True)
    parser.add_argument("--save-charts", type=str, help="Path to save charts.", required=True)
    parser.add_argument("--save-tables", type=str, help="Path to save tables.", required=True)

    args = parser.parse_args()

    return args


def get_ppl(text: str) -> Tuple[Tuple[str, List[str]]]:
    
    ppl = re.findall(r"\|\sppl.+(.+[0-9]+[0-9]+\.[0-9]+)", text)
    valid_ppl = re.findall(r"\|\svalid\sppl.+(.+[0-9]+[0-9]+\.[0-9]+)", text)
    test_ppl = re.findall(r"\|\stest\sppl.+(.+[0-9]+[0-9]+\.[0-9]+)", text)
    
    return ("Train. perplexity", ppl), ("Valid. perplexity", valid_ppl), ("Test perplexity", test_ppl)


def get_data_frame(dropout: List[str], epochs:List[str], ppl: Tuple[str, List[str]]) -> pd.DataFrame:
    idx = 0
    df = pd.DataFrame(columns= [ppl[0]] + ["Dropout" + " " + do for do in dropout])

    if len(ppl[1]) == 240:
        df[ppl[0]] = pd.Series(epochs)
        for do in dropout:
            df["Dropout" + " " + do] = pd.Series(ppl[1][idx:idx + 40])
            idx += 40
    else:
        df.loc[""] = ["End of training"] + ppl[1]

    return df


def save_charts(chart:str, table: pd.DataFrame, ppl: str):

    sns.set(font_scale=1.5, style="darkgrid")
    table = table.drop(ppl[0], axis=1).apply(pd.to_numeric)
    sns.relplot(data=table, kind="line", palette="tab10", height=9, aspect=1.5).set(title=ppl[0], ylabel="Perplexity", xlabel="Epoch")
    plt.savefig(chart + "/{}.png".format(ppl[0].lower().replace(" ", "_")))


def main():

    dropout = ["0.0", "0.175", "0.35", "0.525", "0.7", "0.875"]
    epochs = ["epoch " + str(idx) for idx in range(1, 41)]

    args = parse_args()

    with open(args.input_file, "r") as f:
        text = f.read()

    ppls = get_ppl(text)
    chart = args.save_charts
    tab = args.save_tables

    for ppl in ppls:
        table = get_data_frame(dropout, epochs, ppl)
        table.to_markdown(tab + "/{}.md".format(ppl[0].lower().replace(" ", "_")), index=False)
        if len(ppl[1]) == 240:
            save_charts(chart, table, ppl)

    print("\033[92m" + "Charts and tables are in directories infographic/charts and infographic/tables." + "\033[0m")

    
if __name__ == '__main__':
    main()