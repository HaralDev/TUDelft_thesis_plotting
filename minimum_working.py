#!/usr/bin/env python3
import os
import pandas as pd
import matplotlib.pyplot as plt 
import matplotlib
import seaborn as sns
import numpy as np
from matplotlib import rcParams
from mpl_toolkits.axes_grid1 import make_axes_locatable
from statistics import mean
from datetime import datetime
#-------------------------------------------------------------------------------------------------


#-------------------------------------------------------------------------------------------------
#           Matplotlib settings

rcParams.update({'figure.autolayout': True})    # https://matplotlib.org/3.1.1/tutorials/intermediate/tight_layout_guide.html
matplotlib.font_manager._rebuild()

# COLOURS
# Colors don't actually match names
# Make another palette at https://coolors.co/ or any other palette generator
CB91_Blue = '#235B59'
CB91_Pink = '#93CA97'
CB91_Green = '#149B80'
CB91_Purple = '#FDCE78'
CB91_Violet = '#EC3730'
color_list = [  CB91_Blue, CB91_Pink, CB91_Green,
                CB91_Purple, CB91_Violet]
plt.rcParams['axes.prop_cycle'] = plt.cycler(color=color_list)
plt.style.use('seaborn')

# LATEX
# https://jwalton.info/Embed-Publication-Matplotlib-Latex/
font = 'Utopia'     # TU Delft thesis font 
WIDTH = 448.1309    # Width of document, see https://jwalton.info/Embed-Publication-Matplotlib-Latex/

tex_fonts = {
    # Use LaTeX to write all text
    "text.usetex": False,
    "font.family":'serif',
    'font.serif':font,
    # Use 10pt font in plots, to match 10pt font in document
    "axes.labelsize": 10,
    "font.size": 10,
    # Make the legend/label fonts a little smaller
    "legend.fontsize": 8,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8
}
plt.rcParams.update(tex_fonts)


#-------------------------------------------------------------------------------------------------

#============================================================================================
#       SUPPORT PLOTS

#--------------------------------------------------------------------------------------------
def get_timestamp():
    """Useful for filenames"""
    now = datetime.now()
    time_local = now.strftime("%Y_%m_%d_%H_%M_%S")

    return time_local

#--------------------------------------------------------------------------------------------
def legend_without_duplicate_labels(plt, loc='upper right'):
    """From https://stackoverflow.com/questions/13588920/stop-matplotlib-repeating-labels-in-legend"""
    handles, labels = plt.gca().get_legend_handles_labels()
    labels, handles = zip(*sorted(zip(labels, handles), key=lambda t: t[0]))    # https://stackoverflow.com/questions/22263807/how-is-order-of-items-in-matplotlib-legend-determined
    by_label = dict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys(), loc=loc, fancybox=True, frameon =True, facecolor='white', framealpha=0.7)

#--------------------------------------------------------------------------------------------
def set_size(fraction=1, height=False):
    """Set figure dimensions to avoid scaling in LaTeX.
    https://jwalton.info/Embed-Publication-Matplotlib-Latex/
    Parameters
    ----------
    WIDTH: float
            Document textwidth or columnwidth in pts
    fraction: float, optional
            Fraction of the width which you wish the figure to occupy

    Returns
    -------
    fig_dim: tuple
            Dimensions of figure in inches
    """
    # Width of figure (in pts)
    fig_width_pt = WIDTH * fraction

    # Convert from pt to inches
    inches_per_pt = 1 / 72.27

    # Golden ratio to set aesthetic figure height
    # https://disq.us/p/2940ij3
    golden_ratio = (5**.5 - 1) / 2

    # Figure width in inches
    fig_width_in = fig_width_pt * inches_per_pt
    # Figure height in inches
    fig_height_in = fig_width_in * golden_ratio
    if height:
        fig_height_in = fig_width_in * height
    fig_dim = (fig_width_in, fig_height_in)

    return fig_dim




