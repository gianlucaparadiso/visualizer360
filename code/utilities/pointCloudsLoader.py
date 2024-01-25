import logging, os
from scipy.spatial.transform import Rotation as R
import numpy as np
from structures.model import Model
import open3d as o3d


class PointCloudsLoader:
    def __init__(self, model: Model):
        logging.basicConfig(level=logging.INFO)

        # Logger setup
        self.logger = logging.getLogger()

        self.logger.info("Creating PointCloudsLoader...")
        self.model = model
        self.logger.info("Finished creating PointCloudsLoader")

    def readFromMultipleFiles(self, filenames: list):
        self.logger.info("Loading point clouds...")
        for pair in filenames:
            pc_path = pair[0]
            data_path = pair[1]

            pcd: o3d.geometry.PointCloud = o3d.io.read_point_cloud(pc_path)
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
                self.logger.info("Skipping point cloud (no data provided)")
                continue

            node = self.model.nodeDic.get(data_idx, -1)
            if type(node) is not int:
                quaternion = node.quaternion
                rotation = R.from_quat(quaternion).as_matrix()
                transform = np.identity(4, dtype=np.float64)
                transform[0:3, 0:3] = rotation
                transform[0, 3] = node.pos.x
                transform[1, 3] = node.pos.y
                transform[2, 3] = node.pos.z
                new_cloud = pcd.transform(transform)
                node.cloud = new_cloud

    def readFromTwoFolders(self, cloud_folder: str, data_folder: str):
        self.logger.info("Loading point clouds from folders...")
        pcd_list = list()
        pcd_filenames = sorted([f for f in os.listdir(cloud_folder) if f.endswith('.pcd')])
        for filename in pcd_filenames:
            pcd: o3d.geometry.PointCloud = o3d.io.read_point_cloud(cloud_folder + "/" + filename)
            pcd_list.append(pcd)

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

        nodes_range = min(len(data_list), len(pcd_list), len(self.model.nodes))
        for i in range(nodes_range):
            curr_idx = data_list[i]
            if curr_idx != -1:
                node = self.model.nodeDic.get(curr_idx, -1)
                if type(node) is not int:
                    quaternion = node.quaternion
                    rotation = R.from_quat(quaternion).as_matrix()
                    transform = np.identity(4, dtype=np.float64)
                    transform[0:3, 0:3] = rotation
                    transform[0, 3] = node.pos.x
                    transform[1, 3] = node.pos.y
                    transform[2, 3] = node.pos.z
                    new_cloud = pcd_list[i].transform(transform)
                    node.cloud = new_cloud

    def loadFromSingleFolder(self, cloud_folder: str):
        self.logger.info("Loading point clouds from folder...")
        pcd_list = list()
        pcd_filenames = sorted([f for f in os.listdir(cloud_folder) if f.endswith('.pcd')])
        for filename in pcd_filenames:
            pcd: o3d.geometry.PointCloud = o3d.io.read_point_cloud(cloud_folder + "/" + filename)
            pcd_list.append(pcd)

        nodes_range = min(len(pcd_list), len(self.model.nodes))
        for i in range(nodes_range):
            node = self.model.nodes[i]
            quaternion = node.quaternion
            rotation = R.from_quat(quaternion).as_matrix()
            transform = np.identity(4, dtype=np.float64)
            transform[0:3, 0:3] = rotation
            transform[0, 3] = node.pos.x
            transform[1, 3] = node.pos.y
            transform[2, 3] = node.pos.z
            new_cloud = pcd_list[i].transform(transform)
            node.cloud = new_cloud
