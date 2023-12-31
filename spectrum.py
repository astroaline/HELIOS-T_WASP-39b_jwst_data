# -*- coding: utf-8 -*-

import logging
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator, NullLocator
from matplotlib.colors import LinearSegmentedColormap, colorConverter
from matplotlib.ticker import ScalarFormatter
from scipy.stats import norm
import matplotlib
from input import *
import itertools

try:
    from scipy.ndimage import gaussian_filter
except ImportError:
    gaussian_filter = None

__all__ = ["corner", "hist2d", "quantile"]

matplotlib.rc('text', usetex=True)
matplotlib.rc('font', family='serif')


def spec(xs, xfull, xbin, yfull, ybin, ydata, x_err, y_err, range2, color_list, bins=20, range=None, weights=None, color="k",
         smooth=None, smooth1d=None,
         labels=None, label_kwargs=None,
         show_titles=False, title_fmt=".2f", title_kwargs=None,
         truths=None, truth_color="k",
         #ini_guess = [None]*(len(parameters)-2) + [(rstar,rstar_uncertainty), (g,g_uncertainty)],
         density=True,
         scale_hist=False, quantiles=None, verbose=False, fig=None,
         max_n_ticks=5, top_ticks=False, use_math_text=False, reverse=False,
         hist_kwargs=None, **hist2d_kwargs):
           

    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')

    # Create a new figure if one wasn't provided.
    fig2, ax2 = plt.subplots(figsize=(35, 15))   # fig, axes = plt.subplots(K, K, figsize=(dim, dim))

    # Format the figure.
#    lb = lbdim / dim
#    tr = (lbdim + plotdim) / dim
#    fig.subplots_adjust(left=lb, bottom=lb, right=tr, top=tr, wspace=whspace, hspace=whspace)

    ax2.set_frame_on(True)
    ax2.xaxis.set_tick_params(top=True)
    ax2.yaxis.set_tick_params(right=True)
    linethick = 3
    line1, = ax2.plot(xfull, yfull, linewidth=linethick, color='#069af3', linestyle='-')
    symsize2 = 1
    mew1 = 4
    msize = 6
    elw = 1.5
    ax2.errorbar(xbin, ybin, xerr=x_err, yerr=y_err, fmt='ks', elinewidth=elw)
    ax2.plot(xbin, ybin, 'ks', mew=mew1, markersize=msize)
    symsize = 4
    ax2.errorbar(xbin, ydata, xerr=x_err, yerr=y_err, fmt='ro', capthick=2, elinewidth=elw, zorder=1000)
    ax2.plot(xbin, ydata, 'ro', mew=mew1, markersize=msize, zorder=1000)
    text_size = 50
    wavelength_min, wavelength_max = np.amin(wavelength_centre), np.amax(wavelength_centre)
    transit_min, transit_max = np.amin(transit_depth), np.amax(transit_depth)
    ax2.set_title(planet_name, loc='right', size=text_size*1.3, pad=20)
    ax2.text(0.03, 0.89, r'\textbf{NIRSpec G395H data}', transform=ax2.transAxes, color='r', fontsize=text_size*0.9)
    ax2.text(0.03, 0.82, r'\textbf{Model (binned)}', transform=ax2.transAxes, color='k', fontsize=text_size*0.9)
    ax2.set_xlim([wavelength_min - 0.03, wavelength_max + 0.03])
    ax2.set_ylim([transit_min - 0.02*transit_min, transit_max + 0.02*transit_max])
    ax2.xaxis.set_major_locator(MaxNLocator(5, prune="lower"))
    ax2.yaxis.set_major_locator(MaxNLocator(5, prune="lower"))
    ax2.xaxis.set_major_formatter(ScalarFormatter(useMathText=use_math_text))
    ax2.yaxis.set_major_formatter(ScalarFormatter(useMathText=use_math_text))
    tick_label_size = text_size*1.1
    tick_size = 20
    ax2.tick_params(axis='both', which='major', direction='in', length=tick_size, labelsize=tick_label_size, pad=15)
    label_size = text_size*1.1
    ax2.set_xlabel(r'Wavelength ($\mu$m)', fontsize=label_size, labelpad=15)
    ax2.set_ylabel(r'($R$/$R_{\rm star}$)$^2$ (\%)', fontsize=label_size, labelpad=20)
    #ax2.set_xlabel(r'\textbf{Wavelength (}\boldmath{$\mu$}\textbf{m)}', fontsize=label_size, labelpad=100)
    #ax2.set_ylabel(r'\textbf{(}\boldmath{$R$/$R_{\rm star}$}\textbf{)}\boldmath{$^2$} \textbf{ (\%)}', fontsize=label_size, labelpad=100)
    #ax2.xaxis.set_label_coords(0.5, -0.08)
    #y_label_x = -0.25 + 0.06*K/3
    #ax2.yaxis.set_label_coords(y_label_x, 0.5)

    return fig2
