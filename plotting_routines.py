import numpy as np
import matplotlib.pyplot as plt
import qutip as qt
import time
import matplotlib as mpl 

def plot1d_commonx(xs, yseries, ax=None, plot_style=None, legend=None):
	'''
		For series of y data with common x index

	'''
	if ax is None:
		fig = plt.figure()
		ax = fig.subplot(111)
	
	for i, ys in enumerate(yseries):
		if plot_style is None:
			ax.plot(xs, ys)
		else:
			ax.plot(xs, ys, plot_style[i])

	if legend is not None:
		ax.legend(legend, loc='best')

	return ax

# todo: dictionary replace so I can use **kwargs for AxesGrid options
def multiple_imshow(xs, ys, zs, labels=None):
    
    def get_im_extent(xs, ys, data):
        return data, (xs.min(), xs.max(), ys.min(), ys.max())
    def get_element(ins, index):
        ins = np.array(ins)
        # check if <ins> is a 1D array
        if len(ins.shape) == 1:
            return ins
        else:
            return ins[index]
    
    from mpl_toolkits.axes_grid1 import AxesGrid
    
    fig = plt.figure(figsize=(10.,6.))
    grid = AxesGrid(fig, 111,
                     nrows_ncols=(1,3),
                     axes_pad=0.25,
                     aspect=False,
                     share_all=True,
                     cbar_location='top',
                     cbar_mode='each',
                     cbar_size=r'10%',
                     cbar_pad=r'5%'
                     )
    for i in range(len(zs)):
        
        x = get_element(xs, i)
        y = get_element(ys, i)
        values, extent = get_im_extent(x, y, zs[i])

        im = grid[i].imshow(values, extent=extent, aspect='auto', interpolation='nearest')
        ax = plt.gca()
        grid.cbar_axes[i].colorbar(im)
        
def get_plot_extent(xs, ys):
    '''
        Generates the extent of a given 2D plot based on the x and y series.

        Inputs
            - xs, ys: 1D arrays delineating the series bounds
        Outputs
            - extent: tuple describing the corners of the 2D plot
    '''
    return xs[0], ys[0], xs[-1], ys[-1]


def get_cmap_list(cmap, num_colors):

        cmap = mpl.cm.get_cmap(name=cmap) #I gues we can also use "hsv" or "gist_rainbow" 

        color_list = [] 
        for i in np.linspace(0, 1, num_colors):
            color_list.append(cmap(i))
        
        # mpl.axes.set_default_color_cycle(color_list)
        return color_list