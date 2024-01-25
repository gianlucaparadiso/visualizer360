import logging
from PyQt5 import QtWidgets

"""''' Class representing the handler object used for logging """
class QTextEditLogger(logging.Handler):
    def __init__(self, parent):
        super().__init__()
        self.widget = QtWidgets.QPlainTextEdit(parent)
        self.widget.setReadOnly(True)
        self.setLevel(logging.INFO)

    def emit(self, record):
        msg = self.format(record)
        self.widget.appendPlainText(msg)
