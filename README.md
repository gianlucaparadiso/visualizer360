# SLAM Data Visualization Tool

This repository hosts the Python code for a versatile Qt5 application designed for visualizing SLAM (Simultaneous Localization and Mapping) data. Our tool provides an intuitive interface for interacting with both 2D and 3D representations of pose graphs, along with the integration of LiDAR point clouds and various image formats including 360° panoramic views. It's an essential tool for researchers, engineers, and enthusiasts working in robotics, autonomous vehicles, and related fields to analyze and interpret SLAM data efficiently.

## Features

- **2D Pose Graph Visualization**: Navigate through a 2D representation of the pose graph.

- **3D Pose Graph and Point Cloud Visualization**: Dive into a 3D view of the pose graph and associated LiDAR point clouds.

- **Planar Image Visualization**: Associated edge images in the pose graph can be viewed in a dedicated widget.

- **360° Image Visualization**: Experience a street-view-like presentation of 360° images with an OpenGL widget.

## Getting Started

### Prerequisites

Ensure you have Python and the necessary Qt5 libraries installed on your system. 

### Installation

Clone this repository:
```
git clone https://github.com/gianlucaparadiso/visualizer360.git
```

### Launching the Application

1. Navigate to the cloned directory:
```
cd /path/to/folder/visualizer360/code
```

2. To start the application, run the following command in your terminal:
```
python launch.py
```

## Usage

- **2D Pose Graph Navigation**: Use the keyboard arrow keys to move along the trajectory in the 2D pose graph widget.

- **3D Interaction**: In the 3D widget, use your mouse to zoom, rotate, and pan across the 3D space.

- **Image Exploration**: Utilize mouse actions in the image and 360° image widgets to zoom and navigate through visual data.
