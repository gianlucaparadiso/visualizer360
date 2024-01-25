from typing import Union, List


class SigStringList(list):
    def __init__(self, content: list):
        super().__init__()
        self._content = content

    @property
    def content(self) -> list:
        """Getter method for the string list value."""
        return self._content
