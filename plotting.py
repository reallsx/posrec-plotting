import matplotlib.pyplot as plt
import matplotlib
import numpy as np

def plot_2d_err(data, true, ax, xlabel = True, ylabel = True, vmax = None):
    '''
    Plot 2d error and print bias, rms on the plot

    parameters:
    data: array of (n,2)
        (x,y) coordinate of reconstructed position
    true: array of (n,2)
        (x,y) coordinate of true position
    ax: matplotlib axis
        the axis to plot
    xlabel: bool
        decide  if adding xlabel to the subplot
    ylabel: bool
        decide  if adding ylabel to the subplot

    return: image
        the 3rd returned object in ax.hist2d.
        for making colorbar later.
    '''

    # calculate the error and make histogram
    err = data - true
    
    h = ax.hist2d(err[:,0],  err[:,1], range=((-3, 3), (-3, 3)), bins=(200, 200), 
           norm=matplotlib.colors.LogNorm(vmin=1, vmax=vmax))

    #-------------------------------------------------------------------->
    ticks = np.linspace(-3,3,7)

    ax.set_xticks(ticks)
    ax.set_yticks(ticks)

    if xlabel:
        ax.set_xlabel(r'x [cm]')
    ax.grid(True)
    if ylabel:
        ax.set_ylabel(r'y [cm]')
    ax.grid(True)
    
    ax.set_aspect('equal', 'box')
    
    # Calculate bias and rms and print on plot

    bias = np.sum(err, axis = 0) / len(true)
    rms = np.std(err, axis = 0)

    text_X= ax.text(0.03,0.95,"x, mean : %1.4f, RMS : %1.4f"%(bias[0],rms[0] ), 
             transform = ax.transAxes, ha = "left", va="center" , fontsize=12, c="b")

    text_Y=ax.text(0.03,0.89,"y, mean : %1.4f, RMS : %1.4f"%(bias[1],rms[1] ), 
             transform = ax.transAxes, ha = "left", va="center" , fontsize=12, c="b")

    return h[3]


def plot_r_err_vs_r2(data, true, ax, max_r,vmax = None):
    '''
    Plot radius error (reconstructed radius - true radius) vs true radius

    parameters:
    data: array of (n,2)
        (x,y) coordinate of reconstructed position
    true: array of (n,2)
        (x,y) coordinate of true position
    ax: matplotlib axis
        the axis to plot
    max_r: float
        the radius of detector

    return: image
        the 3rd returned object in ax.hist2d.
        for making colorbar later.
    '''

    h = ax.hist2d(np.sum(true**2, axis = 1), np.sqrt(np.sum(data**2, axis = 1)) - np.sqrt(np.sum(true**2, axis = 1)), 
            bins = (100,100), norm=matplotlib.colors.LogNorm(vmin=1, vmax=vmax))
    
    ax.set_ylim((-2.5,2.5))
    ax.axvline(max_r**2, color='black', linestyle='-', linewidth = 1.5, alpha = 1)
    ax.axhline(0, color='black', linestyle='--', linewidth = 1.5, alpha = 0.5)
    ax.tick_params(axis = 'x', direction = "in")

    return h[3]


def _bin_by_area(upper, lower, s2_size):
    '''
    Select hit patterns with area between upper and lower boundry of a bin.
    '''
    size_cut = (s2_size > lower) & (s2_size < upper)
        
    return size_cut


def quantile_by_area(data, true, area, bins, ax, quantile = 0.393):
    '''
    Compute and plot the quantile for absolute error in each area bin

    parameters:
    data: array of (n,2)
        (x,y) coordinate of reconstructed position
    true: array of (n,2)
        (x,y) coordinate of true position
    area: array of (n,)
        (top) area of the hitpattern
    bins: 1d array 
        boundry of area bins
    ax: matplotlib axis
        the axis to plot
    quantile: float (default 0.393)
        quantile of absolute error to compute
        0.393 corresponding to 1 sigma of 2d gaussian distribution

    return: 1d array
        computed quantile of each bin
    '''

    absolute_error = np.sqrt((data[:,0] - true[:,0]) ** 2 + (data[:,1] - true[:,1]) ** 2)

    bin_quantile = np.zeros(len(bins)-1)

    # bin by area and calculate quantile for each bin
    for i in range(len(bins) - 1):
        in_bin = (area > bins[i]) & (area < bins[i+1])
        bin_quantile[i] = np.quantile(absolute_error[in_bin], q = quantile)

    ax.step(bins[:-1], bin_quantile, alpha = 0.5,  where = "mid")

    return bin_quantile
