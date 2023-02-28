from feather.shapes.rectangle import Rectangle

class Screen(Rectangle):
    def __init__(self, name):
        super().__init__(name, True, None)
