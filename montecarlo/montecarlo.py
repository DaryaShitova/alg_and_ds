from random import random
from rectangle import Rectangle
import numpy as np


class MonteCarlo:

    def __init__(self, length, width, rectangles):
        """constructor
        :param length - length of the enclosing rectangle
        :param width - width of the enclosing rectangle
        :param rectangles - array that contains the embedded rectangles
        :raises ValueError if any of the paramters is None
        """
        if length is None or width is None or rectangles is None:
            raise ValueError("One of the parameters is missing.")

        self.length = length
        self.width = width

        #Creating the enclosing rectangular by a 2d numpy array of the size length*width with all values set to 0
        self.mc = np.zeros((length, width))
        #Creating the embedded recrangular by setting the corresponding values in the enclosing rectangulat to 1
        for rect in rectangles:
            self.mc[int(rect.origin_x):int(rect.origin_x + rect.length), int(rect.origin_y):int(rect.origin_y + rect.width)] = 1


    def area(self, num_of_shots):
        """Method "area "to estimate the area of the enclosing rectangle that is not covered by the embedded rectangles
        :param num_of_shots - Number (>0) of generated random points whose location (inside/outside) is analyzed
        :return float
        :raises ValueError if any of the paramters is None
        """
        if num_of_shots is None:
            raise ValueError("One of the parameters is missing.")

        #Calculators whether the shot hit the enclosing or the embedded rectangular.
        inside = 0
        outside = 0

        #Creating random (x,y) for the shot and checking what it hit, thus updating the calculator accordingly.
        for i in range(num_of_shots):
            x = int(random()*self.length)
            y = int(random()*self.width)
            inside_bool = MonteCarlo.inside(self, x, y, self.mc)
            if inside_bool is True:
                inside += 1
            else:
                outside += 1
        #Calculating the area
        area = self.length*self.width*inside/(inside+outside)
        return area

    def inside(self, x, y, rect):
        """Method "inside" to determine if a given point (x,y) is inside a given rectangle
        :param x,y - coordinates of the point to check
        :param rect - given rectangle
        :return bool
        :raises ValueError if any of the paramters is None
        """
        if x is None or y is None or rect is None:
            raise ValueError("One of the parameters is missing.")

        #Checking if the shot has hit the enclosing or an embedded rectangular
        if self.mc[x][y] == [0]:
            return True
        else:
            return False




