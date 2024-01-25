from PyQt5 import QtWidgets


""" Class representing the widget displaying all the data information """
class PoseInfoForm(QtWidgets.QGroupBox):
    def __init__(self):
        super().__init__()

        self.layout = QtWidgets.QFormLayout()
        sp = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)

        self.x_text = QtWidgets.QTextEdit("")
        self.x_text.setDisabled(True)
        self.x_text.setSizePolicy(sp)
        self.x_text.setMaximumSize(100, 20)
        self.layout.addRow(QtWidgets.QLabel("x[m]:"), self.x_text)

        self.y_text = QtWidgets.QTextEdit("")
        self.y_text.setDisabled(True)
        self.y_text.setSizePolicy(sp)
        self.y_text.setMaximumSize(100, 20)
        self.layout.addRow(QtWidgets.QLabel("y[m]:"), self.y_text)

        self.z_text = QtWidgets.QTextEdit("")
        self.z_text.setDisabled(True)
        self.z_text.setSizePolicy(sp)
        self.z_text.setMaximumSize(100, 20)
        self.layout.addRow(QtWidgets.QLabel("z[m]:"), self.z_text)

        self.roll_text = QtWidgets.QTextEdit("")
        self.roll_text.setDisabled(True)
        self.roll_text.setSizePolicy(sp)
        self.roll_text.setMaximumSize(100, 20)
        self.layout.addRow(QtWidgets.QLabel("roll[deg]:"), self.roll_text)

        self.pitch_text = QtWidgets.QTextEdit("")
        self.pitch_text.setDisabled(True)
        self.pitch_text.setSizePolicy(sp)
        self.pitch_text.setMaximumSize(100, 20)
        self.layout.addRow(QtWidgets.QLabel("pitch[deg]:"), self.pitch_text)

        self.yaw_text = QtWidgets.QTextEdit("")
        self.yaw_text.setDisabled(True)
        self.yaw_text.setSizePolicy(sp)
        self.yaw_text.setMaximumSize(100, 20)
        self.layout.addRow(QtWidgets.QLabel("yaw[deg]:"), self.yaw_text)

        self.xq_text = QtWidgets.QTextEdit("")
        self.xq_text.setDisabled(True)
        self.xq_text.setSizePolicy(sp)
        self.xq_text.setMaximumSize(100, 20)
        self.layout.addRow(QtWidgets.QLabel("xq:"), self.xq_text)

        self.yq_text = QtWidgets.QTextEdit("")
        self.yq_text.setDisabled(True)
        self.yq_text.setSizePolicy(sp)
        self.yq_text.setMaximumSize(100, 20)
        self.layout.addRow(QtWidgets.QLabel("yq:"), self.yq_text)

        self.zq_text = QtWidgets.QTextEdit("")
        self.zq_text.setDisabled(True)
        self.zq_text.setSizePolicy(sp)
        self.zq_text.setMaximumSize(100, 20)
        self.layout.addRow(QtWidgets.QLabel("zq:"), self.zq_text)

        self.wq_text = QtWidgets.QTextEdit("")
        self.wq_text.setDisabled(True)
        self.wq_text.setSizePolicy(sp)
        self.wq_text.setMaximumSize(100, 20)
        self.layout.addRow(QtWidgets.QLabel("zq:"), self.wq_text)

        self.cloud_text = QtWidgets.QTextEdit("")
        self.cloud_text.setDisabled(True)
        self.cloud_text.setSizePolicy(sp)
        self.cloud_text.setMaximumSize(100, 20)
        self.layout.addRow(QtWidgets.QLabel("Cloud size:"), self.cloud_text)

        self.cloud_xrange_text = QtWidgets.QTextEdit("")
        self.cloud_xrange_text.setDisabled(True)
        self.cloud_xrange_text.setSizePolicy(sp)
        self.cloud_xrange_text.setMaximumSize(100, 20)
        self.layout.addRow(QtWidgets.QLabel("Cloud x range:"), self.cloud_xrange_text)

        self.cloud_yrange_text = QtWidgets.QTextEdit("")
        self.cloud_yrange_text.setDisabled(True)
        self.cloud_yrange_text.setSizePolicy(sp)
        self.cloud_yrange_text.setMaximumSize(100, 20)
        self.layout.addRow(QtWidgets.QLabel("Cloud y range:"), self.cloud_yrange_text)

        self.cloud_zrange_text = QtWidgets.QTextEdit("")
        self.cloud_zrange_text.setDisabled(True)
        self.cloud_zrange_text.setSizePolicy(sp)
        self.cloud_zrange_text.setMaximumSize(100, 20)
        self.layout.addRow(QtWidgets.QLabel("Cloud z range:"), self.cloud_zrange_text)

        self.image_text = QtWidgets.QTextEdit("")
        self.image_text.setDisabled(True)
        self.image_text.setSizePolicy(sp)
        self.image_text.setMaximumSize(100, 20)
        self.layout.addRow(QtWidgets.QLabel("Image size:"), self.image_text)

        # Add size display for 360 image
        self.image360_text = QtWidgets.QTextEdit("")
        self.image360_text.setDisabled(True)
        self.image360_text.setSizePolicy(sp)
        self.image360_text.setMaximumSize(100, 20)
        self.layout.addRow(QtWidgets.QLabel("Image 360 size:"), self.image360_text)

        self.setLayout(self.layout)

    def clearText(self):
        self.x_text.clear()
        self.y_text.clear()
        self.z_text.clear()
        self.roll_text.clear()
        self.pitch_text.clear()
        self.yaw_text.clear()
        self.xq_text.clear()
        self.yq_text.clear()
        self.zq_text.clear()
        self.wq_text.clear()
        self.cloud_text.clear()
        self.cloud_xrange_text.clear()
        self.cloud_yrange_text.clear()
        self.cloud_zrange_text.clear()
        self.image_text.clear()
        # Add clear method for image360_text
        self.image360_text.clear()

    def setText(self, x: float, y: float, z: float, roll: float, pitch: float, yaw: float, quaternion, cloud, img, img360):
        self.x_text.setText(str(x))
        self.y_text.setText(str(y))
        self.z_text.setText(str(z))
        self.roll_text.setText(str(roll))
        self.pitch_text.setText(str(pitch))
        self.yaw_text.setText(str(yaw))
        self.xq_text.setText(str(quaternion[0]))
        self.yq_text.setText(str(quaternion[1]))
        self.zq_text.setText(str(quaternion[2]))
        self.wq_text.setText(str(quaternion[3]))

        if cloud is not None:
            self.cloud_text.setText(str(len(cloud.points)))
            max_bounds = list(cloud.get_max_bound())
            min_bounds = list(cloud.get_min_bound())
            max_bounds = [round(num, 1) for num in max_bounds]
            min_bounds = [round(num, 1) for num in min_bounds]

            self.cloud_xrange_text.setText(str([min_bounds[0], max_bounds[0]]))
            self.cloud_yrange_text.setText(str([min_bounds[1], max_bounds[1]]))
            self.cloud_zrange_text.setText(str([min_bounds[2], max_bounds[2]]))
        else:
            self.cloud_text.setText("NaN")
            self.cloud_xrange_text.setText("NaN")
            self.cloud_yrange_text.setText("NaN")
            self.cloud_zrange_text.setText("NaN")

        if cloud is not None:
            self.cloud_text.setText(str(len(cloud.points)))
        else:
            self.cloud_text.setText("NaN")

        if img is not None:
            self.image_text.setText(str(img.size().width()) + "x" + str(img.size().height()))
        else:
            self.image_text.setText("NaN")
        
        # Add case for 360 image
        if img360 is not None:
            self.image360_text.setText(str(img360.size[0]) + "x" + str(img360.size[1]))
        else:
            self.image360_text.setText("NaN")
