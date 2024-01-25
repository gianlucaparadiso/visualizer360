from structures.point3d import Point3D


class Edge:
    def __init__(self):
        self._start = 0
        self._end = 0

        self._diff_x = 0.0
        self._diff_y = 0.0
        self._diff_z = 0.0

        self._diff_roll = 0.0
        self._diff_pitch = 0.0
        self._diff_yaw = 0.0

    @property
    def start(self) -> int:
        return self._start

    @property
    def end(self) -> int:
        return self._end

    @property
    def diff_x(self) -> float:
        return self._diff_x

    @property
    def diff_y(self) -> float:
        return self._diff_y

    @property
    def diff_z(self) -> float:
        return self._diff_z

    @property
    def diff_roll(self) -> float:
        return self._diff_roll

    @property
    def diff_pitch(self) -> float:
        return self._diff_pitch

    @property
    def diff_yaw(self) -> float:
        return self._diff_yaw

    @start.setter
    def start(self, value: int):
        self._start = value

    @end.setter
    def end(self, value: int):
        self._end = value

    @diff_x.setter
    def diff_x(self, value: float):
        self._diff_x = value

    @diff_y.setter
    def diff_y(self, value: float):
        self._diff_y = value

    @diff_z.setter
    def diff_z(self, value: float):
        self._diff_z = value

    @diff_roll.setter
    def diff_roll(self, value: float):
        self._diff_roll = value

    @diff_pitch.setter
    def diff_pitch(self, value: float):
        self._diff_pitch = value

    @diff_yaw.setter
    def diff_yaw(self, value: float):
        self._diff_yaw = value

    def printEdge(self):
        print("Start:\t", self._start)
        print("End:\t", self._end)
        print("Pos. diff: \t", self._diff_x, self._diff_y, self._diff_z)
        print("Roll:\t", self._diff_roll)
        print("Pitch:\t", self._diff_pitch)
        print("Yaw:\t", self._diff_yaw)