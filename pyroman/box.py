from .element import Element


class Box(Element):
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
        self.box_class = self._params.get(
            'box-class', 'content')
        self.first_indent = self._params.get(
            'first-indent', self.parent.first_indent)

        self._stream = []
        self._font_cache = {}

    def __repr__(self):
        return '<Box [%s] (%i,%i) %ix%i on %s>' % (self.box_class,
                                                   self.x, self.y,
                                                   self.width, self.height,
                                                   str(self.parent))

    # returns a list of orphans (child nodes not fitting into this box)
    def calculate(self):
        current_y = 0
        last_bottom_margin = 0
        last_included = None
        for n, child in enumerate(self.children):
            child.x = child.margin_left
            child.y = current_y + max(last_bottom_margin, child.margin_top)
            child.calculate()  # should pass "obstacles" into this one
            current_y = child.y + child.height
            last_bottom_margin = child.margin_bottom
            if current_y > self.height:
                last_included = n - 1
                break
        if last_included is None:
            return []
        orphans = self.children[last_included:]
        self.children = self.children[:last_included]
        return orphans

    @property
    def dimension(self):
        return (self.width, self.height)

    @dimension.setter
    def dimension(self, dim):
        (width, height) = dim
        self.width = width
        self.height = height
