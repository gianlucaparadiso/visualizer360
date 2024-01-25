class Point3D:
    """
    The class describes a 3D points with its coordinates: x, y and z.

    Attributes
    ----------
    __x : float
        x coordinate of the 3D point
    __y : float
        y coordinate of the 3D point
    __z : float
        z coordinate of the 3D point

    Methods
    -------
    x(self) : float
        Returns the x coordinate
    y(self) : float
        Returns the y coordinate
    z(self) : float
        Returns the z coordinate

    """

    def __init__(self, x: float, y: float, z: float):
        self._x = x
        self._y = y
        self._z = z

    @property
    def x(self) -> float:
        """Getter method for coordinate x."""
        return self._x

    @property
    def y(self) -> float:
        """Getter method for coordinate y."""
        return self._y

    @property
    def z(self) -> float:
        """Getter method for coordinate z."""
        return self._z

    @x.setter
    def x(self, value: float):
        """Setter method for coordinate x"""
        self._x = value

    @y.setter
    def y(self, value: float):
        """Setter method for coordinate y"""
        self._y = value

    @z.setter
    def z(self, value: float):
        """Setter method for coordinate z"""
        self._z = value
