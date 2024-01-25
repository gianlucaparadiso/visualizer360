import logging
from functools import partial
from PyQt5 import QtWidgets, QtCore, QtGui
from signals.sigString import SigString
from signals.sigStringList import SigStringList


""" Class representing the point cloud loading widget """
class PointCloudsLoaderDialog(QtWidgets.QMainWindow):
    closed = QtCore.pyqtSignal()
    multi_pc_signal = QtCore.pyqtSignal(SigStringList)
    two_folders_signal = QtCore.pyqtSignal(SigStringList)
    folder_pc_signal = QtCore.pyqtSignal(SigString)

    def __init__(self):
        super(PointCloudsLoaderDialog, self).__init__()

        # Logger setup
        self.logger = logging.getLogger("logger")

        self.logger.info("Creating PointCloudsLoaderDialog...")
        self.initUI(QtCore.QSize(600, 300))
        self.logger.info("Finished creating ImagesLoaderDialog")

    def initUI(self, size: QtCore.QSize):
        # Window setup
        self.setWindowTitle("Images loader mode selection")
        self.resize(size.width(), size.height())

        # Set central area
        self.central_widget = QtWidgets.QFrame()
        self.setCentralWidget(self.central_widget)

        # Set widget areas
        self.setLeftWidgetArea()
        self.setCentreWidgetArea()
        self.setRightWidgetArea()

        # Panels composition
        self.outer_layout = QtWidgets.QHBoxLayout()
        self.outer_layout.addWidget(self.left_panel)
        self.outer_layout.addWidget(self.centre_panel)
        self.outer_layout.addWidget(self.right_panel)
        self.central_widget.setLayout(self.outer_layout)

        # Multiple images loader
        self.multi_point_clouds_loader = MultiPointCloudsLoader()
        self.multi_point_clouds_loader.closed.connect(partial(self.setDisabled, False))
        self.multi_point_clouds_loader.confirmed.connect(partial(self.close))
        self.multi_point_clouds_loader.multi_pc_name_signal.connect(self.emitFilenamesSignal)

        # Two folders images loader
        self.two_folders_point_clouds_loader = TwoFoldersPointCloudsLoader()
        self.two_folders_point_clouds_loader.closed.connect(partial(self.setDisabled, False))
        self.two_folders_point_clouds_loader.confirmed.connect(partial(self.close))
        self.two_folders_point_clouds_loader.two_folders_pc_name_signal.connect(self.emitFoldersSignal)

    """ Initialise the left widget area, for multiple files loading """
    def setLeftWidgetArea(self):
        self.logger.info("Initialising left widget area...")

        # Set the main panel and layout
        self.left_panel = QtWidgets.QFrame()
        self.left_layout = QtWidgets.QVBoxLayout()
        left_sp = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        left_sp.setHorizontalStretch(1)
        self.left_panel.setSizePolicy(left_sp)

        # Set the upper area to load a file dialog with a button
        left_up = QtWidgets.QPushButton("", self)
        left_up.setToolTip('Multiple selection')
        left_up.setIcon(QtGui.QIcon("./icons/files.png"))
        left_up.setIconSize(QtCore.QSize(90, 90))
        left_up.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        left_up.clicked.connect(self.showMultiPointCloudsLoader)

        # Set the bottom area to describe the action with a label
        left_down = QtWidgets.QLabel("Add multiple point clouds, one by one. A single entry requires a point cloud "
                                     "file and a data file containing the correspondences with the pose graph.", self)
        left_down.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        left_down.setAlignment(QtCore.Qt.AlignCenter)
        left_down.setWordWrap(True)

        # Add the areas to the main panel
        self.left_layout.addWidget(left_up)
        self.left_layout.addWidget(left_down)
        self.left_panel.setLayout(self.left_layout)

        self.logger.info("Finished initialising left widget area")

    """ Initialise the centre widget area, for two folders loading """
    def setCentreWidgetArea(self):
        self.logger.info("Initialising centre widget area...")

        # Set the main panel and layout
        self.centre_panel = QtWidgets.QFrame()
        self.centre_layout = QtWidgets.QVBoxLayout()
        centre_sp = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        centre_sp.setHorizontalStretch(1)
        self.centre_panel.setSizePolicy(centre_sp)

        # Set the upper area to load a file dialog with a button
        centre_up = QtWidgets.QPushButton("", self)
        centre_up.setToolTip('Folders selection')
        centre_up.setIcon(QtGui.QIcon("./icons/folders.png"))
        centre_up.setIconSize(QtCore.QSize(90, 90))
        centre_up.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        centre_up.clicked.connect(self.showTwoFoldersPointCloudsLoader)

        # Set the bottom area to describe the action with a label
        centre_down = QtWidgets.QLabel("Add multiple point clouds together. It requires the directory containing the "
                                       "point clouds and the directory containing the data files.", self)
        centre_down.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        centre_down.setAlignment(QtCore.Qt.AlignCenter)
        centre_down.setWordWrap(True)

        # Add the areas to the main panel
        self.centre_layout.addWidget(centre_up)
        self.centre_layout.addWidget(centre_down)
        self.centre_panel.setLayout(self.centre_layout)

        self.logger.info("Finished initialising centre widget area")

    """ Initialise the right widget area, for single folder loading """
    def setRightWidgetArea(self):
        self.logger.info("Initialising centre widget area...")

        # Set the main panel and layout
        self.right_panel = QtWidgets.QFrame()
        self.right_layout = QtWidgets.QVBoxLayout()
        right_sp = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        right_sp.setHorizontalStretch(1)
        self.right_panel.setSizePolicy(right_sp)

        # Set the upper area to load a file dialog with a button
        right_up = QtWidgets.QPushButton("", self)
        right_up.setToolTip('Folder selection')
        right_up.setIcon(QtGui.QIcon("./icons/folder.png"))
        right_up.setIconSize(QtCore.QSize(90, 90))
        right_up.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        right_up.clicked.connect(self.readDirectoryPath)

        # Set the bottom area to describe the action with a label
        right_down = QtWidgets.QLabel("Add multiple point clouds together. It requires the directory containing the "
                                      "point clouds. They will be associated to the pose graph by ordering.", self)
        right_down.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        right_down.setAlignment(QtCore.Qt.AlignCenter)
        right_down.setWordWrap(True)

        # Add the areas to the main panel
        self.right_layout.addWidget(right_up)
        self.right_layout.addWidget(right_down)
        self.right_panel.setLayout(self.right_layout)

        self.logger.info("Finished initialising right widget area")

    def closeEvent(self, event):
        self.multi_point_clouds_loader.reset()
        self.multi_point_clouds_loader.close()
        self.two_folders_point_clouds_loader.reset()
        self.two_folders_point_clouds_loader.close()
        self.closed.emit()

    def showMultiPointCloudsLoader(self):
        self.multi_point_clouds_loader.show()
        self.multi_point_clouds_loader.activateWindow()
        self.multi_point_clouds_loader.raise_()
        self.setDisabled(True)

    def showTwoFoldersPointCloudsLoader(self):
        self.two_folders_point_clouds_loader.show()
        self.two_folders_point_clouds_loader.activateWindow()
        self.multi_point_clouds_loader.raise_()
        self.setDisabled(True)

    def readDirectoryPath(self):
        directory = str(QtWidgets.QFileDialog.getExistingDirectory())
        if directory != "":
            self.folder_pc_signal.emit(SigString(directory))
            self.close()

    # --------------------------------------------------------------
    # -------------------------- EMITTERS --------------------------
    # --------------------------------------------------------------
    @QtCore.pyqtSlot(SigStringList)
    def emitFilenamesSignal(self, files_filenames: SigStringList):
        self.multi_pc_signal.emit(files_filenames)

    @QtCore.pyqtSlot(SigStringList)
    def emitFoldersSignal(self, folders_filepaths: SigStringList):
        self.two_folders_signal.emit(folders_filepaths)


