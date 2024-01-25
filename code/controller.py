import sys, logging
from PyQt5 import QtWidgets, QtCore
from open3d import io
from graphics.mainWindow import MainWindow
from signals.sigString import SigString
from signals.sigStringList import SigStringList
from structures.model import Model
from utilities.poseGraphLoader import PoseGraphLoader
from utilities.pointCloudsLoader import PointCloudsLoader
from utilities.imagesLoader import ImagesLoader

from utilities.images360Loader import Images360Loader


class Controller(QtCore.QObject):
    def __init__(self):
        super().__init__()

        self.app = QtWidgets.QApplication(sys.argv)
        screen = self.app.primaryScreen()
        self.view = MainWindow(screen.size())

        self.view.pg_filename_signal.connect(self.pgFileReadSignal)

        self.view.multi_pcs_signal.connect(self.pcFilesReadSignal)
        self.view.two_folders_pcs_signal.connect(self.pcFoldersReadSignal)
        self.view.single_folder_pcs_signal.connect(self.loadSingleFolderPCs)

        self.view.multi_imgs_signal.connect(self.loadMultiImages)
        self.view.two_folders_imgs_signal.connect(self.loadTwoFoldersImages)
        self.view.single_folder_imgs_signal.connect(self.loadSingleFolderImages)

        # Adding 360 image loading connection
        self.view.multi_imgs360_signal.connect(self.loadMultiImages360)
        self.view.two_folders_imgs360_signal.connect(self.loadTwoFoldersImages360)
        self.view.single_folder_imgs360_signal.connect(self.loadSingleFolderImages360)

        self.view.clean_pose_graph_signal.connect(self.cleanModel)
        self.view.clean_point_clouds_signal.connect(self.cleanPointClouds)
        self.view.clean_images_signal.connect(self.cleanImages)

        # Add clean connection
        self.view.clean_images360_signal.connect(self.cleanImages360)

        self.view.selected_pose_signal.connect(self.displayPoseInfo)

        self.model = Model()
        self.pose_graph_loader = PoseGraphLoader(self.model)
        self.point_clouds_loader = PointCloudsLoader(self.model)
        self.images_loader = ImagesLoader(self.model)

        # Add 360 image loader
        self.images360_loader = Images360Loader(self.model)

    def run(self):
        self.view.show()
        return self.app.exec_()

    # --------------------------------------------------------------
    # -------------------------- RECEIVERS -------------------------
    # --------------------------------------------------------------

    @QtCore.pyqtSlot(SigString)
    def pgFileReadSignal(self, pg_filename: SigString):
        self.pose_graph_loader.readFile(pg_filename.content)

        if len(self.model.nodes) != 0:
            self.view.drawPoseGraph(self.model.nodeDic, self.model.edges)
            self.view.load_pcs_action.setDisabled(False)
            self.view.load_images_action.setDisabled(False)
            # Unlock 360 image loading button after pg is loaded
            self.view.load_images360_action.setDisabled(False)

    @QtCore.pyqtSlot(SigStringList)
    def pcFilesReadSignal(self, pc_filenames: SigStringList):
        self.point_clouds_loader.readFromMultipleFiles(pc_filenames.content)
        self.view.drawPointClouds(self.model.nodes)

    @QtCore.pyqtSlot(SigStringList)
    def pcFoldersReadSignal(self, pc_folders: SigStringList):
        self.point_clouds_loader.readFromTwoFolders(pc_folders.content[0][0], pc_folders.content[0][1])
        self.view.drawPointClouds(self.model.nodes)

    @QtCore.pyqtSlot(SigString)
    def loadSingleFolderPCs(self, folder_filepath: SigString):
        self.point_clouds_loader.loadFromSingleFolder(folder_filepath.content)
        self.view.drawPointClouds(self.model.nodes)

    @QtCore.pyqtSlot(SigStringList)
    def loadMultiImages(self, images_filenames: SigStringList):
        self.images_loader.loadMultipleImages(images_filenames.content)
        self.view.imagesLoaded(self.model.nodes)

    @QtCore.pyqtSlot(SigStringList)
    def loadTwoFoldersImages(self, folders_filepaths: SigStringList):
        self.images_loader.loadFromTwoFolders(folders_filepaths.content[0][0], folders_filepaths.content[0][1])
        self.view.imagesLoaded(self.model.nodes)

    @QtCore.pyqtSlot(SigString)
    def loadSingleFolderImages(self, folder_filepath: SigString):
        self.images_loader.loadFromSingleFolder(folder_filepath.content)
        self.view.imagesLoaded(self.model.nodes)

    # Add recivers for 360 images
    @QtCore.pyqtSlot(SigStringList)
    def loadMultiImages360(self, images360_filenames: SigStringList):
        self.images360_loader.loadMultipleImages360(images360_filenames.content)
        self.view.images360Loaded(self.model.nodes)

    @QtCore.pyqtSlot(SigStringList)
    def loadTwoFoldersImages360(self, folders360_filepaths: SigStringList):
        self.images360_loader.loadFromTwo360Folders(folders360_filepaths.content[0][0], folders360_filepaths.content[0][1])
        self.view.images360Loaded(self.model.nodes)

    @QtCore.pyqtSlot(SigString)
    def loadSingleFolderImages360(self, folder360_filepath: SigString):
        self.images360_loader.loadFromSingle360Folder(folder360_filepath.content)
        self.view.images360Loaded(self.model.nodes)

    @QtCore.pyqtSlot(int)
    def displayPoseInfo(self, pose_idx: int):
        self.view.displayNodeInfo(self.model.nodeDic[pose_idx])

    @QtCore.pyqtSlot()
    def cleanModel(self):
        self.model.resetModel()

    @QtCore.pyqtSlot()
    def cleanPointClouds(self):
        for node in self.model.nodes:
            if node.cloud is not None:
                node.cloud = None

    @QtCore.pyqtSlot()
    def cleanImages(self):
        for node in self.model.nodes:
            if node.img is not None:
                node.img = None

    # Add receiver for cleaning 360 images
    @QtCore.pyqtSlot()
    def cleanImages360(self):
        for node in self.model.nodes:
            if node.img is not None:
                node.img = None