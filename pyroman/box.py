from .element import Element
from .constants import *

class Box(Element):
    def init(self):
        self.word_wrap = self._params.get('word-wrap', self.parent.word_wrap)
        self.font_family = self._params.get('font-family', self.parent.font_family)
        self.font_size = self._params.get('font-size', self.parent.font_size)
        self.text_color = self._params.get('text-color', self.parent.text_color)
        self.align = self._params.get('align', self.parent.align)
        self.content = self._params.get('content', '')
        self.max_width = self._params.get('max-width', self.parent.width)
        self.max_height = self._params.get('max-height', self.parent.height)
        self.line_height = self._params.get('line-height', self.parent.line_height)
        self.space_width = self._params.get('space-width', self.parent.space_width)
        self.box_class = self._params.get('box-class', 'content')

        self._stream = []
        self._font_cache = {}

    def __repr__(self):
        return '<Box [%s] (%ix%i) @(%i, %i) on %s>' % (self.box_class, self.width, self.height, self.x, self.y, str(self.parent))

    # returns a list of orphans (child nodes not fitting into this box)
    def calculate(self):
        current_y = 0
        last_bottom_margin = 0
        orphans = []
        for child in self.children:
            child.x = child.margin_left
            child.y = current_y + max(last_bottom_margin, child.margin_top)
            child.calculate() # should pass "obstacles" into this one
            current_y += child.height
            last_bottom_margin = child.margin_bottom
        return orphans

    @property
    def dimension(self):
        return (self.width, self.height)

    @dimension.setter
    def dimension(self, dim):
        (width, height) = dim
        self.width = width
        self.height = height