""" Class representing the multiple file selection widget """
class MultiPointCloudsLoader(QtWidgets.QMainWindow):
    closed = QtCore.pyqtSignal()
    confirmed = QtCore.pyqtSignal()
    multi_pc_name_signal = QtCore.pyqtSignal(SigStringList)

    def __init__(self):
        super(MultiPointCloudsLoader, self).__init__()
        self.initUI(QtCore.QSize(720, 300))

    def initUI(self, size: QtCore.QSize):

        # Setup window
        self.setWindowTitle("Multiple Point Clouds Reader")
        self.resize(size.width(), size.height())

        # ------ Selection area -------
        self.selection_area = QtWidgets.QWidget()
        self.selection_area_layout = QtWidgets.QHBoxLayout()
        self.selection_area.setLayout(self.selection_area_layout)

        # Buttons
        self.add_button = QtWidgets.QPushButton('Add entry')
        self.add_button.clicked.connect(self.addEntry)

        self.remove_button = QtWidgets.QPushButton('Remove entry')
        self.remove_button.clicked.connect(self.removeEntry)

        self.confirm_button = QtWidgets.QPushButton('OK')
        self.confirm_button.clicked.connect(self.confirmSelection)

        # Buttons composition
        self.selection_area_layout.addWidget(self.add_button)
        self.selection_area_layout.addWidget(self.remove_button)
        self.selection_area_layout.addWidget(self.confirm_button)

        # ------ Scroll area -------
        self.scroll_widget = QtWidgets.QWidget()
        self.scroll_layout = QtWidgets.QFormLayout()
        self.scroll_widget.setLayout(self.scroll_layout)
        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.scroll_widget)

        # ------ Items composition -------
        self.main_layout = QtWidgets.QVBoxLayout()

        self.main_layout.addWidget(self.selection_area)
        self.main_layout.addWidget(self.scroll_area)

        self.central_widget = QtWidgets.QWidget()
        self.central_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.central_widget)

    '''Add an entry to the scroll area of the class'''
    def addEntry(self):
        layout = QtWidgets.QGridLayout()

        # Construction of the point cloud filepath entry
        pc_label = QtWidgets.QLabel("Point cloud filepath:")
        pc_entry = ReaderEntry(0, False)
        layout.addWidget(pc_label, 0, 0, 1, 1)
        layout.addWidget(pc_entry, 0, 1, 1, 1)

        # Construction of the data filepath entry
        data_label = QtWidgets.QLabel("Data filepath:")
        data_entry = ReaderEntry(1, False)
        layout.addWidget(data_label, 1, 0, 1, 1)
        layout.addWidget(data_entry, 1, 1, 1, 1)

        # Entries composition
        entry = QtWidgets.QGroupBox()
        entry.setLayout(layout)
        self.scroll_layout.addRow(entry)

        self.logger.info("Added new point clouds loader entry")

    '''Remove an entry to the scroll area of the class'''
    def removeEntry(self):
        self.scroll_layout.removeRow(self.scroll_layout.rowCount() - 1)

        self.logger.info("Removed last image loader entry")

    '''Confirm the selections in the scroll area of the class'''
    def confirmSelection(self):
        filenames = list()

        # Gather all data from the multiple entries
        for i in range(0, self.scroll_layout.rowCount()):
            row: QtWidgets.QWidgetItem = self.scroll_layout.itemAt(i)
            children = row.widget().children()

            pc_path = ""
            data_path = ""

            for child in children:
                if type(child) == ReaderEntry:
                    if child.tag == 0:
                        pc_path = child.path_text.text()
                    else:
                        data_path = child.path_text.text()

            if pc_path != "" and data_path != "":
                filenames.append([pc_path, data_path])

        while self.scroll_layout.rowCount():
            self.removeEntry()

        self.reset()
        self.close()

        if filenames:
            self.multi_pc_name_signal.emit(SigStringList(filenames))
            self.confirmed.emit()

    def reset(self):
        while self.scroll_layout.rowCount():
            self.removeEntry()

    def closeEvent(self, event):
        self.closed.emit()

