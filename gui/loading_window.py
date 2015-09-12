#!/usr/bin/python3.4

'''
Files loading window module for Ray Tracing Method 4-dimensional visualization.
'''

from PyQt5.QtWidgets import QFileDialog, QLabel, QLineEdit, QPushButton, QWidget
from error_handler.error_handler import ErrorHandler
from gui.visualization_window import VisualizationWindow
from input.file_loader import FileLoader

__author__ = 'Norbert Mieczkowski'
__copyright__ = 'Copyright 2015, Norbert Mieczkowski'
__version__ = '1.0.0'


class LoadingWindow(QWidget):

    def __init__(self, application):
        '''
        Class defining files loading window.
        :param application: parent application
        '''
        super().__init__()

        # assigning application as a class attribute just in case, e.g. for getting screen size
        self._application = application

        # initializing error handler in case of exceptions
        self._error_handler = ErrorHandler()

        # specifying window size
        self._width = 410
        self._height = 220

        # setting window parameters such as size, position and title
        screen_center = self._application.desktop().screen().rect().center()
        self.setGeometry(screen_center.x() - self._width * .5,
                         screen_center.y() - self._height * .5,
                         self._width,
                         self._height)
        self.setWindowTitle('Ray Tracing Method 4-dimensional visualization')
        self.setFixedSize(self._width, self._height)

        # creating master file browse label
        self._master_file_browse_lbl = QLabel('Input file:', self)
        self._master_file_browse_lbl.move(22, 20)

        # creating master file path text field
        self._master_file_path_text_field = QLineEdit(self)
        self._master_file_path_text_field.setFixedWidth(300)
        self._master_file_path_text_field.move(20, 40)

        # creating master file browsing button
        self._master_file_browse_btn = QPushButton('Browse...', self)
        self._master_file_browse_btn.setFixedWidth(70)
        self._master_file_browse_btn.move(20 + self._master_file_path_text_field.width(), 40)
        self._master_file_browse_btn.clicked[bool].connect(self._select_master_file)

        # creating load button
        self._load_btn = QPushButton('Load file', self)
        self._load_btn.setFixedWidth(self._master_file_path_text_field.width() + self._master_file_browse_btn.width())
        self._load_btn.setFixedHeight(60)
        self._load_btn.move((self._width - self._load_btn.width()) * .5, 90)
        self._load_btn.clicked[bool].connect(self._load_files)

        # creating close button
        self._close_btn = QPushButton('Close', self)
        self._close_btn.setFixedWidth(70)
        self._close_btn.move((self._width - self._close_btn.width()) * .5,
                             self._height - self._close_btn.height() - 20)
        self._close_btn.clicked[bool].connect(self.close)

        self.show()

    def _browse_files(self):
        '''
        Pops file dialog window up.
        :returns: path to selected file
        '''
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        return file_dialog.getOpenFileName()[0]

    def _select_master_file(self):
        '''
        Calls _browse_files method and assigns selected file to _master_file_path_text_field text.
        '''
        self._master_file_path_text_field.setText(self._browse_files())

    def _load_files(self):
        '''
        Creates FileLoader instance and loads files specified in text fields.
        '''
        file_loader = FileLoader()
        try:
            room_geometry = file_loader.load_master_file(self._master_file_path_text_field.text())
            self.close()
            self.visualization_window = VisualizationWindow(self._application, room_geometry)
        except Exception as e:
            self._error_handler.raise_dialog(str(e))
