import logging, os
from PyQt5 import QtGui
from structures.model import Model


class ImagesLoader:
    def __init__(self, model: Model):

        # Logger setup
        self.logger = logging.getLogger()

        self.logger.info("Creating ImageLoader...")
        self.model = model
        self.logger.info("Finished creating ImageLoader")

    def loadMultipleImages(self, filenames: list):

        self.logger.info("Loading images...")
        for pair in filenames:
            img_path = pair[0]
            data_path = pair[1]

            img = QtGui.QPixmap(img_path)
            data_idx = -1

            f = open(data_path, 'r')
            with f:
                data = f.readlines()
                for line in data:
                    words = line.split()

                    if words[0] == "id":
                        data_idx = int(words[1])
                        break

            if data_idx == -1:
                self.logger.info("Skipping image (no data provided)")
                continue

            node = self.model.nodeDic.get(data_idx, -1)
            if type(node) is not int:
                node.img = img

    def loadFromTwoFolders(self, imgs_folder: str, data_folder: str):

        self.logger.info("Loading images from folders...")
        img_list = list()
        imgs_filenames = sorted([f for f in os.listdir(imgs_folder) if (f.endswith('.png') or f.endswith('.jpeg'))])
        for filename in imgs_filenames:
            img = QtGui.QPixmap(imgs_folder + '/' + filename)
            img_list.append(img)

        data_list = list()
        data_filenames = sorted([f for f in os.listdir(data_folder) if f.endswith('.txt')])
        for filename in data_filenames:
            data_idx = -1
            f = open(data_folder + "/" + filename, 'r')
            with f:
                data = f.readlines()
                for line in data:
                    words = line.split()

                    if words[0] == "id":
                        data_idx = int(words[1])
                        break
            data_list.append(data_idx)

        nodes_range = min(len(data_list), len(img_list), len(self.model.nodes))
        for i in range(nodes_range):
            curr_idx = data_list[i]
            if curr_idx != -1:
                node = self.model.nodeDic.get(curr_idx, -1)
                if type(node) is not int:
                    node.img = img_list[i]

    def loadFromSingleFolder(self, imgs_folder: str):

        self.logger.info("Loading images from folder...")
        img_list = list()
        imgs_filenames = sorted([f for f in os.listdir(imgs_folder) if (f.endswith('.png') or f.endswith('.jpeg'))])
        for filename in imgs_filenames:
            img = QtGui.QPixmap(imgs_folder + '/' + filename)
            img_list.append(img)

        nodes_range = min(len(img_list), len(self.model.nodes))
        for i in range(nodes_range):
            node = self.model.nodes[i]
            node.img = img_list[i]
