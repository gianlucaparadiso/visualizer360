class SigString(str):
    def __init__(self, content: str):
        super().__init__()
        self.__content = content

    @property
    def content(self) -> str:
        """Getter method for the string value."""
        return self.__content
