from numpy.random import uniform
import matplotlib.pyplot as plt

from spaceplot import spaceplots

def test_spaceplots():
    xs = uniform(size=(10000, 4))
    ys = uniform(size=(10000, 2))
    in_names = ['a', 'b', 'c', 'd']
    out_names = ['A', 'B']
    for plot in spaceplots(
        xs, ys, input_names=in_names, output_names=out_names
    ):
        plt.show()
        plt.close(plot)
