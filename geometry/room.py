#!/usr/bin/python3.4

'''
Room geometry class module for Ray Tracing Method 4-dimensional visualization.
'''

__author__ = 'Norbert Mieczkowski'
__copyright__ = 'Copyright 2015, Norbert Mieczkowski'
__version__ = '1.0.0'


class Room():

    def __init__(self, points, faces, abs):
        '''
        Class defining room geometry, contains all information needed for rendering such as points, faces and materials.
        :param points: dictionary of all room points {id: (x, y, z)}
        :param faces: dictionary of all room faces {id: (point01, point02, ..., material_name)}
        :param abs: dictionary of all room materials {name: (freq01, freq02, ..., R, G, B)}
        '''
        self.points = points
        self.faces = faces
        self.abs = abs
        self.average_alpha = self._compute_average_alpha()
        self.boundaries = self._compute_boundaries()

    def _compute_average_alpha(self):
        '''
        Method computing average alpha for each of 6 frequencies (125 Hz, 250 Hz, 500 Hz, 1000 Hz, 2000 Hz, 4000 Hz)
        :return: dict of average alphas with frequency values as keys
        '''
        average_alpha = [0] * 6   # define list of length 6 to store alpha coefficients
        for key in self.abs:   # iterate over all materials
            material = self.abs[key]   # assigning current material to a variable
            average_alpha = [average_alpha[i] + material[i] for i in range(6)]   # adding material alphas to each other
        materials_count = len(self.abs)   # specifying count of all materials
        average_alpha = [average_alpha[i] / materials_count for i in range(6)]   # dividing each sum by materials count
        return {   # returning computed average alphas
            125:  average_alpha[0],
            250:  average_alpha[1],
            500:  average_alpha[2],
            1000: average_alpha[3],
            2000: average_alpha[4],
            4000: average_alpha[5],
        }

    def _compute_boundaries(self):
        '''
        Method computing room boundaries.
        :return: dictionary of maximum and minimum point in each axis {'min_x': ?.??, 'max_x': ?.??, 'min_y: ?.??, ...}
        '''
        x = [self.points[point][0] for point in self.points]   # getting all X axis values
        y = [self.points[point][1] for point in self.points]   # getting all Y axis values
        z = [self.points[point][2] for point in self.points]   # getting all Z axis value
        return {
            'min_x': min(x),
            'max_x': max(x),
            'min_y': min(y),
            'max_y': max(y),
            'min_z': min(z),
            'max_z': max(z)
        }
