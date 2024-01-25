import logging
import os
from PIL import Image
from structures.model import Model

class Images360Loader:
    def __init__(self, model: Model):
        # Logger setup
        self.logger = logging.getLogger()
        self.logger.info("Creating Image360Loader...")
        self.model = model
        self.logger.info("Finished creating Image360Loader")

    def loadMultipleImages360(self, filenames: list):
        self.logger.info("Loading 360 images...")
        for pair in filenames:
            img360_path = pair[0]
            data_path = pair[1]

            img360 = Image.open(img360_path)
            data_idx = -1

            with open(data_path, 'r') as f:
                data = f.readlines()
                for line in data:
                    words = line.split()

                    if words[0] == "id":
                        data_idx = int(words[1])
                        break

            if data_idx == -1:
                self.logger.info("Skipping 360 image (no data provided)")
                continue

            node = self.model.nodeDic.get(data_idx, -1)
            if type(node) is not int:
                node.img360 = img360

    def loadFromTwo360Folders(self, imgs360_folder: str, data_folder: str):
        self.logger.info("Loading 360 images from folders...")
        img360_list = list()
        imgs360_filenames = sorted([f for f in os.listdir(imgs360_folder) if (f.endswith('.png') or f.endswith('.jpeg'))])
        for filename in imgs360_filenames:
            img360 = Image.open(os.path.join(imgs360_folder, filename))
            img360_list.append(img360)

        data_list = list()
        data_filenames = sorted([f for f in os.listdir(data_folder) if f.endswith('.txt')])
        for filename in data_filenames:
            data_idx = -1
            with open(os.path.join(data_folder, filename), 'r') as f:
                data = f.readlines()
                for line in data:
                    words = line.split()

                    if words[0] == "id":
                        data_idx = int(words[1])
                        break
            data_list.append(data_idx)

        nodes_range = min(len(data_list), len(img360_list), len(self.model.nodes))
        for i in range(nodes_range):
            curr_idx = data_list[i]
            if curr_idx != -1:
                node = self.model.nodeDic.get(curr_idx, -1)
                if type(node) is not int:
                    node.img360 = img360_list[i]

    def loadFromSingle360Folder(self, imgs360_folder: str):
        self.logger.info("Loading 360 images from folder...")
        img360_list = list()
        imgs360_filenames = sorted([f for f in os.listdir(imgs360_folder) if (f.endswith('.png') or f.endswith('.jpeg'))])
        for filename in imgs360_filenames:
            img360 = Image.open(os.path.join(imgs360_folder, filename))
            img360_list.append(img360)

        nodes_range = min(len(img360_list), len(self.model.nodes))
        for i in range(nodes_range):
            node = self.model.nodes[i]
            node.img360 = img360_list[i]
        



###########################################################
################ Orginal version ##########################       
###########################################################


# import logging, os
# from PyQt5 import QtGui
# from structures.model import Model

# # Adding import for Image class
# from PIL import Image


# class Images360Loader:
#     def __init__(self, model: Model):

#         # Logger setup
#         self.logger = logging.getLogger()

#         self.logger.info("Creating Image360Loader...")
#         self.model = model
#         self.logger.info("Finished creating Image360Loader")

#     def loadMultipleImages360(self, filenames: list):

#         self.logger.info("Loading 360 images...")
#         for pair in filenames:
#             img_path = pair[0]
#             data_path = pair[1]

#             # img = QtGui.QPixmap(img_path)
#             # 360 images are of class Image
#             img = Image.open(img_path) 
#             data_idx = -1

#             f = open(data_path, 'r')
#             with f:
#                 data = f.readlines()
#                 for line in data:
#                     words = line.split()

#                     if words[0] == "id":
#                         data_idx = int(words[1])
#                         break

#             if data_idx == -1:
#                 self.logger.info("Skipping 360 image (no data provided)")
#                 continue

#             node = self.model.nodeDic.get(data_idx, -1)
#             if type(node) is not int:
#                 node.img = img

#     def loadFromTwo360Folders(self, imgs360_folder: str, data_folder: str):

#         self.logger.info("Loading 360 images from folders...")
#         img_list = list()
#         imgs_filenames = sorted([f for f in os.listdir(imgs360_folder) if (f.endswith('.png') or f.endswith('.jpeg'))])
#         for filename in imgs_filenames:
#             img = Image(imgs360_folder + '/' + filename)
#             img_list.append(img)

#         data_list = list()
#         data_filenames = sorted([f for f in os.listdir(data_folder) if f.endswith('.txt')])
#         for filename in data_filenames:
#             data_idx = -1
#             f = open(data_folder + "/" + filename, 'r')
#             with f:
#                 data = f.readlines()
#                 for line in data:
#                     words = line.split()

#                     if words[0] == "id":
#                         data_idx = int(words[1])
#                         break
#             data_list.append(data_idx)

#         nodes_range = min(len(data_list), len(img_list), len(self.model.nodes))
#         for i in range(nodes_range):
#             curr_idx = data_list[i]
#             if curr_idx != -1:
#                 node = self.model.nodeDic.get(curr_idx, -1)
#                 if type(node) is not int:
#                     node.img = img_list[i]

#     def loadFromSingle360Folder(self, imgs360_folder: str):

#         self.logger.info("Loading 360 images from folder...")
#         img360_list = list()
#         imgs360_filenames = sorted([f for f in os.listdir(imgs360_folder) if (f.endswith('.png') or f.endswith('.jpeg'))])
#         for filename in imgs360_filenames:
#             img360 = Image.open(imgs360_folder + '/' + filename)
#             img360_list.append(img360)

#         nodes_range = min(len(img360_list), len(self.model.nodes))
#         for i in range(nodes_range):
#             node = self.model.nodes[i]
#             node.img360 = img360_list[i]
