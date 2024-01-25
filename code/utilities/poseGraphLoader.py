import logging
import math

from structures.model import Model
from structures.node import Node
from structures.edge import Edge
from structures.point3d import Point3D


class PoseGraphLoader:
    def __init__(self, model: Model):

        # Logger setup
        self.logger = logging.getLogger()

        self.logger.info("Creating PoseGraphLoader...")
        self.model = model
        self.logger.info("Finished creating PoseGraphLoader")

    def readFile(self, filename: str):

        self.logger.info("Opening file: " + filename + "...")
        f = open(filename, 'r')
        idx = 0

        with f:
            data = f.readlines()
            for line in data:
                words = line.split()

                # Handle pose node creation
                if words[0] == "VERTEX_SE3:QUAT":
                    new_node = Node()
                    new_node.idx = int(words[1])
                    new_node.pos = Point3D(float(words[2]), float(words[3]), float(words[4]))
                    new_node.quaternion[0] = float(words[5])
                    new_node.quaternion[1] = float(words[6])
                    new_node.quaternion[2] = float(words[7])
                    new_node.quaternion[3] = float(words[8])
                    roll, pitch, yaw = self.quaternionToEuler(float(words[5]), float(words[6]), float(words[7]), float(words[8]))
                    new_node.roll = roll
                    new_node.pitch = pitch
                    new_node.yaw = yaw

                    self.model.addNode(new_node)
                    idx += 1
                    continue

                # Handle edges creation
                if words[0] == "EDGE_SE3:QUAT":
                    new_edge = Edge()
                    new_edge.end = int(words[1])
                    new_edge.start = int(words[2])

                    if self.model.nodeDic.get(new_edge.start, -1) == -1 or self.model.nodeDic.get(new_edge.end, -1) == -1:
                        self.logger.info("Skipping edge " + str(new_edge.start) + " " + str(new_edge.end))
                        continue

                    new_edge.diff_x = float(words[3])
                    new_edge.diff_y = float(words[4])
                    new_edge.diff_z = float(words[5])
                    roll_diff, pitch_diff, yaw_diff = self.quaternionToEuler(float(words[6]), float(words[7]), float(words[8]), float(words[9]))
                    new_edge.diff_roll = roll_diff
                    new_edge.diff_pitch = pitch_diff
                    new_edge.diff_yaw = yaw_diff

                    self.model.addEdge(new_edge)
                    continue

        self.logger.info("Finished opening file")

    """ Method used to convert quaternion to Euler angles """
    def quaternionToEuler(self, x, y, z, w):
        # roll
        sinr_cosp = 2*(w*x + y*z)
        cosr_cosp = 1 - 2*(x*x + y*y)
        roll = math.degrees(math.atan2(sinr_cosp, cosr_cosp))

        # pitch
        sinp = 2*(w*y - z*x)
        if math.fabs(sinp) >= 1:
            pitch = math.degrees(math.copysign(math.pi / 2, sinp))
        else:
            pitch = math.degrees(math.asin(sinp))

        # yaw
        siny_cosp = 2*(w*z + x*y)
        cosy_cosp = 1 - 2*(y*y + z*z)
        yaw = math.degrees(math.atan2(siny_cosp, cosy_cosp))

        return roll, pitch, yaw
