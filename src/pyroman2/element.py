

class Element:
    def __init__(self, doc, params={}):
        self._doc = doc
        self._children = []
        self._local = params
        self._width = 0
        self._height = 0
        self._rendered = 0
        self.position = (0, 0) 
        self.margin_top = 0
        self.margin_bottom = 0
        self.margin_left = 0
        self.margin_right = 0
        self.label = None
        self.label_class = None

    def init(self):
        pass

    def render(self):
        self._rendered = True

    def calculate(self):
        pass

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def x(self):
        return self._position[0]

    @property
    def y(self):
        return self._position[1]

    @x.setter(self, x)
    def x(self, x):
        self._position = (x, self._position[1])

    @y.setter(self, y)
    def y(self, y):
        self._position = (self._position[0], y)
