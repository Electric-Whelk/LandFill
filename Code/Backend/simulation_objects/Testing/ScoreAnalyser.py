import json
import statistics

import numpy as np
import pandas as pd
import scipy
from matplotlib import pyplot as plt
from statsmodels.distributions import ECDF

#names = ["AllBasics", "CheckDeck", "ShockDeck", "HalfwayThere", "AsIBuild"]
#formal_names = ["BasicDeck", "CheckDeck," "ShockDeck", "PartialDeck", "ExpectedDeck"]

names = ["AllBasics", "CheckDeck", "ShockDeck", "HalfwayThere", "AsIBuild", "NoBasics"]
formal_names = ["BasicDeck", "CheckDeck", "ShockDeck", "PartialDeck", "ExpectedDeck", "OverDeck"]

def assemble_dict(input, formalinput):
    output = {}
    for name, formal in zip(input, formalinput):
        with open(f"output_files/deck_assessment_multiruns/{name}.json", "r") as file:
            data = json.load(file)
        output[formal] = data.get("outputs")
    return output

def get_means(input):
    d = []
    order = []
    for key in input:
        d.append([np.mean(x) for x in input[key]])
        order.append(key)
    draw_boxplot(d, order)

def get_proportions(input):
    d = []
    order = []
    for key in input:
        d.append([get_single_proportion(x) for x in input[key]])
        order.append(key)

    draw_boxplot(d, order)

def get_cumulatived(input):
    d = []
    order = []
    for key in input:
        d.append([get_single_cumulatived(x) for x in input[key]])
        order.append(key)
    draw_boxplot(d, order)


def get_single_cumulatived(input):
        e = ECDF(input)
        x = list(e.x[1:])
        y = list(e.y[1:])
        x.append(30)
        y.append(1)
        from scipy.integrate import trapezoid

        area = trapezoid(x=x, y=y)
        return area

def get_single_proportion(input):
    zeroes = []
    for item in input:
        if item == 0:
            zeroes.append(0)
    return len(zeroes)/len(input)

def draw_boxplot(d, labels):
    fig = plt.figure()

    ax = fig.add_subplot(111)
    ax.boxplot(d)

    #plt.boxplot(d)
    plt.tight_layout()
    ax.set_xticklabels(labels)
    plt.show()

def get_histograms(input):
    for key in input:
        plt.hist(input[key][0])
        plt.show()


def get_stats(input):
    all_data = []
    for key in input:
        data = input[key][0]

        #mean median mode range kurtosis
        tmp = [key, np.mean(data), np.median(data), statistics.mode(data), np.ptp(data), scipy.stats.kurtosis(data)]
        all_data.append(tmp)

    df = pd.DataFrame(all_data, columns=['player_deck', 'Mean', 'Median', 'Mode', 'Range', 'Kurtosis'])
    print(df)

def data_for_mum(input):
    columns = []
    all_data = []
    for key in input:
        columns.append(key)
    for i in range(len(input["BasicDeck"])):
        tmp = []
        for key in input:
            tmp.append(get_single_proportion(input[key]))
        all_data.append(tmp)

    df = pd.DataFrame(all_data, columns=columns)
    print(df)



rawdata = assemble_dict(names, formal_names)
data_for_mum(rawdata)

