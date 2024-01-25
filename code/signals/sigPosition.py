from structures.point3d import Point3D


class SigPosition:
    def __init__(self, content: Point3D):
        super().__init__()
        self.__content = content

    @property
    def content(self) -> Point3D:
        """Getter method for the point value."""
        return self.__content