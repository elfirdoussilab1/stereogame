from feather import Program


class ShaderMaterial(Program):
    def __init__(self, vertexPath, fragmentPath):
        with open(vertexPath, 'r') as file:
            vs_tx = file.read()

        with open(fragmentPath, 'r') as file:
            fs_tx = file.read()

        super().__init__(vs_tx, fs_tx)

        self.updateFunction = lambda self: None

    def setUpdateFunction(self, updateFunction):
        self.updateFunction = updateFunction

    def update(self):
        self.updateFunction(self)