#============================================================================================
#       EXAMPLE PLOTS           
#--------------------------------------------------------------------------------------------
def plot_all_colours():

    for ind, col in enumerate(color_list):
        x  = np.linspace(0, 10, 10)
        y = [x * 1 + ind for x in x]
        plt.plot(x, y, color=col, label=col)
        # print(x, y)
    plt.legend()
    plt.xlabel("X-label")
    plt.ylabel("Y-label")
    plt.show()

#--------------------------------------------------------------------------------------------
def get_mean_error_theta(df):
    """Returns the mean, max error and the Series of diff between hall_theta and motor_theta"""
    hall_theta = df.filter(like="hall_theta")
    motor_theta = df.filter(like="motor_theta")
    max_motor_incrs = 93450
    theta_diff = abs(hall_theta.values - motor_theta.values) / max_motor_incrs * 100
    theta_diff = np.nan_to_num(theta_diff, nan=0)   # https://numpy.org/doc/stable/reference/generated/numpy.nan_to_num.html
    theta_diff_avg = round(theta_diff.mean(),2)
    theta_diff_max = round(theta_diff.max(),2)

    return theta_diff_avg, theta_diff, theta_diff_max


def plot_positions_with_error_and_power(file_path, figure_name, motor_name, width=0.8, hours=False, pow_except=""):
    """Plots the positions throughout the test with the error above and power below."""
    fig, ax1 = plt.subplots(nrows=2,figsize=set_size(), sharex=True)

    # Make diff plot
    # https://matplotlib.org/mpl_toolkits/axes_grid/users/overview.html
    divider = make_axes_locatable(ax1[0])
    ax2 = divider.append_axes("top", 0.5, pad=0.05, sharex=ax1[0])
    plt.setp(ax2.get_xticklabels(),
            visible=False)
 
    # Get data
    df = pd.read_csv(file_path)
    cols = list(df)

    # Select columns
    if pow_except:
        print(pow_except)
        pow_cols = [col for col in cols if "Power" in col and "total" not in col.lower() and pow_except not in col]
        print(pow_cols)
    else:
        pow_cols = [col for col in cols if "Power" in col and "total" not in col.lower()]

    hall_theta = df.filter(like="hall_theta")
    motor_theta = df.filter(like="motor_theta")
    time = (df["Time since start [s]"] - df["Time since start [s]"][0])
    if hours:
        time = time /3600 

    theta_diff_avg, theta_diff, theta_diff_max = get_mean_error_theta(df)

    # Plot pow columns
    for col in pow_cols:
        data = df[col]
        col_name = col.strip("Power [W]").strip("HMC8041").strip('2').strip("-").strip().strip("- ")
        ax1[1].plot(time, data, label=col_name, linewidth=width)


    # Plot positions
    ax1[0].plot(time, hall_theta, color=CB91_Blue, linewidth=width, label="Actual position")
    ax1[0].plot(time, motor_theta, color=CB91_Green, linewidth=width, linestyle='dashed', label="Commanded position")
    ax2.plot(time, theta_diff, linewidth=width, label="Position error", zorder=1)
    ax2.hlines(theta_diff_avg, xmin=time.iloc[0], xmax=time.iloc[-1], linestyle='dashed',linewidth=0.5, label=f"Mean: {theta_diff_avg} %", zorder=2)

    # Legend
    ax1[0].legend(frameon =True, facecolor='white', framealpha=0.95)
    ax1[1].legend(frameon =True, facecolor='white', framealpha=0.95)
    ax2.legend(frameon =True, facecolor='white', framealpha=0.95)

    # Labels
    ax1[0].set_ylabel("Motor\nposition []")
    ax2.set_ylabel("Error [%]")
    ax1[1].set_ylabel("Power [W]")
    if hours:
        ax1[1].set_xlabel("Test time [hrs]")     # [Hrs] for hours
    else:
        ax1[1].set_xlabel("Test time [s]")     # [Hrs] for hours
    
    # Save and end
    fig.savefig(figure_name)
    plt.show() 
#============================================================================================

if __name__ == "__main__":
    
    # plot_all_colours()
    motor = "EM1"
    figure_name = f"{get_timestamp}_example_plot.pdf"  
    file_name = "data_file_example.csv"
    plot_positions_with_error_and_power(file_name,figure_name, motor, width=0.7, hours=True)