""" Class representing the two folders selection widget """
class TwoFoldersPointCloudsLoader(QtWidgets.QMainWindow):
    closed = QtCore.pyqtSignal()
    confirmed = QtCore.pyqtSignal()
    two_folders_pc_name_signal = QtCore.pyqtSignal(SigStringList)

    def __init__(self):
        super(TwoFoldersPointCloudsLoader, self).__init__()
        self.initUI(QtCore.QSize(720, 300))

    def initUI(self, size: QtCore.QSize):
        self.setWindowTitle("Multiple Point Clouds Reader")
        self.resize(size.width(), size.height())

        # ------ Selection area -------
        self.selection_area = QtWidgets.QWidget()
        self.selection_area_layout = QtWidgets.QHBoxLayout()
        self.selection_area.setLayout(self.selection_area_layout)

        # Buttons
        self.confirm_button = QtWidgets.QPushButton('OK')
        self.confirm_button.clicked.connect(self.confirmSelection)
        self.selection_area_layout.addWidget(self.confirm_button)

        # ------ Scroll area -------
        self.scroll_widget = QtWidgets.QWidget()
        self.scroll_layout = QtWidgets.QFormLayout()
        self.scroll_widget.setLayout(self.scroll_layout)
        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.scroll_widget)

        self.addEntry()

        # ------ Items composition -------
        self.main_layout = QtWidgets.QVBoxLayout()

        self.main_layout.addWidget(self.selection_area)
        self.main_layout.addWidget(self.scroll_area)

        self.central_widget = QtWidgets.QWidget()
        self.central_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.central_widget)

    '''Add an entry to the scroll area of the class'''
    def addEntry(self):
        layout = QtWidgets.QGridLayout()

        # Construction of the point cloud filepath entry
        pc_label = QtWidgets.QLabel("Point cloud folder path:")
        pc_entry = ReaderEntry(0, True)
        layout.addWidget(pc_label, 0, 0, 1, 1)
        layout.addWidget(pc_entry, 0, 1, 1, 1)

        # Construction of the data filepath entry
        data_label = QtWidgets.QLabel("Data folder path:")
        data_entry = ReaderEntry(1, True)
        layout.addWidget(data_label, 1, 0, 1, 1)
        layout.addWidget(data_entry, 1, 1, 1, 1)

        # Entries composition
        entry = QtWidgets.QGroupBox()
        entry.setLayout(layout)
        self.scroll_layout.addRow(entry)

    '''Confirm the selections in the scroll area of the class'''
    def confirmSelection(self):
        filenames = list()

        # Gather all data from the multiple entries
        row: QtWidgets.QWidgetItem = self.scroll_layout.itemAt(0)
        children = row.widget().children()

        pc_path = ""
        data_path = ""

        for child in children:
            if type(child) == ReaderEntry:
                if child.tag == 0:
                    pc_path = child.path_text.text()
                    child.path_text.clear()
                else:
                    data_path = child.path_text.text()
                    child.path_text.clear()

        if pc_path != "" and data_path != "":
            filenames.append([pc_path, data_path])

        self.reset()
        self.close()

        if filenames:
            self.two_folders_pc_name_signal.emit(SigStringList(filenames))
            self.confirmed.emit()

    def reset(self):
        row: QtWidgets.QWidgetItem = self.scroll_layout.itemAt(0)
        children = row.widget().children()

        for child in children:
            if type(child) == ReaderEntry:
                if child.tag == 0:
                    child.path_text.clear()
                else:
                    child.path_text.clear()

    def closeEvent(self, event):
        self.closed.emit()


