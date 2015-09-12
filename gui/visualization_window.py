#!/usr/bin/python3.4

'''
Main window and basic GUI widgets module for Ray Tracing Method 4-dimensional visualization.
'''

from PyQt5.QtWidgets import QComboBox, QLabel, QLineEdit, QPushButton, QWidget
from error_handler.error_handler import ErrorHandler
from gui.opengl_widget import OpenGLWidget

__author__ = 'Norbert Mieczkowski'
__copyright__ = 'Copyright 2015, Norbert Mieczkowski'
__version__ = '1.0.0'


class VisualizationWindow(QWidget):

    def __init__(self, application, room, *args, **kwargs):
        '''
        Class defining main window and basic GUI widgets.
        :param application: parent application
        :param room: Room() instance, which is loaded and parsed input file
        '''
        super(VisualizationWindow, self).__init__(*args, **kwargs)

        # initializing error handler in case of exceptions
        self._error_handler = ErrorHandler()

        # assigning application as a class attribute just in case, e.g. for getting screen size
        self._application = application

        # assigning room as a class attribute for easier argument passing
        self.room = room

        # specifying window size
        self._width = 1280
        self._height = 720

        # setting window parameters such as size, position and title
        screen_center = self._application.desktop().screen().rect().center()
        self.setGeometry(screen_center.x() - self._width * .5,
                         screen_center.y() - self._height * .5,
                         self._width,
                         self._height)
        self.setWindowTitle('Ray Tracing Method 4-dimensional visualization')
        self.setFixedSize(self._width, self._height)

        # creating OpenGL widget area
        self._opengl_widget = OpenGLWidget(self)

        # creating source parameters label
        self._source_parameters_lbl = QLabel('Source parameters:', self)
        self._source_parameters_lbl.move(22, 20)

        # creating source coordinates labels and text fields
        self._source_x_lbl = QLabel('X:', self)
        self._source_x_lbl.move(22, 50)
        self._source_x_text = QLineEdit(self)
        self._source_x_text.setFixedWidth(57)
        self._source_x_text.move(40, 46)

        self._source_y_lbl = QLabel('Y:', self)
        self._source_y_lbl.move(112, 50)
        self._source_y_text = QLineEdit(self)
        self._source_y_text.setFixedWidth(57)
        self._source_y_text.move(130, 46)

        self._source_z_lbl = QLabel('Z:', self)
        self._source_z_lbl.move(202, 50)
        self._source_z_text = QLineEdit(self)
        self._source_z_text.setFixedWidth(57)
        self._source_z_text.move(220, 46)

        # creating source SPL label and text field
        self._source_spl_lbl = QLabel('SPL [dB]:', self)
        self._source_spl_lbl.move(22, 80)
        self._source_spl_text = QLineEdit(self)
        self._source_spl_text.setFixedWidth(190)
        self._source_spl_text.move(87, 76)

        # creating source frequency label and dropdown list
        self._source_freq_lbl = QLabel('Frequency [Hz]:', self)
        self._source_freq_lbl.move(22, 110)
        self._source_freq_dropdown = QComboBox(self)
        self._source_freq_dropdown.addItems(['125', '250', '500', '1000', '2000', '4000'])
        self._source_freq_dropdown.setFixedWidth(146)
        self._source_freq_dropdown.move(131, 106)

        # creating simulation button
        self._simulation_button = QPushButton('Start simulation', self)
        self._simulation_button.setFixedSize(257, 60)
        self._simulation_button.move(20, 160)
        self._simulation_button.clicked[bool].connect(self._start_simulation)

        self.show()

    def _start_simulation(self):
        '''
        Method disabling all Qt widgets and starting OpenGL animation.
        '''
        try:   # exception handling in case of wrong input values
            source_pos = (   # source position tuple
                float(self._source_x_text.text()),   # source position x
                float(self._source_z_text.text()),   # source position y
                float(self._source_y_text.text())    # source position z
            )
            source_spl = float(self._source_spl_text.text()),   # source sound pressure level
            source_spl = source_spl[0] if type(source_spl) == type(tuple()) else source_spl
            source_freq = int(self._source_freq_dropdown.currentText())   # source frequency
        except Exception as e:   # in case of exception
            self._error_handler.raise_dialog(str(e))   # raise dialog window with exception description
            return   # and return to prevent function from proceeding

        # disabling all widgets
        self._source_parameters_lbl.setDisabled(True)
        self._source_x_lbl.setDisabled(True)
        self._source_x_text.setDisabled(True)
        self._source_y_lbl.setDisabled(True)
        self._source_y_text.setDisabled(True)
        self._source_z_lbl.setDisabled(True)
        self._source_z_text.setDisabled(True)
        self._source_spl_lbl.setDisabled(True)
        self._source_spl_text.setDisabled(True)
        self._source_freq_lbl.setDisabled(True)
        self._source_freq_dropdown.setDisabled(True)
        self._simulation_button.setDisabled(True)

        # initializing OpenGL animation
        self._opengl_widget.initialize_animation(source_pos=source_pos, source_spl=source_spl, source_freq=source_freq)
