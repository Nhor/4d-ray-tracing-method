#!/usr/bin/python3.4

'''
Room geometry file loader module for Ray Tracing Method 4-dimensional visualization.
'''

from geometry.room import Room

__author__ = 'Norbert Mieczkowski'
__copyright__ = 'Copyright 2015, Norbert Mieczkowski'
__version__ = '1.0.0'


class FileLoader():

    def __init__(self):
        '''
        Creates empty dictionaries of values yet to read.
        '''
        self._points = {}
        self._faces = {}
        self._abs = {}

    def load_master_file(self, file_path):
        '''
        Loads file with room geometry into three lists of points, faces and abs (materials).
        :param file_path: path to file with room geometry
        '''
        with open(file_path) as master_file:   # opening specified file
            lines = master_file.readlines()   # reading each line of opened file
            for line in lines:   # iterating over the lines
                # reading points
                if line[0].isdigit():
                    self._read_point(line)
                # reading faces
                elif line.startswith('['):
                    self._read_face(line)
                # reading materials
                elif line.lower().startswith('abs'):
                    self._read_abs(line)
            master_file.close()
        return Room(self._points, self._faces, self._abs)

    def _read_point(self, text_line):
        '''
        Reads line of text and picks the point id and coordinates.
        :param text_line: string with point data
        '''
        # splitting the line into separate elements and deleting '\n' at its end
        data = [sth for sth in text_line.split(' ') if sth != '']
        if data[-1].endswith('\n'):
            data[-1] = data[-1][:-1]
        self._points[int(data[0])] = (float(data[1]), float(data[3]), float(data[2]))   # adding new point to the list

    def _read_face(self, text_line):
        '''
        Reads line of text and picks the face id, points and material.
        :param text_line: string with face data
        '''
        # splitting the line into separate elements and deleting '\n' at its end and '[' ']' if glued to data samples
        data = [sth for sth in text_line.split(' ') if sth != '']
        if data[0].startswith('['):
            data[0] = data[0][1:]
        if data[-1].endswith('\n'):
            data[-1] = data[-1][:-1]
        if data[-1].endswith(']'):
            data[-1] = data[-1][:-1]
        for i in range(len(data)):
            if data[i].startswith('/') and (data[i] != '/'):
                data[i] = data[i][1:]
                data.insert(i, '/')
        face = []   # creating empty list to fill with face information
        beginning_index = data.index('/')   # finding first '/' tag index
        data[beginning_index] = 'X'   # replacing the '/' tag with 'X' to find the second '/' tag
        ending_index = data.index('/')   # finding second '/' tag index
        for i in range(ending_index - beginning_index - 1):   # loop to iterate over each element between '/' tags
            face.append(int(data[beginning_index + i + 1]))   # appending each point between '/' tags to face list
        face.append(data[ending_index + 1])   # finally appending abs name
        self._faces[int(data[0])] = tuple(face)   # adding new face to the faces list

    def _read_abs(self, text_line):
        '''
        Reads line of text and picks the material name, sound absorption coefficient for certain frequencies and color.
        :param text_line: string with material data
        '''
        # splitting the line into separate elements and deleting '\n' at its end
        data = [sth for sth in text_line.split(' ') if sth != '']
        if data[-1].endswith('\n'):
            data[-1] = data[-1][:-1]
        # inefficient but necessary set of loops for cutting out '<', '>', '{' and '}' from data samples
        for i in range(len(data)):
            if data[i].startswith('<') and (data[i] != '<'):
                data[i] = data[i][1:]
                data.insert(i, '<')
        for i in range(len(data)):
            if (data[i].endswith('>')) and (data[i] != '>'):
                data[i] = data[i][:-1]
                data.insert(i + 1, '>')
        for i in range(len(data)):
            if data[i].startswith('{') and (data[i] != '{'):
                data[i] = data[i][1:]
                data.insert(i, '{')
        for i in range(len(data)):
            if (data[i].endswith('}')) and (data[i] != '}'):
                data[i] = data[i][:-1]
                data.insert(i + 1, '}')
        abs = []   # creating empty list to fill with material information
        beginning_index = data.index('<')   # finding '<' tag index
        ending_index = data.index('>')   # finding '>' tag index
        for i in range(ending_index - beginning_index - 1):   # loop to iterate over each element between '<' '>' tags
            abs.append(int(data[beginning_index + i + 1]) / 100)   # appending each coefficient between '<' '>' tags
        try:   # material color is optional so exception handler is called
            beginning_index = data.index('{')   # finding '}' tag index
            ending_index = data.index('}')   # finding '{' tag index
            for i in range(ending_index - beginning_index - 1):   # loop to iterate over elements between '{' '}' tags
                abs.append(int(data[beginning_index + i + 1]) / 255)   # appending each rgb value between '{' '}' tags
        except ValueError:   # if material color wasn't specified
            abs.extend((150 / 255, 150 / 255, 157 / 255))   # setting material color to default
        self._abs[data[1]] = tuple(abs)   # adding new abs to the abs list
