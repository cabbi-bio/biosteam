# -*- coding: utf-8 -*-
"""
Created on Mon Sep  2 05:01:11 2019

@author: yoelr
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from biosteam._utils.plot_utils import DoubleColorCircle, DoubleColorLegend
from biosteam import colors

__all__ = ('plot_montecarlo', 'plot_montecarlo_across_coordinate',
           'annotate_line', 'plot_single_points', 'plot_spearman')

def plot_spearman(rhos, top=None):
    """Display Spearman's rank correlation plot.
    
    Parameters
    ----------
    rhos : pandas.Series
         Spearman's rank correlation coefficients to be plotted.
    top=None : float, optional
        Number of parameters to plot (from highest values).
    
    Returns
    -------
    fig : matplotlib Figure
    ax : matplotlib AxesSubplot
    """
    # Sort parameters for plot
    abs_ = abs
    name = rhos.name
    rhos, index = zip(*sorted(zip(rhos, rhos.index),
                              key=lambda x: abs_(x[0])))
    if top:
        rhos = rhos[-top:]
        index = index[-top:]
    
    xranges = [(0, i) for i in rhos]
    yranges = [(i, 1) for i in range(len(rhos))]
    
    # Plot bars one by one
    fig, ax = plt.subplots()
    for x, y in zip(xranges, yranges):
        ax.broken_barh([x], y, facecolors=colors.blue_tint.RGBn,
                       edgecolors=colors.blue_dark.RGBn)
    
    ax.set_xlim(-1, 1)
    ax.set_xlabel(f"{name} " + r"$\mathrm{\rho}_{spearman}$")
    ax.set_yticks([i[0]+i[1]/2 for i in yranges])
    ax.set_yticklabels(index)
    ax.grid(False)
    
    return fig, ax


# %% Plot metrics vs coordinate

light_color = colors.brown_tint.RGBn
dark_color = colors.brown_shade.RGBn

def plot_vertial_line(x, color='grey'):
    """Plot vertical line."""
    plt.axvline(x=x, color=color) 

def plot_single_points(xs, ys, color=dark_color):
    """Plot single points and return patch artist."""
    return plt.scatter(xs, ys, marker='o', s=50, color=color, zorder=1e6, edgecolor='black') 

def plot_montecarlo(data, 
                    light_color=light_color,
                    dark_color=dark_color,
                    position=0):
    """Return box plot of Monte Carlo evaluation.
    
    Parameters
    ----------
    data : numpy.ndarray(ndim=1)
        Metric values with uncertainty.
    light_color : numpy.ndarray
        RGB normalized to 1. Defaults to brown.
    dark_color : numpy.ndarray
        RGB normalized to 1. Defaults to brown.
        
    Returns
    -------
    bx : Patch
    
    """
    bx = plt.boxplot(x=data, positions=[position], patch_artist=True,
                     widths=0.8, whis=[5, 95],
                     boxprops={'facecolor':light_color,
                               'edgecolor':dark_color},
                     medianprops={'color':dark_color,
                                  'linewidth':1.5},
                     flierprops = {'marker':'D',
                                   'markerfacecolor': light_color,
                                   'markeredgecolor': dark_color,
                                   'markersize':6})
    return bx

def plot_montecarlo_across_coordinate(xs, ys, 
                                      light_color=light_color,
                                      dark_color=dark_color):
    """
    Plot Monte Carlo evaluation across a coordinate.
    
    Parameters
    ----------
    xs : numpy.ndarray(ndim=1)
        Coordinate values for each column in ``ys``.
    ys : numpy.ndarray(ndim=2)
        Metric values with uncertainty.
    light_color : numpy.ndarray
        RGB normalized to 1. Defaults to brown.
    dark_color : numpy.ndarray
        RGB normalized to 1. Defaults to brown.
    
    Returns
    -------
    percentiles : numpy.ndarray(ndim=2)
        5, 25, 50, 75 and 95th percentiles by row (5 rows total).
    
    """
    q05, q25, q50, q75, q95 = percentiles = np.percentile(ys, [5,25,50,75,95], axis=0)

    # Create line graph vs lipid fraction
    plt.plot(xs, q50, '-',
             color=dark_color,
             linewidth=1.5) # Median
    plt.fill_between(xs, q25, q50,
                     color=light_color,
                     linewidth=1.0) # Lower quartile
    plt.fill_between(xs, q75, q50,
                     color=light_color,
                     linewidth=1.0) # Upper quartile
    plt.plot(xs, q05, '-.',
             color=dark_color,
             linewidth=1.0) # Lower whisker
    plt.plot(xs, q95, '-.',
             color=dark_color,
             linewidth=1.0) # Upper whisker
    
    return percentiles

# def estimate_ylim(lower, upper, ylim=()):
#     if ylim:
#         ylim[0] = min([ylim[0], min(lower)])
#         ylim[1] = max([ylim[1], max(upper)])
#     else:
#         ylim = (0.95*min(lower), 1.05*max(upper))
#     return ylim    
    
def expand(lower, upper, lb, ub):
    dx = (upper - lower)/12
    return max(lower-dx, lb), min(upper+dx, ub)

def closest_index(x, xs):
    if xs[0] < xs[-1]:
        for i, xi in enumerate(xs):
            if x < xi: break
    else:
        for i, xi in enumerate(xs):
            if x > xi: break
    return i

def annotate_line(text, x, xs, ys, dy=0.2, dy_text=0.22, position='under', 
                  color=colors.brown_shade.RGBn):
    """Annotate line with text and arrow pointing to text.
    
    Parameters
    ----------
    text : str
    x : float
        Arrow position
    xs : numpy.ndarray(dim=1)
    ys : numpy.ndarray(dim=1)
    dy : float
        Length of arrow to y-position.
    dy_text : float
        Distance of text to arrow.
    position : {'under', 'over'}
        Relative position of text to line.
    color : numpy.ndarray
        RGB normalized to 1. Defaults to brown.
    
    """
    index = closest_index(x, xs)
    x = xs[index]
    y = ys[index]
    if position == 'under':
        y *= 0.998
        y_text = y - dy - dy_text
    elif position == 'over':
        y *= 1.002
        y_text = y + dy + dy_text
    else:
        raise ValueError(f"position must be either 'over' or 'under', not '{position}'")
    dx = 0
    color = 0.60*color
    plt.arrow(x, y, dx, dy, linestyle='-', alpha=0.8, color=color, linewidth=1)
    plt.text(x, y_text, text, color=0.75*color, horizontalalignment='center', fontsize=12)
    


