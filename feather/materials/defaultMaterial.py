from feather.materials import ColorMaterial

class DefaultMaterial(ColorMaterial):
    def __init__(self):
        super().__init__(255.0 / 255.0, 0.0, 203.0 / 255.0)