""" Class representing the entry used in the selection widgets """
class ReaderEntry(QtWidgets.QWidget):
    def __init__(self, tag: int, mode: bool):
        super(ReaderEntry, self).__init__()

        self.tag = tag
        self.entry_layout = QtWidgets.QHBoxLayout()
        self.path_text = QtWidgets.QLineEdit()
        self.path_text.setReadOnly(True)
        self.dialog_button = QtWidgets.QToolButton()
        if mode:
            self.dialog_button.clicked.connect(self.readDirectoryPath)
        else:
            self.dialog_button.clicked.connect(partial(self.readFilePath, tag))

        self.entry_layout.addWidget(self.path_text)
        self.entry_layout.addWidget(self.dialog_button)

        self.setLayout(self.entry_layout)

    def readDirectoryPath(self):
        directory = str(QtWidgets.QFileDialog.getExistingDirectory())
        self.path_text.setText('{}'.format(directory))

    def readFilePath(self, tag: int):
        dlg = QtWidgets.QFileDialog()
        dlg.setFileMode(QtWidgets.QFileDialog.ExistingFile)
        if tag == 0:
            dlg.setNameFilter("Point Cloud Data (pcd) files (*.pcd)")
        else:
            dlg.setNameFilter("Data files (*.txt)")

        if dlg.exec_():
            filenames = dlg.selectedFiles()
            self.path_text.setText(filenames[0])
