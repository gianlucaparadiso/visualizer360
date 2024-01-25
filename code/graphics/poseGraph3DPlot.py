import logging, math
from collections import OrderedDict
import numpy as np
from PyQt5 import QtCore, QtGui
import pyqtgraph as pg
import pyqtgraph.opengl as gl
from signals.sigPosition import SigPosition
from structures.point3d import Point3D
import utilities.paletteCreator as pc
from utilities.threadWorker import Worker


""" Class representing the 3D plot widget and its content """
class PoseGraph3DPlot(gl.GLViewWidget):
    camera_position_signal = QtCore.pyqtSignal(SigPosition) # signal emitted when changing the camera position

    def __init__(self, parent=None):
        super(PoseGraph3DPlot, self).__init__(parent)

        # Logger setup
        self.logger = logging.getLogger()

        self.logger.info("Creating PoseGraph3DPlot...")
        self.__initUI()
        self.logger.info("Finished creating PoseGraph3DPlot")

    def __initUI(self):
        # Create style for the main plot
        self.logger.info("Creating 3D plot...")
        self.setWindowTitle('pyqtgraph example: GLLinePlotItem')
        self.setGeometry(0, 110, 1920, 1080)
        self.setBackgroundColor(pg.mkColor(150, 150, 150, 255))
        self.opts['distance'] = 40

        # Create and set plot elements
        self.logger.info("Creating and setting plot elements...")
        self.graph_poses = None
        self.edges = None
        self.clouds_data = dict()

        # Initialise data elements
        self.logger.info("Initialising data elements...")
        self.journey_mode = True
        self.toggled_map = False
        self.poses: None
        self.graph_colors: None
        self.graph_colors_unselected: None
        self.main_poses = dict()
        self.main_colors = dict()
        self.curr_poses = dict()
        self.curr_colors = dict()
        self.num_nodes = 0
        self.selected_idx = -1
        self.data_correspondences = dict()

    # --------------------------------------------------------------
    # ----------------------- DRAWING METHODS ----------------------
    # --------------------------------------------------------------
    """ Method used to draw the pose graph """
    def drawPoseGraph3D(self, nodes: OrderedDict, edges: list):

        self.logger.info("Drawing 2D pose graph...")
        self.cleanPlot()
        self.__drawNodes(nodes)
        graph_edges = self.__drawEdges(list(nodes.keys()), edges)

        self.graph_poses = gl.GLScatterPlotItem(pos=self.poses,
                                                size=30,
                                                color=self.graph_colors,
                                                glOptions='translucent')
        self.addItem(self.graph_poses)
        self.edges = gl.GLLinePlotItem(pos=graph_edges, mode='lines')
        self.addItem(self.edges)

        self.num_nodes = len(nodes)
        idx = 0
        for key in list(nodes.keys()):
            self.data_correspondences[key] = idx
            idx += 1
        self.logger.info("Finished drawing 3D pose graph...")

    """ Method used to draw the nodes of the pose graph, assigning them a color """
    def __drawNodes(self, nodes_dict: OrderedDict):
        # Create the color palette for the nodes
        self.logger.info("Creating color palette for nodes...")
        color_map = pc.createPalette("gnuplot_r", len(nodes_dict))
        white = np.array([1.0, 1.0, 1.0, 0.5])
        whites = np.tile(white, (len(nodes_dict), 1))

        # Create the nodes in the graph
        self.logger.info("Creating nodes from data...")
        nodes = list(nodes_dict.values())
        graph_node_poses = np.empty([len(nodes_dict), 3])
        colors = np.empty([len(nodes_dict), 4])

        for i in range(len(nodes)):
            curr_spot = nodes[i]
            graph_node_poses[i] = [curr_spot.pos.x, curr_spot.pos.y, curr_spot.pos.z]
            colors[i] = color_map(i)

        self.graph_colors = colors
        self.graph_colors_unselected = whites
        self.poses = graph_node_poses

    """ Method used to draw the edges of the pose graph """
    def __drawEdges(self, keys: list, edges: list):
        # Create the edges in the graph
        self.logger.info("Creating edges from data...")
        graph_edges = np.empty([len(edges) * 2, 3])

        for i in range(len(edges)):
            curr_edge = edges[i]
            graph_edges[2*i] = self.poses[keys.index(curr_edge.start)]
            graph_edges[2*i + 1] = self.poses[keys.index(curr_edge.end)]

        return graph_edges

    """ Method used to draw the point clouds associated to the pose graph """
    def drawPointClouds(self, nodes: list):
        self.logger.info("Drawing point clouds...")
        for node in nodes:
            if node.cloud is not None:
                curr_cloud = np.asarray(node.cloud.points)
                curr_data_idx = node.idx
                self.main_poses[curr_data_idx] = curr_cloud
                self.curr_poses[curr_data_idx] = curr_cloud

                curr_colour = (0.6, 0.6, 0.6, 1.0)
                self.main_colors[curr_data_idx] = curr_colour
                self.curr_colors[curr_data_idx] = curr_colour

                curr_scatterplot = gl.GLScatterPlotItem(pos=curr_cloud, size=1, color=curr_colour)
                self.clouds_data[curr_data_idx] = curr_scatterplot
                self.addItem(curr_scatterplot)
        self.logger.info("Finished drawing point clouds")

        self.threadpool = QtCore.QThreadPool()
        self.logger.info("Coloring the point clouds with multithreading...")
        worker = Worker(self.setPointCloudsColour)
        self.threadpool.start(worker)

    """ Method used to clean the plot and data when drawing a new pose graph """
    def cleanPlot(self):
        self.logger.info("Cleaning 3D plot...")
        if self.graph_poses is not None:
            self.removeItem(self.graph_poses)
            self.graph_poses = None
        if self.edges is not None:
            self.removeItem(self.edges)
            self.edges = None

        self.journey_mode = True
        self.poses = None
        self.graph_colors = None
        self.graph_colors_unselected = None
        self.num_nodes = 0
        self.selected_idx = -1
        self.data_correspondences.clear()

        self.cleanClouds()
        self.logger.info("Finished cleaning 3D plot")

    """ Method used to clean the plot and data from the point clouds """
    def cleanClouds(self):
        self.logger.info("Cleaning point clouds")
        for scatter in list(self.clouds_data.values()):
            self.removeItem(scatter)

        self.toggled_map = False
        self.main_poses.clear()
        self.main_colors.clear()
        self.curr_poses.clear()
        self.curr_colors.clear()
        self.clouds_data.clear()
        self.logger.info("Finished cleaning point clouds")

    """ Method used to create colors for all the points of all the point clouds (no assignment) """
    def setPointCloudsColour(self, progress_callback):
        self.color_map = pc.createSPalette("brg_r")
        for key in self.curr_poses:
            curr_cloud = self.curr_poses[key]
            self.setPointCloudColour(curr_cloud, key)

    """ Method used to create colors for all the points of a point cloud (no assignment) """
    def setPointCloudColour(self, point_cloud, key):
        z = point_cloud[:, 2]
        colors = self.color_map(z/3)

        self.curr_colors[key] = colors

    """ Method used to toggle whether the displayed clouds are colored or gray """
    def toggleMapColour(self):
        if self.toggled_map:
            self.logger.info("Displaying gray clouds")
            for key in self.clouds_data:
                curr_cloud = self.clouds_data[key]
                curr_cloud.setData(color=self.main_colors[key])
            self.toggled_map = False
        else:
            self.logger.info("Displaying colored clouds")
            for key in self.clouds_data:
                curr_cloud = self.clouds_data[key]
                curr_cloud.setData(color=self.curr_colors[key])
            self.toggled_map = True

    """ Method used to handle the selection of a graph pose """
    def selectPose(self, data_idx):
        self.logger.info("Node " + str(data_idx) + " selected")

        # If the node does not have a point cloud, hide everything
        if data_idx not in self.data_correspondences:
            for key in self.clouds_data:
                self.clouds_data[key].hide()
            return
        
        idx = self.data_correspondences[data_idx]
        color_copy = np.copy(self.graph_colors_unselected)
        color_copy[idx] = np.array([1.0, 0.0, 0.0, 1.0])
        self.graph_poses.setData(color=color_copy)

        curr_point = self.poses[idx]
        if 0 < idx < len(self.poses) - 1:
            next_point = self.poses[idx+1]
            prev_point = self.poses[idx-1]
            azimuth = math.degrees(math.atan2((next_point[1]-prev_point[1]), (next_point[0]-prev_point[0]))) + 180
        elif idx == len(self.poses) - 1:
            prev_point = self.poses[idx-1]
            azimuth = math.degrees(math.atan2((curr_point[1] - prev_point[1]), (curr_point[0] - prev_point[0]))) + 180
        else:
            next_point = self.poses[idx+1]
            azimuth = math.degrees(math.atan2((next_point[1] - curr_point[1]), (next_point[0] - curr_point[0]))) + 180

        if self.journey_mode:
            self.setCameraPosition(pos=QtGui.QVector3D(curr_point[0], curr_point[1], curr_point[2]), azimuth=azimuth)
        else:
            self.setCameraPosition(pos=QtGui.QVector3D(curr_point[0], curr_point[1], curr_point[2]))

        if len(self.clouds_data) != 0:
            for key in self.clouds_data:
                if key != data_idx:
                    self.clouds_data[key].hide()
                else:
                    self.clouds_data[key].show()

        self.selected_idx = idx

        # Emit camera position signal
        initial_camera_pos = self.cameraPosition()
        point = Point3D(initial_camera_pos.x(), initial_camera_pos.y(), initial_camera_pos.z())
        self.camera_position_signal.emit(SigPosition(point))

    """ Method used to handle the unselection of a graph pose """
    def unselectPose(self):
        self.logger.info("Node " + str(self.selected_idx) + " unselected")
        self.graph_poses.setData(color=self.graph_colors)

        if len(self.clouds_data) != 0:
            for key in self.clouds_data:
                self.clouds_data[key].show()

        self.selected_idx = -1

    """ Method used to emit a camera position signal when the mouse click is released """
    def mouseReleaseEvent(self, ev):
        super().mouseReleaseEvent(ev)

        initial_camera_pos = self.cameraPosition()
        point = Point3D(initial_camera_pos.x(), initial_camera_pos.y(), initial_camera_pos.z())
        self.camera_position_signal.emit(SigPosition(point))

    """ Method used to emit a camera position signal when the mouse wheel is scrolled """
    def wheelEvent(self, ev):
        super().wheelEvent(ev)

        initial_camera_pos = self.cameraPosition()
        point = Point3D(initial_camera_pos.x(), initial_camera_pos.y(), initial_camera_pos.z())
        self.camera_position_signal.emit(SigPosition(point))

