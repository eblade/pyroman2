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
        self.max_width = self._params.get('max-width', self.parent.max_width)
        self.max_height = self._params.get('max-height', self.parent.max_height)
        self.line_height = self._params.get('line-height', self.parent.line_height)
        self.space_width = self._params.get('space-width', self.parent.space_width)

        self._stream = []
        self._font_cache = {}
