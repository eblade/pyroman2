from .element import Element
from .constants import *

class Paragraph(Element):
    def init(self):
        self.label_class = LABEL_CLASS_MARK
        self.wordwrap = self._params.get('wordwrap', True)
        self.font_family = self._params.get('font-family', doc.font_family)
        self.font_size = self._params.get('font-size', doc.font_size)
        self.align = self._params.get('align', ALIGN_LEFT)
