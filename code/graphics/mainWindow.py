import math
from collections import OrderedDict

from PyQt5.QtWidgets import QMainWindow, QDockWidget
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from graphics.graphicArea import GraphicArea
from graphics.poseGraphLoaderDialog import PoseGraphLoaderDialog
from graphics.pointCloudsLoaderDialog import PointCloudsLoaderDialog
from graphics.imagesLoaderDialog import ImagesLoaderDialog
from graphics.poseInfoForm import PoseInfoForm

# Add include for imgs 360 loader dialog
from graphics.images360LoaderDialog import Images360LoaderDialog

from signals.sigString import SigString
from signals.sigStringList import SigStringList
from signals.sigPosition import SigPosition
from functools import partial

import logging


class MainWindow(QMainWindow):
    pg_filename_signal = QtCore.pyqtSignal(SigString)

    multi_pcs_signal = QtCore.pyqtSignal(SigStringList)
    two_folders_pcs_signal = QtCore.pyqtSignal(SigStringList)
    single_folder_pcs_signal = QtCore.pyqtSignal(SigString)

    multi_imgs_signal = QtCore.pyqtSignal(SigStringList)
    two_folders_imgs_signal = QtCore.pyqtSignal(SigStringList)
    single_folder_imgs_signal = QtCore.pyqtSignal(SigString)

    # Add 360 imags signals
    multi_imgs360_signal = QtCore.pyqtSignal(SigStringList)
    two_folders_imgs360_signal = QtCore.pyqtSignal(SigStringList)
    single_folder_imgs360_signal = QtCore.pyqtSignal(SigString)

    clean_pose_graph_signal = QtCore.pyqtSignal()
    clean_point_clouds_signal = QtCore.pyqtSignal()
    clean_images_signal = QtCore.pyqtSignal()
    
    # Add cleaning signal for 360 imgs
    clean_images360_signal = QtCore.pyqtSignal()

    selected_pose_signal = QtCore.pyqtSignal(int)

    def __init__(self, size: QtCore.QSize):
        super(MainWindow, self).__init__()

        # Logger setup
        self.logger_handle = QTextEditLogger(self)
        self.logger_handle.setFormatter(logging.Formatter('%(levelname)s : %(module)s : %(funcName)s : %(lineno)d : %(message)s'))
        self.logger = logging.getLogger()
        self.logger.addHandler(self.logger_handle)
        self.logger.info("Creating MainWindow...")

        self.initUI(size)

    def initUI(self, size: QtCore.QSize):

        self.block = False

        # Window setup
        self.initialiseWindow(size)

        # Set toolbars
        self.initialiseLoadToolbar()
        self.initialiseColouringToolbar()
        self.initialiseCleaningToolbar()
        self.initialiseShowHideToolbar()
        self.initialiseInteractionsToolbar()

        self.createInteractionInfoPanel()

        # Set the central widget, which contains the graph and points 2D and 3D viewers
        self.initialiseGraphicArea()

        # Initialise the file loaders, without showing them
        self.initialiseFileLoaderDialogs()

        # Connect toolbars and loaders
        self.load_pg_action.triggered.connect(self.loadPG)
        self.load_pcs_action.triggered.connect(self.loadPCS)
        self.load_images_action.triggered.connect(self.loadIMGS)

        # Add load action fro 360 images
        self.load_images360_action.triggered.connect(self.loadIMGS360)

        self.toggle_colour_action.triggered.connect(self.togglePCsColour)
        self.set_journey_mode_action.triggered.connect(self.toggleJourneyMode)

        self.clean_pose_graph_action.triggered.connect(self.cleanPoseGraph)
        self.clean_point_clouds_action.triggered.connect(self.cleanPointClouds)
        self.clean_images_action.triggered.connect(self.cleanImages)

        # Adding cleaning action for 360 images
        self.clean_images360_action.triggered.connect(self.cleanImages360)

        self.showhide_info_action.triggered.connect(self.showhideInfoPanel)
        self.showhide_log_action.triggered.connect(self.showhideLogPanel)
        self.showhide_sliders_action.triggered.connect(self.showhideSlidersPanel)

        self.interactions_action.triggered.connect(self.interaction_widget.show)

        # Add log docker (bottom)
        self.log_dock = QDockWidget("LOG")
        self.log_dock.setWidget(self.logger_handle.widget)
        self.addDockWidget(QtCore.Qt.BottomDockWidgetArea, self.log_dock)

        # Add info docker (left)
        self.info_form = PoseInfoForm()
        self.info_dock = QDockWidget("Pose info")
        self.info_dock.setWidget(self.info_form)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.info_dock)

        # Add 3D sliders
        self.initialiseSliders()
        self.sliders_dock = QDockWidget("Sliders")
        self.sliders_dock.setWidget(self.sliders_frame)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.sliders_dock)

        # Data
        self.has_graph = False
        self.has_clouds = False
        self.has_images = False
        self.has_images360 = False

    def mooo(self, opend: QtWidgets.QAction):
        self.loadingBar.setStyleSheet(
            "QToolButton::hover#opend { background-color: rgba(100, 200, 250, 0.3); border-style: inset; border-width: 0px; border-radius: 5px; }")

    def nameAction(self, bar: QtWidgets.QToolBar, action: QtWidgets.QAction, name: str):
        action.setObjectName(name)
        bar.widgetForAction(action).setObjectName(action.objectName())

    # --------------------------------------------------------------
    # --------------------- UI CREATION METHODS --------------------
    # --------------------------------------------------------------
    """ Initialise main window """
    def initialiseWindow(self, size: QtCore.QSize):
        self.logger.info("Initialising window...")
        self.setWindowTitle("SLAM pose graph visualiser")
        self.resize(size.width(), size.height())
        self.logger.info("Finished initialising window")

    """ Initialise load toolbar """
    def initialiseLoadToolbar(self):
        self.logger.info("Initialising load toolbar...")

        self.loading_bar = QtWidgets.QToolBar("Loading Toolbar")

        self.load_pg_action = QtWidgets.QAction(QtGui.QIcon("./icons/pg.png"), "Load pose graph", self)
        self.loading_bar.addAction(self.load_pg_action)

        self.load_pcs_action = QtWidgets.QAction(QtGui.QIcon("./icons/pc.png"), "Load point clouds", self)
        self.loading_bar.addAction(self.load_pcs_action)
        self.load_pcs_action.setDisabled(True)

        self.load_images_action = QtWidgets.QAction(QtGui.QIcon("./icons/image.png"), "Load images", self)
        self.loading_bar.addAction(self.load_images_action)
        self.load_images_action.setDisabled(True)

        # Adding 360 images loading bar
        self.load_images360_action = QtWidgets.QAction(QtGui.QIcon("./icons/image360.png"), "Load 360 images", self)
        self.loading_bar.addAction(self.load_images360_action)
        self.load_images360_action.setDisabled(True)

        self.addToolBar(QtCore.Qt.TopToolBarArea, self.loading_bar)

        self.logger.info("Finished initialising load toolbar")

    """ Initialise colouring toolbar """
    def initialiseColouringToolbar(self):
        self.logger.info("Initialising colouring toolbar...")

        self.colouring_bar = QtWidgets.QToolBar("Colouring Toolbar")

        self.toggle_colour_action = QtWidgets.QAction(QtGui.QIcon("./icons/pc_toggle_colour.png"), "Enable/disable colored map", self)
        self.colouring_bar.addAction(self.toggle_colour_action)
        self.toggle_colour_action.setDisabled(True)

        self.set_journey_mode_action = QtWidgets.QAction(QtGui.QIcon("./icons/journey_on.png"), "Enable/disable journey mode", self)
        self.colouring_bar.addAction(self.set_journey_mode_action)
        self.set_journey_mode_action.setDisabled(True)

        self.addToolBar(QtCore.Qt.TopToolBarArea, self.colouring_bar)

        self.logger.info("Finished initialising colouring toolbar")

    """ Initialise cleaning toolbar """
    def initialiseCleaningToolbar(self):
        self.logger.info("Initialising cleaning toolbar...")

        self.cleaning_bar = QtWidgets.QToolBar("Cleaning Toolbar")

        self.clean_pose_graph_action = QtWidgets.QAction(QtGui.QIcon("./icons/pg_dump.png"),
                                                      "Remove pose graph", self)
        self.cleaning_bar.addAction(self.clean_pose_graph_action)
        self.clean_pose_graph_action.setDisabled(True)

        self.clean_point_clouds_action = QtWidgets.QAction(QtGui.QIcon("./icons/pc_dump.png"),
                                                         "Remove point clouds", self)
        self.cleaning_bar.addAction(self.clean_point_clouds_action)
        self.clean_point_clouds_action.setDisabled(True)

        self.clean_images_action = QtWidgets.QAction(QtGui.QIcon("./icons/image_dump.jpeg"),
                                                         "Remove images", self)
        self.cleaning_bar.addAction(self.clean_images_action)
        self.clean_images_action.setDisabled(True)

        # Add cleaning for 360 images
        self.clean_images360_action = QtWidgets.QAction(QtGui.QIcon("./icons/image360_dump.png"),
                                                         "Remove 360 images", self)
        self.cleaning_bar.addAction(self.clean_images360_action)
        self.clean_images360_action.setDisabled(True)

        self.addToolBar(QtCore.Qt.TopToolBarArea, self.cleaning_bar)

        self.logger.info("Finished initialising cleaning toolbar")

    """ Initialise show/hide toolbar """
    def initialiseShowHideToolbar(self):
        self.logger.info("Initialising show/hide toolbar...")

        self.showhide_bar = QtWidgets.QToolBar("Show/hide Toolbar")

        self.showhide_info_action = QtWidgets.QAction(QtGui.QIcon("./icons/show_info.png"),
                                                         "Show/hide info panel", self)
        self.showhide_bar.addAction(self.showhide_info_action)

        self.showhide_sliders_action = QtWidgets.QAction(QtGui.QIcon("./icons/show_sliders.png"),
                                                           "Show/hide sliders panel", self)
        self.showhide_bar.addAction(self.showhide_sliders_action)

        self.showhide_log_action = QtWidgets.QAction(QtGui.QIcon("./icons/show_log.png"),
                                                     "Show/hide log panel", self)
        self.showhide_bar.addAction(self.showhide_log_action)

        self.addToolBar(QtCore.Qt.TopToolBarArea, self.showhide_bar)

        self.logger.info("Finished initialising show/hide toolbar")

    """ Initialise interactions toolbar """
    def initialiseInteractionsToolbar(self):
        self.logger.info("Initialising interactions toolbar...")

        self.interactions_bar = QtWidgets.QToolBar("Interaction Toolbar")
        self.interactions_action = QtWidgets.QAction(QtGui.QIcon("./icons/info.png"),
                                                      "Mouse and keyboard interactions", self)
        self.interactions_bar.addAction(self.interactions_action)
        self.addToolBar(QtCore.Qt.TopToolBarArea, self.interactions_bar)

        self.logger.info("Finished initialising interactions toolbar")

    def createInteractionInfoPanel(self):
        #self.interaction_window = QtWidgets.QMainWindow()
        self.interaction_widget = QtWidgets.QTextEdit()
        self.interaction_widget.setDisabled(True)

        self.interaction_widget.setFixedSize(400, 300)

        self.interaction_widget.append("2D PLOT:")
        self.interaction_widget.append(" - Mouse left drag: pan the plot")
        self.interaction_widget.append(" - Wheel scrolling: zoom the plot")
        self.interaction_widget.append(" - Right arrow key (after pose selection): move to next pose")
        self.interaction_widget.append(" - Left arrow key (after pose selection): move to previous pose")
        self.interaction_widget.append("\n")
        self.interaction_widget.append("IMAGE VIEWER:")
        self.interaction_widget.append(" - Mouse left drag: pan the image")
        self.interaction_widget.append(" - Mouse double right click: reset the zoom")
        self.interaction_widget.append(" - Plus (+) key: zoom the plot by 25%")
        self.interaction_widget.append(" - Minus (-) key: zoom the plot by -25%")
        self.interaction_widget.append("\n")
        self.interaction_widget.append("3D PLOT:")
        self.interaction_widget.append(" - Mouse left drag: rotate the plot")
        self.interaction_widget.append(" - Ctrl (or cmd for Mac users) + mouse left drag: pan the plot")
        self.interaction_widget.append(" - Wheel scrolling: zoom the plot")

        #self.interaction_window.layout().addWidget(self.interaction_widget)

    """ Initialise menu bars """
    def initialiseMenuBar(self):
        self.menu_bar = self.menuBar()

        self.file = self.menu_bar.addMenu("File")
        self.file.addAction("New")
        self.file.addAction("Save")
        self.file.addAction("Quit")

        self.view = self.menu_bar.addMenu("View")

    """ Initialise graphic area """
    def initialiseGraphicArea(self):
        self.logger.info("Initialising graphic area...")

        self.central_frame = QtWidgets.QFrame()
        self.graphic_layout = QtWidgets.QVBoxLayout()
        self.graphic_area = GraphicArea()

        self.graphic_layout.addWidget(self.graphic_area)
        self.central_frame.setLayout(self.graphic_layout)
        self.setCentralWidget(self.central_frame)

        self.graphic_area.selected_pose_signal.connect(self.emitSelectedPoseSignal)
        self.graphic_area.unselected_pose_signal.connect(self.unselectPose)
        self.graphic_area.camera_position_signal.connect(self.changeSlidersValues)

        self.logger.info("Finished initialising graphic area...")

    """ Initialise file loader dialogs """
    def initialiseFileLoaderDialogs(self):
        self.logger.info("Initialising pose graph loader dialog...")
        self.pose_graph_loader_dialog = PoseGraphLoaderDialog()
        filename_signal = self.pose_graph_loader_dialog.filename_signal
        filename_signal.connect(self.emitFilenameSignal)
        self.logger.info("Finished initialising pose graph loader dialog...")

        self.logger.info("Initialising point clouds loader dialog...")
        self.point_clouds_loader_dialog = PointCloudsLoaderDialog()
        pcld_closed_signal = self.point_clouds_loader_dialog.closed
        pcld_closed_signal.connect(partial(self.setDisabled, False))
        signal_multi = self.point_clouds_loader_dialog.multi_pc_signal
        signal_multi.connect(self.emitFilenamesSignal)
        signal_two = self.point_clouds_loader_dialog.two_folders_signal
        signal_two.connect(self.emitFolderPathsSignal)
        signal_single = self.point_clouds_loader_dialog.folder_pc_signal
        signal_single.connect(self.emitFolderPathSignal)
        self.logger.info("Finished initialising point clouds loader dialog")

        self.logger.info("Initialising images loader dialog...")
        self.images_loader_dialog = ImagesLoaderDialog()
        ild_closed_signal = self.images_loader_dialog.closed
        ild_closed_signal.connect(partial(self.setDisabled, False))
        multi_images_signal = self.images_loader_dialog.multi_images_signal
        multi_images_signal.connect(self.emitMultiImagesSignal)
        two_folders_images_signal = self.images_loader_dialog.two_folders_signal
        two_folders_images_signal.connect(self.emitTwoFoldersImagesSignal)
        single_folder_images_signal = self.images_loader_dialog.single_folder_signal
        single_folder_images_signal.connect(self.emitFolderImagesSignal)
        self.logger.info("Finished initialising images loader dialog")

        # Adding 360 images loader dialog
        self.logger.info("Initialising 360 images loader dialog...")
        self.images360_loader_dialog = Images360LoaderDialog()
        i360ld_closed_signal = self.images360_loader_dialog.closed
        i360ld_closed_signal.connect(partial(self.setDisabled, False))
        multi_images360_signal = self.images360_loader_dialog.multi_images360_signal
        multi_images360_signal.connect(self.emitMultiImages360Signal)
        two_folders_images360_signal = self.images360_loader_dialog.two_360folders_signal
        two_folders_images360_signal.connect(self.emitTwoFoldersImages360Signal)
        single_folder_images360_signal = self.images360_loader_dialog.single_360folder_signal
        single_folder_images360_signal.connect(self.emitFolderImages360Signal)
        self.logger.info("Finished initialising 360 images loader dialog")

    """ Initialise sliders """
    def initialiseSliders(self):
        self.logger.info("Initialising sliders...")

        self.sliders_frame = QtWidgets.QFrame()
        self.sliders_h_layout = QtWidgets.QGridLayout()
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        size_policy.setHorizontalStretch(1)

        # Azimuth area
        self.logger.info("Drawing azimuth slider...")
        azimuth_widget = QtWidgets.QFrame()
        vbox_azimuth = QtWidgets.QVBoxLayout()

        self.azimuth_label = QtWidgets.QLabel("AZIMUTH")

        self.azimuth_slider = QtWidgets.QSlider()
        self.azimuth_slider.setOrientation(QtCore.Qt.Vertical)
        self.azimuth_slider.setTickPosition(QtWidgets.QSlider.TicksLeft)
        self.azimuth_slider.setTickInterval(30)
        self.azimuth_slider.setMinimum(0)
        self.azimuth_slider.setMaximum(360)

        self.azimuth_slider.valueChanged.connect(self.changedValue)
        initial_camera_pos = self.graphic_area.plot_3d.cameraPosition()
        initial_angle = math.degrees(math.atan2(initial_camera_pos.y(), initial_camera_pos.x()))
        self.azimuth_value = QtWidgets.QLabel("")
        self.azimuth_slider.setValue(int(initial_angle))

        vbox_azimuth.addWidget(self.azimuth_label, alignment=QtCore.Qt.AlignHCenter)
        vbox_azimuth.addWidget(self.azimuth_slider, alignment=QtCore.Qt.AlignHCenter)
        vbox_azimuth.addWidget(self.azimuth_value, alignment=QtCore.Qt.AlignHCenter)
        azimuth_widget.setLayout(vbox_azimuth)
        azimuth_widget.setSizePolicy(size_policy)

        # Elevation area
        self.logger.info("Drawing elevation slider...")
        elevation_widget = QtWidgets.QFrame()
        vbox_elevation = QtWidgets.QVBoxLayout()

        self.elevation_label = QtWidgets.QLabel("ELEVATION")

        self.elevation_slider = QtWidgets.QSlider()
        self.elevation_slider.setOrientation(QtCore.Qt.Vertical)
        self.elevation_slider.setTickPosition(QtWidgets.QSlider.TicksLeft)
        self.elevation_slider.setTickInterval(20)
        self.elevation_slider.setMinimum(-90)
        self.elevation_slider.setMaximum(90)

        self.elevation_slider.valueChanged.connect(self.changedElevationValue)
        elevation_angle = math.degrees(math.atan2(initial_camera_pos.z(), math.sqrt(math.pow(initial_camera_pos.x(),2) + math.pow(initial_camera_pos.y(),2))))
        self.elevation_value = QtWidgets.QLabel("")
        self.elevation_slider.setValue(int(elevation_angle))

        vbox_elevation.addWidget(self.elevation_label, alignment=QtCore.Qt.AlignHCenter)
        vbox_elevation.addWidget(self.elevation_slider, alignment=QtCore.Qt.AlignHCenter)
        vbox_elevation.addWidget(self.elevation_value, alignment=QtCore.Qt.AlignHCenter)
        elevation_widget.setLayout(vbox_elevation)
        elevation_widget.setSizePolicy(size_policy)

        # Distance area
        self.logger.info("Drawing distance slider...")
        distance_widget = QtWidgets.QFrame()
        vbox_distance = QtWidgets.QVBoxLayout()

        self.distance_label = QtWidgets.QLabel("DISTANCE")

        self.distance_slider = QtWidgets.QSlider()
        self.distance_slider.setOrientation(QtCore.Qt.Vertical)
        self.distance_slider.setTickPosition(QtWidgets.QSlider.TicksLeft)
        self.distance_slider.setTickInterval(15)
        self.distance_slider.setMinimum(10)
        self.distance_slider.setMaximum(160)

        self.distance_slider.valueChanged.connect(self.changedDistanceValue)
        distance = math.sqrt(math.pow(initial_camera_pos.x(), 2) + math.pow(initial_camera_pos.y(), 2) + + math.pow(initial_camera_pos.z(), 2))
        self.distance_value = QtWidgets.QLabel("")
        self.distance_slider.setValue(int(distance))

        vbox_distance.addWidget(self.distance_label, alignment=QtCore.Qt.AlignHCenter)
        vbox_distance.addWidget(self.distance_slider, alignment=QtCore.Qt.AlignHCenter)
        vbox_distance.addWidget(self.distance_value, alignment=QtCore.Qt.AlignHCenter)
        distance_widget.setLayout(vbox_distance)
        distance_widget.setSizePolicy(size_policy)

        # Distance area
        self.logger.info("Drawing point size slider...")
        point_size_widget = QtWidgets.QFrame()
        vbox_point_size = QtWidgets.QVBoxLayout()

        self.point_size_label = QtWidgets.QLabel("POINT SIZE")

        self.point_size_slider = QtWidgets.QSlider()
        self.point_size_slider.setOrientation(QtCore.Qt.Vertical)
        self.point_size_slider.setTickPosition(QtWidgets.QSlider.TicksLeft)
        self.point_size_slider.setTickInterval(1)
        self.point_size_slider.setMinimum(1)
        self.point_size_slider.setMaximum(10)
        self.point_size_slider.setDisabled(True)

        self.point_size_slider.valueChanged.connect(self.changedPointSizeValue)
        self.point_size_value = QtWidgets.QLabel("1")
        self.point_size_slider.setValue(1)

        vbox_point_size.addWidget(self.point_size_label, alignment=QtCore.Qt.AlignHCenter)
        vbox_point_size.addWidget(self.point_size_slider, alignment=QtCore.Qt.AlignHCenter)
        vbox_point_size.addWidget(self.point_size_value, alignment=QtCore.Qt.AlignHCenter)
        point_size_widget.setLayout(vbox_point_size)
        point_size_widget.setSizePolicy(size_policy)

        # Areas composition
        self.sliders_h_layout.addWidget(azimuth_widget, 0, 0, 1, 1)
        self.sliders_h_layout.addWidget(elevation_widget, 0, 1, 1, 1)
        self.sliders_h_layout.addWidget(distance_widget, 1, 0, 1, 1)
        self.sliders_h_layout.addWidget(point_size_widget, 1, 1, 1, 1)
        self.sliders_frame.setLayout(self.sliders_h_layout)

        self.logger.info("Finished initialising sliders")

    def changedValue(self):
        size = self.azimuth_slider.value()
        self.azimuth_value.setText(str(size))
        if not self.block:
            self.graphic_area.plot_3d.setCameraPosition(azimuth=size)

    def changedElevationValue(self):
        size = self.elevation_slider.value()
        self.elevation_value.setText(str(size))
        if not self.block:
            self.graphic_area.plot_3d.setCameraPosition(elevation=size)

    def changedDistanceValue(self):
        value = self.distance_slider.value()
        self.distance_value.setText(str(value))
        if not self.block:
            self.graphic_area.plot_3d.setCameraPosition(distance=value)

    def changedPointSizeValue(self):
        value = self.point_size_slider.value()
        self.point_size_value.setText(str(value))
        if not self.block:
            for item in list(self.graphic_area.plot_3d.clouds_data.values()):
                item.setData(size=value)

    # --------------------------------------------------------------
    # -------------------------- LOADERS ---------------------------
    # --------------------------------------------------------------

    def loadPG(self):
        self.pose_graph_loader_dialog.show()
        self.pose_graph_loader_dialog.raise_()
        self.pose_graph_loader_dialog.loadg2oFile()

    def loadPCS(self):
        self.point_clouds_loader_dialog.show()
        self.point_clouds_loader_dialog.activateWindow()
        self.point_clouds_loader_dialog.raise_()
        self.setDisabled(True)

    def loadIMGS(self):
        self.images_loader_dialog.show()
        self.images_loader_dialog.activateWindow()
        self.images_loader_dialog.raise_()
        self.setDisabled(True)

    # Add loader for 360 images
    def loadIMGS360(self):
        self.images360_loader_dialog.show()
        self.images360_loader_dialog.activateWindow()
        self.images360_loader_dialog.raise_()
        self.setDisabled(True)

    # --------------------------------------------------------------
    # ---------------------- COLOUR TOGGLERS -----------------------
    # --------------------------------------------------------------
    def togglePCsColour(self):
        self.graphic_area.plot_3d.toggleMapColour()

    def toggleJourneyMode(self):
        if self.graphic_area.plot_3d.journey_mode:
            self.graphic_area.plot_3d.journey_mode = False
            self.set_journey_mode_action.setIcon(QtGui.QIcon("./icons/journey_off.png"))
        else:
            self.graphic_area.plot_3d.journey_mode = True
            self.set_journey_mode_action.setIcon(QtGui.QIcon("./icons/journey_on.png"))

    # --------------------------------------------------------------
    # -------------------------- CLEANERS --------------------------
    # --------------------------------------------------------------
    def cleanPoseGraph(self):
        self.clean_pose_graph_action.setDisabled(True)
        self.clean_point_clouds_action.setDisabled(True)
        self.clean_images_action.setDisabled(True)
        self.clean_images360_action.setDisabled(True)
        self.graphic_area.plot_2d.cleanPlot()
        self.graphic_area.image_viewer.cleanViewer()
        self.graphic_area.plot_3d.cleanPlot()
        self.has_graph = False
        self.has_clouds = False
        self.has_images = False
        self.hasimages360 = False
        self.clean_pose_graph_signal.emit()

    def cleanPointClouds(self):
        self.clean_point_clouds_action.setDisabled(True)
        self.point_size_slider.setDisabled(True)
        self.toggle_colour_action.setDisabled(True)
        self.set_journey_mode_action.setDisabled(True)
        self.graphic_area.plot_3d.cleanClouds()
        self.has_clouds = False
        self.clean_point_clouds_signal.emit()

    def cleanImages(self):
        self.clean_images_action.setDisabled(True)
        self.graphic_area.image_viewer.cleanViewer()
        self.graphic_area.image_selected = False
        self.has_images = False
        self.clean_images_signal.emit()

    # Add 360 images cleaner
    def cleanImages360(self):
        self.clean_images360_action.setDisabled(True)
        self.graphic_area.image360_viewer.cleanViewer360()
        self.graphic_area.image360_selected = False
        self.has_images360 = False
        self.clean_images360_signal.emit()
    

    # --------------------------------------------------------------
    # ------------------------- SHOW/HIDE --------------------------
    # --------------------------------------------------------------
    def showhideInfoPanel(self):
        if self.info_dock.isHidden():
            self.info_dock.show()
            self.showhide_info_action.setIcon(QtGui.QIcon("./icons/show_info.png"))
        else:
            self.info_dock.hide()
            self.showhide_info_action.setIcon(QtGui.QIcon("./icons/hide_info.png"))

    def showhideLogPanel(self):
        if self.log_dock.isHidden():
            self.log_dock.show()
            self.showhide_log_action.setIcon(QtGui.QIcon("./icons/show_log.png"))
        else:
            self.log_dock.hide()
            self.showhide_log_action.setIcon(QtGui.QIcon("./icons/hide_log.png"))

    def showhideSlidersPanel(self):
        if self.sliders_dock.isHidden():
            self.sliders_dock.show()
            self.showhide_sliders_action.setIcon(QtGui.QIcon("./icons/show_sliders.png"))
        else:
            self.sliders_dock.hide()
            self.showhide_sliders_action.setIcon(QtGui.QIcon("./icons/hide_sliders.png"))

    # --------------------------------------------------------------
    # -------------------------- EMITTERS --------------------------
    # --------------------------------------------------------------
    @QtCore.pyqtSlot(SigString)
    def emitFilenameSignal(self, pg_filename: SigString):
        self.pg_filename_signal.emit(pg_filename)

    @QtCore.pyqtSlot(SigStringList)
    def emitFilenamesSignal(self, pc_filenames: SigStringList):
        self.multi_pcs_signal.emit(pc_filenames)

    @QtCore.pyqtSlot(SigStringList)
    def emitFolderPathsSignal(self, folder_paths: SigStringList):
        self.two_folders_pcs_signal.emit(folder_paths)

    @QtCore.pyqtSlot(SigStringList)
    def emitFolderPathSignal(self, folder_path: SigString):
        self.single_folder_pcs_signal.emit(folder_path)

    @QtCore.pyqtSlot(SigStringList)
    def emitMultiImagesSignal(self, images_filenames: SigStringList):
        self.multi_imgs_signal.emit(images_filenames)

    @QtCore.pyqtSlot(SigStringList)
    def emitTwoFoldersImagesSignal(self, folders_paths: SigStringList):
        self.two_folders_imgs_signal.emit(folders_paths)

    @QtCore.pyqtSlot(SigString)
    def emitFolderImagesSignal(self, folder_path: SigString):
        self.single_folder_imgs_signal.emit(folder_path)

    # Adding emitters for 360 images
    @QtCore.pyqtSlot(SigStringList)
    def emitMultiImages360Signal(self, images360_filenames: SigStringList):
        self.multi_imgs360_signal.emit(images360_filenames)

    @QtCore.pyqtSlot(SigStringList)
    def emitTwoFoldersImages360Signal(self, folders360_paths: SigStringList):
        self.two_folders_imgs360_signal.emit(folders360_paths)

    @QtCore.pyqtSlot(SigString)
    def emitFolderImages360Signal(self, folder360_path: SigString):
        self.single_folder_imgs360_signal.emit(folder360_path)

    @QtCore.pyqtSlot(int)
    def emitSelectedPoseSignal(self, pose_index: int):
        self.load_pcs_action.setDisabled(True)
        self.load_images_action.setDisabled(True)
        # Adding action for 360 images
        self.load_images360_action.setDisabled(True)

        self.clean_pose_graph_action.setDisabled(True)
        self.clean_point_clouds_action.setDisabled(True)
        self.clean_images_action.setDisabled(True)

        # Add emitter for clean 360 images
        self.clean_images360_action.setDisabled(True)

        self.selected_pose_signal.emit(pose_index)

    # --------------------------------------------------------------
    # -------------------------- HANDLERS --------------------------
    # --------------------------------------------------------------
    @QtCore.pyqtSlot()
    def unselectPose(self):
        self.load_pcs_action.setDisabled(False)
        self.load_images_action.setDisabled(False)
        
        # Add 360 image select button unlock
        self.load_images360_action.setDisabled(False)

        if self.has_graph:
            self.clean_pose_graph_action.setDisabled(False)
        if self.has_clouds:
            self.clean_point_clouds_action.setDisabled(False)
        if self.has_images:
            self.clean_images_action.setDisabled(False)
        if self.has_images360:
            self.clean_images360_action.setDisabled(False)

        self.info_form.clearText()

    def displayNodeInfo(self, node):
        self.info_form.setText(node.pos.x, node.pos.y, node.pos.z, node.roll, node.pitch, node.yaw, node.quaternion, node.cloud, node.img, node.img360)

    @QtCore.pyqtSlot(SigPosition)
    def changeSlidersValues(self, camera_position: SigPosition):
        pose = camera_position.content

        azimuth = math.degrees(math.atan2(pose.y, pose.x))
        elevation = math.degrees(math.atan2(pose.z, math.sqrt(math.pow(pose.x,2) + math.pow(pose.y,2))))

        self.block = True
        self.azimuth_slider.setValue(int(azimuth))
        self.elevation_slider.setValue(int(elevation))
        self.block = False

    # --------------------------------------------------------------
    # ------------------------- DELEGATORS -------------------------
    # --------------------------------------------------------------
    def drawPoseGraph(self, nodes: OrderedDict, edges: list):
        self.graphic_area.drawPoseGraph(nodes, edges)
        self.clean_pose_graph_action.setDisabled(False)
        self.has_graph = True

    def drawPointClouds(self, nodes: list):
        self.graphic_area.drawPointClouds(nodes)
        self.clean_point_clouds_action.setDisabled(False)
        self.point_size_slider.setDisabled(False)
        self.toggle_colour_action.setDisabled(False)
        self.set_journey_mode_action.setDisabled(False)
        self.has_clouds = True

    def imagesLoaded(self, nodes: list):
        self.graphic_area.imagesOk(nodes)
        self.clean_images_action.setDisabled(False)
        self.has_images = True

    # Add delegator for 360 images
    def images360Loaded(self, nodes: list):
        self.graphic_area.images360Ok(nodes)
        self.clean_images360_action.setDisabled(False)
        self.has_images360 = True

class QTextEditLogger(logging.Handler):
    def __init__(self, parent):
        super().__init__()
        self.widget = QtWidgets.QPlainTextEdit(parent)
        self.widget.setReadOnly(True)

    def emit(self, record):
        msg = self.format(record)
        self.widget.appendPlainText(msg)

    def write(self, m):
        pass
