#!/usr/bin/python3.4

'''
Error handler module for Ray Tracing Method 4-dimensional visualization.
'''

from PyQt5.QtWidgets import QMessageBox

__author__ = 'Norbert Mieczkowski'
__copyright__ = 'Copyright 2015, Norbert Mieczkowski'
__version__ = '1.0.0'


class ErrorHandler():

    def raise_dialog(self, text):
        '''
        Raises critical error dialog box with an exception description.
        :param text: string printed in the dialog message window
        '''
        dialog = QMessageBox()
        dialog.setWindowTitle('Error')
        dialog.setIcon(QMessageBox.Critical)
        dialog.setText(text)
        dialog.setStandardButtons(QMessageBox.Close)
        dialog.setFixedSize(dialog.width(), dialog.height())
        dialog.exec()
