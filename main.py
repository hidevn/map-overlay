from dcel import *
from mapOverlay import MapOverlay
from segment import Segment
from dcel1 import dcel as dcel1
from dcel2 import dcel as dcel2
import numpy as np


if __name__ == '__main__':
    F = MapOverlay()
    new_dcel, _ = F.calculate(dcel1, dcel2)
    #print(new_dcel.faces)
    new_dcel.plot_dcel()

