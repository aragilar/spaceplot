

from numpy import array as _array
from matplotlib.colors import Normalize as _Normalize
from matplotlib.gridspec import GridSpec as _GridSpec
from matplotlib.pyplot import figure as _figure


def spaceplots(
    inputs, outputs, input_names=None, output_names=None, limits=None, **kwargs
):
    num_samples, num_inputs = inputs.shape
    if input_names is not None:
        if len(input_names) != num_inputs:
            raise RuntimeError("Input data and names don't match")
    else:
        input_names = [None] * num_inputs

    out_num_samples, num_outputs = outputs.shape
    if out_num_samples != num_samples:
        raise RuntimeError("Inputs and outputs don't match")
    if output_names is not None:
        if len(output_names) != num_outputs:
            raise RuntimeError("Output data and names don't match")
    else:
        output_names = [None] * num_outputs

    if limits is not None:
        if limits.shape[1] != 2:
            raise RuntimeError(
                "There must be a upper and lower limit for each output"
            )
        elif limits.shape[0] != num_outputs:
            raise RuntimeError("Output data and limits don't match")
    else:
        limits = [[None, None]] * num_outputs

    for out_index in range(num_outputs):
        yield _subspace_plot(
            inputs, outputs[:, out_index], input_names=input_names,
            output_name=output_names[out_index], min_output=limits[out_index][0],
            max_output=limits[out_index][1], **kwargs
        )


def _setup_axes(
    *, input_names, histogram_labels=False, constrained_layout=True
):
    num_inputs = len(input_names)
    fig = _figure(constrained_layout=constrained_layout)
    axes = _array(
        [[None] * num_inputs for _ in range(num_inputs)],
        dtype=object
    )

    grid = _GridSpec(
        nrows=num_inputs, ncols=num_inputs, figure=fig,
    )

    common_tick_args = dict(
        top=True,
        bottom=True,
        left=True,
        right=True,
        direction='in',
    )

    for i in range(num_inputs):
        axes[i, i] = fig.add_subplot(grid[i, i])
        axes[i, i].tick_params(
            labelbottom=False, labelleft=False, labelright=histogram_labels,
            **common_tick_args
        )

    for y in range(num_inputs):
        for x in range(y):
            plot_args = dict(sharex=axes[x, x])
            if y != 0:
                plot_args["sharey"] = axes[y, 0]
            axes[y, x] = fig.add_subplot(grid[y, x], **plot_args)

            if x != 0:
                axes[y, x].tick_params(labelleft=False, **common_tick_args)
            else:
                axes[y, x].set_ylabel(input_names[y])

            if y != num_inputs - 1:
                axes[y, x].tick_params(labelbottom=False, **common_tick_args)
            else:
                axes[y, x].set_xlabel(input_names[x])

    return fig, axes, grid


def _subspace_plot(
    inputs, output, *, input_names, output_name, scatter_args=None,
    histogram_args=None, min_output=None, max_output=None
):
    if scatter_args is None:
        scatter_args = {}
    if histogram_args is None:
        histogram_args = {}
    if min_output is None:
        min_output = min(output)
    if max_output is None:
        max_output = max(output)

    # see https://matplotlib.org/examples/pylab_examples/multi_image.html
    _, num_inputs = inputs.shape

    fig, axes, grid = _setup_axes(input_names=input_names)

    if output_name is not None:
        fig.suptitle(output_name)

    norm = _Normalize(min_output, max_output)

    hist_plots = []
    for i in range(num_inputs):
        hist_plots.append(_plot_hist(
            inputs[:, i], axis=axes[i][i], **histogram_args
        ))

    scatter_plots = []
    scatter_plots_grid = []
    for y_index in range(num_inputs):
        scatter_plots_grid.append([])
        for x_index in range(y_index):
            sc_plot = _plot_scatter(
                x=inputs[:, x_index], y=inputs[:, y_index], z=output,
                axis=axes[y_index][x_index],  # check order
                norm=norm, **scatter_args
            )
            scatter_plots.append(sc_plot)
            scatter_plots_grid[y_index].append(sc_plot)

    cbar_ax = fig.add_subplot(grid[0, 1:])
    fig.colorbar(
        scatter_plots[0], cax=cbar_ax, orientation='horizontal',
    )
    cbar_ax.set_aspect(1/20)

    return fig


def _plot_hist(values, *, axis, **kwargs):
    return axis.hist(values, **kwargs)


def _plot_scatter(*, x, y, z, axis, norm, **kwargs):
    return axis.scatter(x=x, y=y, c=z, norm=norm, **kwargs)


from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
