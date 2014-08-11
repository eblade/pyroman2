from .element import Element
from .constants import *

class TextAtom(Element):
    def init(self):
        self.content = self._params.get('content', '')
        self.font_family = self._params.get('font-family')
        self.font_size = self._params.get('font-size')
        self.text_color = self._params.get('text-color')

    def __repr__(self):
        return '<Atom (%i, %i) "%s">' % (self.x, self.y, self.content[:20])

    def calculate(self):
        font = self.doc.get_font(self.font_family, self.font_size)
        self.width, self.height = font.getsize(self.content)

    def serialize(self, options={}):
        output = super().serialize(options)
        output.update({
            'content': self.content,
            'font-family': self.font_family,
            'font-size': self.font_size,
            'text-color': self.text_color,
        })
        return output

class Paragraph(Element):
    def init(self):
        self.label_class = LABEL_CLASS_MARK
        self.word_wrap = self._params.get('word-wrap', self.parent.word_wrap)
        self.font_family = self._params.get('font-family', self.parent.font_family)
        self.font_size = self._params.get('font-size', self.parent.font_size)
        self.text_color = self._params.get('text-color', self.parent.text_color)
        self.align = self._params.get('align', self.parent.align)
        self.content = self._params.get('content', '')
        self.max_width = self._params.get('max-width', self.parent.width - (self.margin_left or 0) - (self.margin_right or 0))
        self.max_height = self._params.get('max-height', self.parent.height - (self.margin_top or 0) - (self.margin_bottom or 0))
        self.line_height = self._params.get('line-height', self.parent.line_height)
        self.space_width = self._params.get('space-width', self.parent.space_width)

    def __repr__(self):
        return '<Paragraph @%i "%s">' % (self.y, self.content[:20])

    @property
    def stream(self):
        for obj in self.children:
            yield obj

    def calculate(self):
        words = self.content.split(' ')
        atoms = [TextAtom(self.doc, self, {
            'content': word,
            'font-family': self.font_family,
            'font-size': self.font_size,
            'text-color': self.text_color,
            }) for word in words]
        
        x = 0
        y = 0
        current_line_height = self.line_height
        for atom in atoms:
            atom.calculate()
            if self.max_width is not None and x + atom.width > self.max_width:
                y += current_line_height
                if self.max_height is not None and y > self.max_height:
                    break
                x = 0
                current_line_height = self.line_height
            atom.position = (x, y)
            x += atom.width + self.space_width
            current_line_height = max(current_line_height, atom.height)
        self.width = self.max_width
        self.height = y + current_line_height
        self.children = atoms
