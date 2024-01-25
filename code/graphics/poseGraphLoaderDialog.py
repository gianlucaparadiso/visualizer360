import logging
from PyQt5 import QtWidgets, QtCore
from signals.sigString import SigString


""" Class representing the 3D plot widget and its content """
class PoseGraphLoaderDialog(QtWidgets.QFileDialog):
    filename_signal = QtCore.pyqtSignal(SigString)

    def __init__(self):
        super().__init__()

        # Logger setup
        self.logger = logging.getLogger()

        self.logger.info("Creating PoseGraphLoaderDialog...")
        self.setFileMode(QtWidgets.QFileDialog.ExistingFile)
        self.setNameFilter("G2O files (*.g2o)")
        self.setViewMode(QtWidgets.QFileDialog.Detail)
        self.logger.info("Finished creating PoseGraphLoaderDialog")

    def loadg2oFile(self):
        self.logger.info("Selecting g2o file...")
        if self.exec_():
            filenames = self.selectedFiles()
            if filenames:
                self.logger.info("Selected g2o file...")
                self.filename_signal.emit(SigString(filenames[0]))
            else:
                self.logger.info("No selected g2o file")
