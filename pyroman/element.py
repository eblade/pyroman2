class Element:
    def __init__(self, doc=None, parent=None, params={}):
        self.doc = doc
        self.parent = parent or doc
        self.children = []
        self.width = 0
        self.height = 0
        self.x = 0
        self.y = 0
        self._rendered = 0
        self._params = params
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
    def position(self):
        return self.x, self.y

    @position.setter
    def position(self, pos):
        (x, y) = pos
        self.x = x
        self.y = y

    @property
    def absolute_position(self):
        if self.parent is None:
            return self.position
        else:
            px, py = self.parent.absolute_position
            return px + self.x, py + self.y

    @property
    def dimension(self):
        return (self.width, self.height)

    @property
    def margin(self):
        return (self.margin_top, self.margin_right, self.margin_bottom, self.margin_left)

    @margin.setter
    def margin(self, margin):
        self.margin_top, self.margin_right, self.margin_bottom, self.margin_left = margin

    def append(self, obj):
        self.children.append(obj)

    def copy(self):
        a = self.__class__()
        a.__dict__ = self.__getstate__()
        return a

    # to make it picklable
    def __getstate__(self):
        odict = self.__dict__.copy()
        odict['class'] = self.__class__.__name__
        internals = [k for k in odict.keys() if k.startswith('_')]
        for k in internals:
            del odict[k]
        del odict['doc']
        del odict['parent']
        if 'parameters' in odict:
            del odict['parameters']
        return odict
