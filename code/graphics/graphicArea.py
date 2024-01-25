import logging
from collections import OrderedDict
from PyQt5 import QtCore, QtWidgets
from graphics.poseGraph3DPlot import PoseGraph3DPlot
from graphics.poseGraph2DPlot import PoseGraph2DPlot
from graphics.imageViewer import QtImageViewer
from signals.sigPosition import SigPosition

# Add 360 images viewer
from graphics.image360Viewer import GLWidget
from PIL import Image

""" Class representing the graphic area of the visualiser, including widgets and content """
class GraphicArea(QtWidgets.QFrame):
    selected_pose_signal = QtCore.pyqtSignal(int)
    unselected_pose_signal = QtCore.pyqtSignal()

    camera_position_signal = QtCore.pyqtSignal(SigPosition)

    def __init__(self):
        super(GraphicArea, self).__init__()

        # Logger setup
        self.logger = logging.getLogger()
        self.logger.info("Creating GraphicArea...")

        self.vertical_layout = QtWidgets.QVBoxLayout()

        # Prepare 2D area
        self.horizontal_splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        self.visual_area_2d = QtWidgets.QFrame()

        self.plot_2d = PoseGraph2DPlot(self)
        self.plot_2d.clicked_signal.connect(self.selectPose)
        self.plot_2d.unclicked_signal.connect(self.unselectPose)

        self.image_viewer = QtImageViewer()
        self.image_viewer.canZoom = True
        self.image_viewer.canPan = False
        self.image_selected = False

        # Add 360 images visualiser widget to UI
        self.image360_viewer = GLWidget()
        self.image360_selected = False

        self.horizontal_splitter.addWidget(self.plot_2d)
        self.horizontal_splitter.addWidget(self.image_viewer)
        self.horizontal_splitter.addWidget(self.image360_viewer)
        self.horizontal_splitter.setSizes([1000, 1000, 1000])

        # Prepare 3D area
        self.vertical_splitter = QtWidgets.QSplitter(QtCore.Qt.Vertical)
        self.plot_3d = PoseGraph3DPlot()
        self.plot_3d.camera_position_signal.connect(self.emitCameraPosition)
        self.vertical_splitter.addWidget(self.horizontal_splitter)
        self.vertical_splitter.addWidget(self.plot_3d)
        self.vertical_splitter.setSizes([1000, 1000])

        # Finish up drawing area
        self.vertical_layout.addWidget(self.vertical_splitter)
        self.setLayout(self.vertical_layout)

        self.logger.info("Finished creating GraphicArea")

    """ Method used to delegate the creation of the pose graph in the 2D and 3D objects """
    def drawPoseGraph(self, nodes: OrderedDict, edges: list):
        self.plot_2d.drawPoseGraph2D(nodes, edges)
        self.plot_3d.drawPoseGraph3D(nodes, edges)

    """ Method used to delegate the creation of the point clouds in the 3D object """
    def drawPointClouds(self, nodes: list):
        #self.plot_2d.drawClouds(nodes)
        self.plot_3d.drawPointClouds(nodes)

    """ Method used to load the images in the image viewer object, for later use """
    def imagesOk(self, nodes: list):
        self.image_viewer.setDefaultImage()
        self.image_selected = True
        for node in nodes:
            if node.img is not None:
                self.image_viewer.images[node.idx] = node.img

    """ Method used to load the 360 images in the 360 image viewer object, for later use """
    def images360Ok(self, nodes: list):
        self.image360_viewer.setDefaultImage360()
        self.image360_selected = True
        self.logger.info("inside image3600K")
        for node in nodes:
           if node.img360 is not None:
                self.logger.info("node.image360 is not None")
                self.image360_viewer.images[node.idx] = node.img360


    """ Method used to handle the selection of the graph phose event in all the graphic area elements"""
    @QtCore.pyqtSlot(int)
    def selectPose(self, pose_index: int):
        self.selected_pose_signal.emit(pose_index)

        self.logger.info("select pose: %i", pose_index)

        if pose_index in self.image_viewer.images:
            self.image_viewer.setImageByIndex(pose_index)
            self.logger.info("setImageByIndex")
        else:
            self.image_viewer.setDefaultImage()

        if pose_index in self.image360_viewer.images:
            self.logger.info("setImage360ByIndex")
            # Add call to setImage360ByIndex
            self.image360_viewer.setImage360ByIndex(pose_index)
        else:
            # Same reasoning as above, set image visualized to default when no pose is selected
            self.image360_viewer.setDefaultImage360()
        self.plot_3d.selectPose(pose_index)

    """ Method used to handle the selection of the graph phose event in all the graphic area elements"""
    @QtCore.pyqtSlot()
    def unselectPose(self):
        self.unselected_pose_signal.emit()
        if self.image_selected:
            self.image_viewer.setDefaultImage()
        # Duplicate logic for 360 image
        if self.image360_selected:
            self.image360_viewer.setDefaultImage360()
        self.plot_3d.unselectPose()

    """ Method used for delegation of the 3D plot camera pose changed event """
    @QtCore.pyqtSlot(SigPosition)
    def emitCameraPosition(self, cameraPosition: SigPosition):
        self.camera_position_signal.emit(cameraPosition)
