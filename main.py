from dcel import *
from findIntersection import FindIntersections
from segment import Segment
from dcel1 import dcel as dcel1
from dcel2 import dcel as dcel2
import numpy as np


if __name__ == '__main__':
    F = FindIntersections()
    new_dcel = F.map_overlay(dcel1, dcel2)
    print(new_dcel.faces)
    new_dcel.plot_dcel()

