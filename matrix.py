#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Object-oriented rewrite of percolation2d.py."""

from matplotlib    import pyplot
from matplotlib    import colors
from random        import random
from numpy         import interp


def vect(dim):
    """Returns the list of possible vector displacements in a specific dimension."""

    vectors = []
    for direction in range(dim):
        for side in [-1, 1]:
            vector = [0]*dim
            vector[direction] = side
            vectors.append(vector)
    return vectors


def regression(size_x, size_y, samples, iterations, color='blue'):
    """Draw a curve of porosity indice by probability."""

    matrix = Matrice2d(size_y, size_y)
    indices = []
    percolations = []

    for sample in range(samples+1):
        indice = interp(sample, [0, samples], [0, 1])
        percolation = 0

        for iteration in range(iterations+1):
            matrix.reset()
            matrix.randomize(indice)
            matrix.borders()
            matrix.rain()
            if matrix.percolate():
                percolation += 1

        indices.append(indice)
        percolations.append(percolation/(iterations+1))
        print("Sample", sample, "/", samples)

    pyplot.plot(indices, percolations, color=color)
    pyplot.show()


class Matrice2d:
    """A class for manipulating basic 2D matrixes. Full of usefull functions when dealing with percolation."""

    WALL        = -1
    STONE       = 0
    EMPTY       = 1
    WATER       = 2
    MOVINGWATER = 3

    clrs = ['black', 'grey', 'white', 'blue', 'cyan']
    vals  = [WALL, STONE, EMPTY, WATER, MOVINGWATER]
    cmap = colors.ListedColormap(clrs)
    norm = colors.BoundaryNorm(vals + [max(vals)+1], cmap.N)


    def __init__(self, x, y, data=None):
        """Constructor. If no data is specified, the matrix is full of 0s."""

        if data == None:
            data = [0]*x
            for i in range(x):
                data[i] = [0]*y

        self.x    = x
        self.y    = y
        self.data = data


    def __str__(self):
        return str(self.data)


    def reset(self):
        """Fills the matrix with 0s."""

        self.__init__(self.x, self.y)


    def randomize(self, indice=.5):
        """Populates the matrix with Bernoulli data."""

        for x, line in enumerate(self.data):
            for y, cell in enumerate(line):
                if random() < indice:
                    self.data[x][y] = self.EMPTY


    def borders(self):
        """Puts the matrix in a jar."""

        for x, line in enumerate(self.data):
            self.data[x] = [self.WALL]+line+[self.WALL]

        self.data.append([self.WALL]*(self.y+2))


    def rain(self):
        """Adds moving water at the top line of the matrix."""

        for y, cell in enumerate(self.data[0]):
            if cell == self.EMPTY:
                self.data[0][y] = self.MOVINGWATER


    def percolate(self, moving_water=None, draw_graphics=False):
        """Recursive function wich performs a percolation."""

        if moving_water == None:
            moving_water = self.get_moving_water()

        if moving_water != []:

            if draw_graphics:
                self.draw(.0001)

            empty_cells = []
            for (x, y) in moving_water:
                close_empty_cells = self.get_close_empty_cells(x, y)
                for (u, v) in close_empty_cells:
                    self.data[u][v] = self.MOVINGWATER
                self.data[x][y] = self.WATER
                empty_cells += close_empty_cells
            self.percolate(empty_cells, draw_graphics)

            return self.is_percolated()


    def draw(self, time=1):
        """Draw the matrix using MatPlotLib."""

        pyplot.matshow(self.data, 1, cmap=self.cmap, norm=self.norm)
        pyplot.pause(time)


    def get_moving_water(self):
        """Returns moving water."""

        moving_water = []
        for x, line in enumerate(self.data):
            for y, cell in enumerate(line):
                if cell == self.MOVINGWATER:
                    moving_water.append((x, y))
        return moving_water


    def get_close_empty_cells(self, x, y):
        """Returns the coords of all empty cells near to (x, y)."""

        empty_cells = []
        for v in vect(2):
                if self.data[x+v[0]][y+v[1]] == self.EMPTY:
                    empty_cells.append((x+v[0], y+v[1]))
        return empty_cells


    def is_percolated(self):
        """Returns True in case of percolation."""

        for cell in self.data[self.x-1]:
            if cell == self.WATER or cell == self.MOVINGWATER:
                return True
        return False


if __name__ == '__main__':
    testmat = Matrice2d(1, 5, [[-1, 0, 1, 2, 3]])
    testmat.draw()

    matrix = Matrice2d(50, 50)

    matrix.randomize(0.6)
    matrix.borders()
    matrix.rain()

    print(matrice.percolate(draw_graphics=True))

    regression(12, 6, 512, 128, color='cyan')
