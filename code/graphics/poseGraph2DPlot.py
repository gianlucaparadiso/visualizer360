import logging
from collections import OrderedDict
from typing import List, Union
import numpy as np
from PyQt5 import QtCore, QtGui
import pyqtgraph as pg
import utilities.paletteCreator as pc


""" Class representing the 2D plot widget and its content """
class PoseGraph2DPlot(pg.GraphicsLayoutWidget):
    clicked_signal = QtCore.pyqtSignal(int)
    unclicked_signal = QtCore.pyqtSignal()

    def __init__(self, parent):
        super(PoseGraph2DPlot, self).__init__(parent, title="2D")

        # Logger setup
        self.logger = logging.getLogger()

        self.logger.info("Creating PoseGraph2DPlot...")
        self.__initUI()
        self.logger.info("Finished creating PoseGraph2DPlot")

    def __initUI(self):
        # Create style for the main plot
        self.logger.info("Creating 2D plot...")
        self.setBackground(pg.mkColor(150, 150, 150, 255))
        self.plot: pg.PlotItem = self.addPlot()
        self.plot.showGrid(True, True, 0.5)

        # Set left axis y
        self.logger.info("Setting left axis...")
        left_axis: pg.AxisItem = self.plot.getAxis('left')
        left_axis.setPen(pg.mkPen(0, 0, 0))
        left_axis.setTextPen(pg.mkPen(0, 0, 0))
        left_axis.setLabel("y [m]")

        # Set bottom axis x
        self.logger.info("Setting bottom axis...")
        right_axis: pg.AxisItem = self.plot.getAxis('bottom')
        right_axis.setPen(pg.mkPen(0, 0, 0))
        right_axis.setTextPen(pg.mkPen(0, 0, 0))
        right_axis.setLabel("x [m]")

        # Create and set plot elements
        self.logger.info("Creating and setting plot elements...")
        self.pose_graph = pg.GraphItem()
        self.pose_graph.scatter.sigClicked.connect(self.clickedNode)
        self.plot.addItem(self.pose_graph)
        self.display_text = pg.TextItem(anchor=(0, 0), border='w', fill=(0, 0, 255, 200))

        # Initialise data elements
        self.logger.info("Initialising data elements...")
        self.num_nodes = 0
        self.selected_idx = -1
        self.data_correspondences = dict()
        self.colors = list()

        # TODO update for point clouds projected in 2D, not used now
        self.point_clouds = list()

    # --------------------------------------------------------------
    # ----------------------- DRAWING METHODS ----------------------
    # --------------------------------------------------------------
    """ Method used to draw the pose graph """
    def drawPoseGraph2D(self, nodes: OrderedDict, edges: list):

        self.logger.info("Drawing 2D pose graph...")
        self.cleanPlot()
        colors: List[Union[QtGui.QBrush, QtGui.QBrush]]
        graph_node_poses, colors = self.__drawNodes(nodes)
        graph_edges = self.__drawEdges(list(nodes.keys()), edges)

        self.pose_graph.setData(pos=graph_node_poses,
                                adj=graph_edges,
                                size=20,
                                symbolBrush=colors,
                                pen=pg.mkPen(color=(0, 0, 0, 255), width=8),
                                symbolPen=pg.mkPen(color=(0, 0, 0, 255))
                                )

        self.num_nodes = len(graph_node_poses)
        self.colors = colors
        for i in range(len(nodes)):
            self.data_correspondences[i] = list(nodes.keys())[i]
        self.logger.info("Finished drawing 2D pose graph")

    """ Method used to draw the nodes of the pose graph, assigning them a color """
    def __drawNodes(self, nodes_dict: OrderedDict):
        # Create the color palette for the nodes
        self.logger.info("Creating color palette for nodes...")
        color_map = pc.createPalette("gnuplot_r", len(nodes_dict))

        # Create the nodes in the graph
        self.logger.info("Creating nodes from data...")
        nodes = list(nodes_dict.values())
        graph_nodes_poses = np.empty([len(nodes), 2])
        colors = list()

        for i in range(len(nodes)):
            curr_node = nodes[i]
            graph_nodes_poses[i] = [curr_node.pos.x, curr_node.pos.y]
            colors.append(pg.mkBrush(color=np.array(color_map(i)) * 255))

        return graph_nodes_poses, colors

    """ Method used to draw the edges of the pose graph """
    def __drawEdges(self, keys: list, edges: list):
        # Create the edges in the graph
        self.logger.info("Creating edges from data...")
        graph_edges = np.empty([len(edges), 2], dtype=int)

        for i in range(0, len(edges)):
            curr_edge = edges[i]
            graph_edges[i] = [keys.index(curr_edge.start), keys.index(curr_edge.end)]

        return graph_edges

    """ Method used to clean the plot and data when drawing a new pose graph """
    def cleanPlot(self):
        self.logger.info("Cleaning 2D plot...")
        self.pose_graph.setData(pen=pg.mkPen(color=(0, 0, 0, 0)))
        self.num_nodes = 0
        self.selected_idx = -1
        self.data_correspondences.clear()
        self.colors.clear()
        self.logger.info("Finished cleaning 2D plot")

    """ Unused method to draw 2D point clouds; pyqtgraph performances degrade over 10k points """
    def drawClouds(self, nodes: list):
        for node in nodes:
            if node.cloud is not None:
                curr_cloud = np.asarray(node.cloud.points)
                curr_cloud = curr_cloud[(curr_cloud[:, 2] > -1.5)]
                curr_cloud_2d = curr_cloud[:, [0, 1]]
                curr_scatter_plot = pg.ScatterPlotItem(pos=curr_cloud_2d, color=(0, 0, 0, 1), size=0.1, pxMode=False)
                self.point_clouds.append(curr_scatter_plot)
                self.plot.plot(curr_cloud[:, 0], curr_cloud[:, 1], pen=None, symbol='o', symbolPen=pg.mkPen(color=(0, 0, 255), width=0), symbolBrush=pg.mkBrush(0, 0, 255, 255), symbolSize=0.1)
                self.plot.addItem(curr_scatter_plot)

    # --------------------------------------------------------------
    # ----------------------- EVENT HANDLERS -----------------------
    # --------------------------------------------------------------
    """ Method called to handle the click of a node of the graph """
    def clickedNode(self, scatter: pg.ScatterPlotItem, pts):

        self.logger.info("Handling graph node click...")
        data_list = scatter.data.tolist()
        curr_point = [tup for tup in data_list if pts[0] in tup][0]
        mypoint_index = data_list.index(curr_point)

        if mypoint_index == self.selected_idx:
            # The point is already clicked, so remove the visual part
            for i in range(len(scatter.points())):
                scatter.points()[i].setBrush(self.colors[i])
            scatter.points()[mypoint_index].setSize(20)
            self.plot.removeItem(self.display_text)
            self.selected_idx = -1
            self.logger.info("Node " + str(self.data_correspondences[mypoint_index]) + " unselected")
            self.unclicked_signal.emit()

        elif self.selected_idx == -1:
            # No point is clicked, so make it
            for point in scatter.points():
                point.setBrush(QtGui.QBrush(QtGui.QColor(255, 255, 255)))
            self.__selectPoint(scatter, curr_point, mypoint_index)
        else:
            # Another point is selected, so change it
            old_point = scatter.points()[self.selected_idx]
            old_point.setBrush(QtGui.QBrush(QtGui.QColor(255, 255, 255)))
            old_point.setSize(20)
            self.__selectPoint(scatter, curr_point, mypoint_index)

        self.logger.info("Finished handling graph node click")

    """ Method used to select the clicked point in the graph """
    def __selectPoint(self, scatter, curr_point, point_index):
        # Selecting the clicked point
        new_point = scatter.points()[point_index]
        new_point.setBrush(QtGui.QBrush(QtGui.QColor(255, 0, 0)))
        new_point.setSize(25)
        self.display_text.setText(text='x=%f\nY=%f' % (curr_point[0], curr_point[1]))
        self.plot.addItem(self.display_text)
        self.display_text.setPos(curr_point[0], curr_point[1])

        self.selected_idx = point_index
        self.logger.info("Node " + str(self.data_correspondences[point_index]) + " selected")
        self.clicked_signal.emit(self.data_correspondences[point_index])
        self.__setPlotRange(curr_point)

    """ Method used to set the plot ranges to center the view on the selected point """
    def __setPlotRange(self, curr_point):
        # Center left axis range
        self.logger.info("Centering left axis range...")
        left_range = self.plot.getAxis('left').range
        left_centre = (left_range[1] + left_range[0]) / 2.0
        diff_y = left_centre - curr_point[1]
        new_left = [left_range[0] - diff_y, left_range[1] - diff_y]
        ld = pg.LinearRegionItem(new_left)
        self.plot.setYRange(*ld.getRegion(), padding=0)

        # Center bottom axis range
        self.logger.info("Centering bottom axis range...")
        bottom_range = self.plot.getAxis('bottom').range
        bottom_centre = (bottom_range[1] + bottom_range[0]) / 2.0
        diff_x = bottom_centre - curr_point[0]
        new_bottom = [bottom_range[0] - diff_x, bottom_range[1] - diff_x]
        lr = pg.LinearRegionItem(new_bottom)
        self.plot.setXRange(*lr.getRegion(), padding=0)

    """ Key pressed handler: left and right arrows are moved to select the nodes of the graph """
    def keyPressEvent(self, ev):
        if self.selected_idx != -1:
            if ev.key() == QtCore.Qt.Key_Right:
                if self.selected_idx != (self.num_nodes - 1):
                    self.logger.info("Pressed right arrow, moving to next graph node...")
                    pts = list()
                    pts.append(self.pose_graph.scatter.points()[self.selected_idx + 1])
                    self.clickedNode(self.pose_graph.scatter, pts)
            elif ev.key() == QtCore.Qt.Key_Left:
                if self.selected_idx != 0:
                    self.logger.info("Pressed left arrow, moving to previous graph node...")
                    pts = list()
                    pts.append(self.pose_graph.scatter.points()[self.selected_idx - 1])
                    self.clickedNode(self.pose_graph.scatter, pts)
