from PIL import ImageFont

from .element import Element
from .parameters import Parameters
from .constants import *

class Document(Element):
    def __init__(self, params={}):
        super().__init__(params=params)

    def init(self):
        self.parameters = Parameters()
        all_params = self.parameters.get_defaults()
        all_params.update(self._params)
        self._params = all_params

        self.word_wrap = self._params.get('word-wrap')
        self.font_family = self._params.get('font-family')
        self.font_size = self._params.get('font-size')
        self.text_color = self._params.get('text-color')
        self.align = self._params.get('align')
        self.content = self._params.get('content', '')
        self.width = self._params.get('width')
        self.height = self._params.get('height')
        self.line_height = self._params.get('line-height')
        self.space_width = self._params.get('space-width')

        self._font_cache = {}

    def get_font(self, font_family, font_size):
        key = '%s-%i' % (font_family, font_size)
        font = self._font_cache.get(key, None)
        if font is None:
            font = ImageFont.truetype('%s.ttf' % font_family, font_size)
            self._font_cache[key] = font
        return font

    def __repr__(self):
        return '<Document>'
