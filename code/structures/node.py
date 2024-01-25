from structures.point3d import Point3D
import numpy as np
import open3d as o3d
from PyQt5 import QtGui

# Add the include for Image class
from PIL import Image

class Node:
    def __init__(self):

        self._pos = None

        self._roll = 0.0
        self._pitch = 0.0
        self._yaw = 0.0

        self.quaternion = np.empty([4])

        self._idx = 0

        self._img = None
        
        # Add new attribute for 360 imgs
        self._img360 = None

        self._cloud = None

        self._posref2d = None
        self._posref3d = None

    @property
    def pos(self) -> Point3D:
        """Getter method for node position (x,y,z)."""
        return self._pos

    @property
    def roll(self) -> float:
        return self._roll

    @property
    def pitch(self) -> float:
        return self._pitch

    @property
    def yaw(self) -> float:
        return self._yaw

    @property
    def idx(self) -> int:
        return self._idx

    @property
    def img(self) -> QtGui.QPixmap:
        return self._img
    
    # Define property for 360 imgs
    @property
    def img360(self) -> Image:
        return self._img360

    @property
    def cloud(self) -> o3d.geometry.PointCloud:
        return self._cloud

    @pos.setter
    def pos(self, value: Point3D):
        self._pos = value

    @roll.setter
    def roll(self, value: float):
        self._roll = value

    @pitch.setter
    def pitch(self, value: float):
        self._pitch = value

    @yaw.setter
    def yaw(self, value: float):
        self._yaw = value

    @idx.setter
    def idx(self, value):
        self._idx = value

    @img.setter
    def img(self, value):
        self._img = value

    # Define setter method for 360 imgs
    @img360.setter
    def img360(self, value):
        self._img360 = value

    @cloud.setter
    def cloud(self, value):
        self._cloud = value

    def printNode(self):
        print("Index:\t", self._idx)
        print("Pose:\t", self._pos._x, self._pos._y, self._pos._z)
        print("Roll:\t", self._roll)
        print("Pitch:\t", self._pitch)
        print("Yaw:\t", self._yaw)



