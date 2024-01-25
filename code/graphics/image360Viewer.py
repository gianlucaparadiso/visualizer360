import logging
from OpenGL.GL import *
from OpenGL.GLU import *
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtOpenGL import QGLWidget
from PIL import Image

class GLWidget(QGLWidget):

    leftMouseButtonPressed = QtCore.pyqtSignal(float, float)
    leftMouseButtonReleased = QtCore.pyqtSignal(float, float)
    

    def __init__(self):
        super().__init__()
        self.images = dict()

        # Default image is just a blank gray image
        self.default_image = Image.open("./icons/gray.jpg")
        self.image = self.default_image

        self.image_width, self.image_height = self.image.size
        self.yaw = 0
        self.pitch = 0
        self.prev_dx = 0
        self.prev_dy = 0
        self.fov = 90   
        self.moving = False

        # Store a local handle to the scene's current image pixmap.
        self._360Handle = False


    def initializeGL(self):
        glEnable(GL_TEXTURE_2D)
        self.texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, self.image_width, self.image_height, 0, GL_RGB, GL_UNSIGNED_BYTE, self.image.tobytes())
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        self.sphere = gluNewQuadric()
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(90, self.width()/self.height(), 0.1, 1000)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPushMatrix()
        glRotatef(self.pitch, 1, 0, 0)
        glRotatef(self.yaw, 0, 1, 0)
        glRotatef(90, 1, 0, 0)
        glRotatef(-90, 0, 0, 1)
        gluQuadricTexture(self.sphere, True)
        gluSphere(self.sphere, 1, 100, 100)
        glPopMatrix()
          
    def resizeGL(self, width, height):
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(self.fov, self.width()/self.height(), 0.1, 1000)
        
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.mouse_x, self.mouse_y = event.pos().x(), event.pos().y()
            self.moving = True

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.moving = False
            

    def mouseMoveEvent(self, event):
        if self.moving:
            dx = event.pos().x() - self.mouse_x 
            dy = event.pos().y() - self.mouse_y
            dx *= 0.1
            dy *= 0.1
            self.yaw -= dx
            self.pitch -= dy
            self.pitch = min(max(self.pitch, -90), 90)
            self.mouse_x, self.mouse_y = event.pos().x(), event.pos().y()
            self.update()

    def wheelEvent(self, event):
        delta = event.angleDelta().y()
        self.fov -= delta * 0.1
        self.fov = max(30, min(self.fov, 90))
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(self.fov, self.width()/self.height(), 0.1, 1000)
        self.update()



    def hasImage360(self):
        """ Returns whether or not the scene contains an image.
        """
        return self._360Handle

    def clearImage360(self):
        """ Removes the current image from the scene if it exists.
        """
        if self.hasImage360():
            self.setImage360(self.default_image)
            # self.image = self.default_image
            # self.image_width, self.image_height = self.image.size
            # glBindTexture(GL_TEXTURE_2D, self.texture)
            # glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, self.image_width, self.image_height, 0, GL_RGB, GL_UNSIGNED_BYTE, self.image.tobytes())
            # self.update()
            # self._360Handle = False

    def setImage360(self, set_image):
        """ Set the scene's current image to input image
        """
        self.image = set_image
        self.image_width, self.image_height = self.image.size
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, self.image_width, self.image_height, 0, GL_RGB, GL_UNSIGNED_BYTE, self.image.tobytes())
        self.update()
        if set_image == self.default_image:
            self._360Handle = False
        else:
            self._360Handle = True

    def setDefaultImage360(self):
        self.setImage360(self.default_image)

    def setImage360ByIndex(self, key):
        if key in self.images:
            self.setImage360(self.images[key])

    def cleanViewer360(self):
        self.clearImage360()
        self.images.clear()



