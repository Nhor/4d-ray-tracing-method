#!/usr/bin/python3.4

'''
Main module for Ray Tracing Method 4-dimensional visualization.
'''

import sys
from PyQt5.QtWidgets import QApplication
from gui.loading_window import LoadingWindow

__author__ = 'Norbert Mieczkowski'
__copyright__ = 'Copyright 2015, Norbert Mieczkowski'
__version__ = '1.0.0'


def main():
    """
    Initializes and executes PyQt5 and PyOpenGL whole application.
    """
    application = QApplication(sys.argv)   # initializing application
    loading_window = LoadingWindow(application)   # creating application window for loading files
    sys.exit(application.exec_())   # executing application

if __name__ == '__main__':
    main()
