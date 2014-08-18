from .element import Element


class Construct(Element):
    def init(self):
        self.word_wrap = self._params.get(
            'word-wrap', self.parent.word_wrap)
        self.font_family = self._params.get(
            'font-family', self.parent.font_family)
        self.font_style = self._params.get(
            'font-style', self.parent.font_style)
        self.font_size = self._params.get(
            'font-size', self.parent.font_size)
        self.text_color = self._params.get(
            'text-color', self.parent.text_color)
        self.align = self._params.get(
            'align', self.parent.align)
        self.content = self._params.get(
            'content', '')
        self.max_width = self._params.get(
            'max-width', self.parent.width)
        self.max_height = self._params.get(
            'max-height', self.parent.height)
        self.line_height = self._params.get(
            'line-height', self.parent.line_height)
        self.space_width = self._params.get(
            'space-width', self.parent.space_width)
        self.first_indent = self._params.get(
            'first-indent', self.parent.first_indent)
        self.min_after = self._params.get(
            'min-after', 0)
        self.no_split = self._params.get(
            'no-split', True)

        self._stream = []
        self._font_cache = {}

    def __repr__(self):
        return '<Construct (%i,%i) %ix%i>' % (self.x, self.y,
                                              self.width, self.height)

    def calculate(self):
        current_y = 0
        last_bottom_margin = 0
        self.width = self.parent.width - self.margin_left - self.margin_right
        for child in self.children:
            print("Calculating " + str(child))
            child.x = child.margin_left
            child.y = current_y + max(last_bottom_margin, child.margin_top)
            child.max_width = self.width - child.margin_left - child.margin_right
            child.calculate()  # should pass "obstacles" into this one
            current_y = child.y + child.height
            last_bottom_margin = child.margin_bottom
            print("Calculated " + str(child))

    @property
    def dimension(self):
        return (self.width, self.height)

    @dimension.setter
    def dimension(self, dim):
        (width, height) = dim
        self.width = width
        self.height = height

    # we don't split basic boxes, but subclasses may override this
    def split(self, height_left):
        return None
