import numpy
from matplotlib import pyplot as plt
from numpy import gradient

from scipy.signal import savgol_filter



def multi_deck_analysis():
    #load both decks
    with open('output_files/halt_criteria_testing/xav_no_mandatory', 'r') as file:
        no_man = [float(l.strip()) for l in file.readlines()]
    with open('output_files/halt_criteria_testing/xav_typical_input', 'r') as file:
        typ_inp = [float(l.strip()) for l in file.readlines()]

    no_man_sg_small = rolling_savgol(no_man, 3)
    no_man_av = rolling_average(no_man)
    no_man_sg_large = rolling_savgol(no_man, 11)

    three_line_plot(no_man, no_man_sg_large, no_man_av)
    three_line_plot(no_man, no_man_sg_small, no_man_av)

    plt.plot(no_man)
    plt.grid(lw=2,ls=':')
    plt.xlabel('Increment')
    plt.ylabel("Score")
    #plt.legend()
    plt.show()

    #typ_inp_av = rolling_average(typ_inp)
    #typ_inp_sg = rolling_savgol(typ_inp)
    #three_line_plot(no_man, no_man_sg, no_man_av)
    #three_line_plot(typ_inp, typ_inp_sg, typ_inp_av)


def three_line_plot(raw_scores, savgol, rolling_av):
    plt.plot(raw_scores, label='raw scores', color='green')
    plt.plot(savgol, label='savgol', color='red')
    plt.plot(rolling_av, label='rolling av', color='blue')
    plt.grid(lw=2, ls=':')
    plt.xlabel('Increment')
    plt.ylabel("Score")
    plt.legend()
    plt.show()
    pass


def rolling_savgol(data, window_size):
    #window_size = 3
    poly_order = 2
    rolling = []
    for i in range(len(data)):
        if i < window_size:
            rolling.append(0)
        else:
            subsect = data[0:i]
            rollingsav = savgol_filter(subsect, window_size, poly_order)
            rolling.append(gradient(rollingsav)[-1])
    return rolling

def rolling_average(data):
    rolling = []
    window_size = 3
    improvement_threshold = 0

    for i in range(len(data)):
        if i < 2*window_size:
            rolling.append(0)
        else:
            scores = data[0:i]
            prior_window = scores[len(scores) - 2 * window_size: len(scores) - window_size]
            recent_window = scores[len(scores) - window_size:]

            best_recent = numpy.mean(recent_window)
            best_prior = numpy.mean(prior_window)

            improvement = best_recent - best_prior


            rolling.append(improvement)

    return rolling



def simple_analysis():
    #load lines
    with open('output_files/halt_criteria_testing/scoreslog.txt', 'r') as file:
        lines = file.readlines()
        lines = [float(l.strip()) for l in lines]

    window_size = 11
    poly_order = 3
    y_smooth = savgol_filter(lines, window_size, poly_order)
    grad = gradient(y_smooth)

    #do a version where you're always just looking at the latest savgol value
    rolling = []
    diff = []
    for i in range(11, len(lines)):
        subsect = lines[0:i]
        rollingsav = savgol_filter(subsect, window_size, poly_order)
        rolling.append(rollingsav[-1])
        print(y_smooth[i] - rollingsav[-1])

    plt.plot(lines, label='Noisy Signal')
    plt.plot(y_smooth, label='Smoothed Signal', color='red')
    plt.plot(rollingsav, label='rsav', color='blue')
    plt.grid(lw=2,ls=':')
    plt.xlabel('Time Step')
    plt.ylabel("Value")
    plt.legend()
    plt.show()

multi_deck_analysis()