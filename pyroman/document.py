from PIL import ImageFont

from .element import Element
from .parameters import Parameters
from .constants import *

class Document(Element):
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
        self.max_width = self._params.get('max-width')
        self.max_height = self._params.get('max-height')
        self.line_height = self._params.get('line-height')
        self.space_width = self._params.get('space-width')

        self._stream = []
        self._font_cache = {}

    def get_font(self, font_family, font_size):
        key = '%s-%i' % (font_family, font_size)
        font = self._font_cache.get(key, None)
        if font is None:
            font = ImageFont.truetype('%s.ttf' % font_family, font_size)
            self._font_cache[key] = font
        return font

    def serialize(self, options={}):
        output = super().serialize(options)
        output.update({
            'word-wrap': self.word_wrap,
            'font-family': self.font_family,
            'font-size': self.font_size,
            'text-color': self.text_color,
            'align': self.align,
            'content': self.content,
            'max-width': self.max_width,
            'max-height': self.max_height,
            'line-height': self.line_height,
            'space-width': self.space_width,
        })
        return output
