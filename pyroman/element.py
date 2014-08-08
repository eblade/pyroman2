class Element:
    def __init__(self, doc=None, parent=None, params={}):
        self.doc = doc
        self.parent = parent or doc
        self._children = []
        self._local = params
        self._width = 0
        self._height = 0
        self._rendered = 0
        self._params = params
        self.position = (0, 0) 
        self.margin_top = 0
        self.margin_bottom = 0
        self.margin_left = 0
        self.margin_right = 0
        self.label = None
        self.label_class = None
        self.init()

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

    @property
    def position(self):
        return self._position

    @x.setter
    def x(self, x):
        self._position = (x, self._position[1])

    @y.setter
    def y(self, y):
        self._position = (self._position[0], y)

    @position.setter
    def position(self, pos):
        (x, y) = pos
        self._position = (x, y)

    def append(self, obj):
        self._children.append(obj)

    def serialize(self, options={}):
        return {
            'class': self.__class__.__name__,
            'children': [x.serialize() for x in self._children],
            #'local': self._local,
            'width': self._width,
            'height': self._height,
            'rendered': self._rendered,
            #'params': self._params,
            'position': self.position,
            'margin_top': self.margin_top,
            'margin_bottom': self.margin_bottom,
            'margin_left': self.margin_left,
            'margin_right': self.margin_right,
            'label': self.label,
            'label_class': self.label_class,
        }
