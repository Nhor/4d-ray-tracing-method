#!/usr/bin/python3.4

'''
Main window and basic GUI widgets module for Ray Tracing Method 4-dimensional visualization.
'''

from math import cos, log10, pi, sin

from PyQt5.QtWidgets import QOpenGLWidget
from PyQt5.QtCore import QBasicTimer
from OpenGL.GL import *
from OpenGL.GLU import *

__author__ = 'Norbert Mieczkowski'
__copyright__ = 'Copyright 2015, Norbert Mieczkowski'
__version__ = '1.0.0'


class OpenGLWidget(QOpenGLWidget):

    def __init__(self, *args, **kwargs):
        '''
        Class representing OpenGL widget in the VisualizationWindow.
        '''
        super(OpenGLWidget, self).__init__(*args, **kwargs)
        self._room = self.parent().room   # assign room geometry to a variable
        self.setGeometry(self.parent()._width * .25, 0, self.parent()._width, self.parent()._height)   # window size/pos
        self._timer = QBasicTimer()   # create a timer

    def initializeGL(self):
        '''
        A method to initialize all OpenGL features.
        '''
        glClearColor(.22, .22, .22, 1)   # set background color to gray
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)   # make sure to clear everything at the beginning
        glClearDepth(1)   # set background depth to farthest
        glEnable(GL_DEPTH_TEST)   # enable depth testing for z-culling
        glDepthFunc(GL_LEQUAL)   # set the type of depth-test
        glShadeModel(GL_SMOOTH)   # enable smooth shading
        glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)   # nice perspective corrections
        glMatrixMode(GL_PROJECTION)   # necessary for a nice perspective view
        glLoadIdentity()   # necessary for a nice perspective view
        gluPerspective(45, (self.width() / self.height()), .1, 50.0)   # configure perspective view
        glMatrixMode(GL_MODELVIEW)   # necessary for a nice model view
        glLoadIdentity()   # necessary for a nice model view
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)   # wireframe rendering method
        gluLookAt(   # camera position and looking point
            -15, 8, -15,
            -3, 0, 0,
            0, 1, 0
        )

    def paintGL(self):
        '''
        A method to paint in OpenGL.
        '''
        glClearColor(.22, .22, .22, 1)   # set background color to gray
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)   # clear everything before rendering next frame

        self._draw_grid()   # drawing grid lines
        self._draw_room()   # drawing room geometry

        if self._timer.isActive():   # if animation is initialized
            self._draw_particles()   # draw sound waves represented by particles

    def timerEvent(self, QTimerEvent):
        '''
        An overridden method of what happens on each self._timer tick.
        Warning! This method should only be used by self.initialize_animation()!!
        :param QTimerEvent: should be ignored
        '''
        self.update()   # calling self.update() in order to refresh the widget

    def initialize_animation(self, source_pos=(0,0,0), source_spl=80, source_freq=1000, fps=60):
        '''
        A method to animate the ray tracing method in 4D.
        :param source_pos: source position tuple
        :param source_spl: source sound pressure level
        :param source_freq: source sound frequency
        '''
        self._source_pos = source_pos
        self._source_spl = source_spl
        self._source_power = 10 ** (self._source_spl * .1)
        self._source_freq = source_freq
        self._calculate_particles_normals_positions_energies()
        self._timer.start(1000 / fps, self)

    def _draw_grid(self):
        '''
        A method to draw grid lines.
        '''
        glLineWidth(1)   # width of a single grid line
        glColor3f(.29, .29, .29, 1)   # color of a single grid line (gray)
        glBegin(GL_LINES)   # tell OpenGL to draw lines
        grid_lines = 10   # grid lines range (meaning its gird lines number / 4)
        for i in range(-grid_lines, grid_lines + 1):   # drawing grid lines
            glVertex3f(-grid_lines, 0, i)   # draw a horizontal line
            glVertex3f(grid_lines, 0, i)
            glVertex3f(i, 0, -grid_lines)   # draw a vertical line
            glVertex3f(i, 0, grid_lines)
        glColor3f(.52, .07, .07, 1)   # change line color to red
        glVertex3f(-grid_lines, 0, 0)   # draw red grid line
        glVertex3f(grid_lines, 0, 0)
        glColor3f(.07, .52, .07, 1)   # change line color to green
        glVertex3f(0, 0, -grid_lines)   # draw green grid line
        glVertex3f(0, 0, grid_lines)
        glEnd()   # tell OpenGL to stop drawing

    def _draw_room(self):
        '''
        A method to draw room geometry.
        '''
        faces = self._room.faces   # store room faces in a new variable
        points = self._room.points   # store room points in a new variable
        glColor3f(.59, .59, .62, 1)   # color of an edge (light gray)
        for id in faces:   # iterate through all faces
            glBegin(GL_POLYGON)   # tell OpenGL to draw a polygon
            for point_id in faces[id][:-1]:   # iterate through all points in a single face
                glVertex3fv(points[point_id])   # draw a single point
            glEnd()   # tell OpenGL to stop drawing

    def _draw_particles(self):
        '''
        A method to draw sound waves represented by particles.
        '''
        glBegin(GL_POINTS)   # tell OpenGL to draw points
        for index, particle in enumerate(self._particles_positions):   # iterate through all particles
            green = self._particles_energies[index] / self._source_spl   # computing green color share in rgb palette
            red = 1 - green   # computing red color share in rgb palette
            glColor3f(red, green, 0, 1)   # color of a particle (initially green, then turning red)
            glVertex3f(particle[0], particle[1], particle[2])   # draw each particle
        self._recalculate_particles_normals()   # recalculate particles normals
        self._recalculate_particles_positions()   # recalculate particles positions
        glEnd()   # stop drawing

    def _calculate_particles_normals_positions_energies(self):
        '''
        A method to calculate normal vectors of all particles.
        Warning! This method should be used only after initialize_animation()!
        '''
        particles_count = 15   # not the exact particles count, number of particles in a single ring
        radius = .5   # radius of starting sphere
        self._particles_normals = []   # list of all particles normals
        self._particles_positions = []   # list of all particles current positions
        self._particles_energies = []   # list of all particles energies that reduce each time a particle reflects
        for i in range(0, particles_count):   # iterate through each ring of particles
            for j in range(0, particles_count):   # iterate through each particle in the current ring
                x = cos(2*pi * j / (particles_count-1)) * sin(pi * i / (particles_count-1))   # x position of particle
                y = sin(-pi/2 + pi * i / (particles_count-1))   # y position of particle
                z = sin(2*pi * j / (particles_count-1)) * sin(pi * i / (particles_count-1))   # z position of particle
                self._particles_normals.append([x, y, z])   # add normal vector of each particle to the list
                self._particles_positions.append([x*radius+self._source_pos[0],   # add position of each particle
                                                  y*radius+self._source_pos[1],   # to the list
                                                  z*radius+self._source_pos[2]])
                self._particles_energies.append(self._source_spl)   # each particle has energy equal to source spl

    def _recalculate_particles_normals(self):
        '''
        A method to recalculate all particles normals in each frame.
        Recalculates particles energies within each reflection and removes the particles with energy level below 60dB.
        '''
        self._particles_to_delete = []   # a list with indexes of particles with energy level below 60dB
        for index, particle in enumerate(self._particles_positions):   # iterate through all particles
            if particle[0] <= self._room.boundaries['min_x'] or particle[0] >= self._room.boundaries['max_x']:
                self._compute_new_particle_normal_and_reduce_energy('x', index)   # react to particle reflection
            elif particle[1] <= self._room.boundaries['min_y'] or particle[1] >= self._room.boundaries['max_y']:
                self._compute_new_particle_normal_and_reduce_energy('y', index)   # react to particle reflection
            elif particle[2] <= self._room.boundaries['min_z'] or particle[2] >= self._room.boundaries['max_z']:
                self._compute_new_particle_normal_and_reduce_energy('z', index)   # react to particle reflection
        for particle in sorted(self._particles_to_delete, reverse=True):   # deleting particles with energy below 60dB
            del self._particles_normals[particle]
            del self._particles_positions[particle]
            del self._particles_energies[particle]

    def _recalculate_particles_positions(self):
        '''
        A method to recalculate all particles positions in each frame.
        '''
        for index, particle in enumerate(self._particles_positions):   # iterate through all particles
            normal = self._particles_normals[index]   # assign a particle normal vector to a variable
            self._particles_positions[index] = [   # override previous particle position with a new position
                particle[0]+normal[0]*.1,
                particle[1]+normal[1]*.1,
                particle[2]+normal[2]*.1
            ]

    def _compute_new_particle_normal_and_reduce_energy(self, axis, index):
        '''
        A method to compute new particle normals and reduce its energy level after reflection.
        :param axis: either 'x', 'y' or 'z' based on which axis does the particle reflects
        :param index: index of particle in all global lists
        '''
        normal = self._particles_normals[index]   # assign a particle normal vector to a variable
        if axis == 'x':
            self._particles_normals[index] = ([-normal[0], normal[1], normal[2]])   # reflecting the particle
        elif axis == 'y':
            self._particles_normals[index] = ([normal[0], -normal[1], normal[2]])   # reflecting the particle
        else:
            self._particles_normals[index] = ([normal[0], normal[1], -normal[2]])   # reflecting the particle
        # reducing particle energy
        self._particles_energies[index] = 10 * log10(10 ** (self._particles_energies[index] * .1) * (1 - self._room.average_alpha[self._source_freq]))
        if self._particles_energies[index] < self._source_spl - 60:
            self._particles_to_delete.append(index)   # queueing the particle to removal when its energy is below 60dB
