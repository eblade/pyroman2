from .element import Element
from .constants import LABEL_CLASS_MARK


class TextAtom(Element):
    def init(self):
        self.content = self._params.get('content', '')
        self.font_family = self._params.get('font-family')
        self.font_size = self._params.get('font-size')
        self.text_color = self._params.get('text-color')
        self.base_line = self._params.get('base_line')

    def __repr__(self):
        return '<Atom _%i (%i, %i) %ix%i "%s">' % (self.base_line,
                                                   self.x, self.y,
                                                   self.width, self.height,
                                                   self.content[:20])

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
            'base-line': self.base_line,
        })
        return output


class Paragraph(Element):
    def init(self):
        self.label_class = LABEL_CLASS_MARK
        self.word_wrap = self._params.get(
            'word-wrap', self.parent.word_wrap)
        self.font_family = self._params.get(
            'font-family', self.parent.font_family)
        self.font_size = self._params.get(
            'font-size', self.parent.font_size)
        self.text_color = self._params.get(
            'text-color', self.parent.text_color)
        self.align = self._params.get(
            'align', self.parent.align)
        self.content = self._params.get(
            'content', '')
        self.max_width = self._params.get(
            'max-width', self.parent.width - (self.margin_left or 0) -
            (self.margin_right or 0))
        self.max_height = self._params.get(
            'max-height', self.parent.height - (self.margin_top or 0) -
            (self.margin_bottom or 0))
        self.line_height = self._params.get(
            'line-height', self.parent.line_height)
        self.space_width = self._params.get(
            'space-width', self.parent.space_width)
        self.margin_top = self._params.get(
            'margin-top', self.parent.margin_top or 0)
        self.margin_right = self._params.get(
            'margin-right', self.parent.margin_right or 0)
        self.margin_bottom = self._params.get(
            'margin-bottom', self.parent.margin_bottom or 0)
        self.margin_left = self._params.get(
            'margin-left', self.parent.margin_left or 0)

    def __repr__(self):
        return '<Paragraph (%i, %i) %i+%i+%i "%s">' % (
            self.x,
            self.y,
            self.margin_top,
            self.height,
            self.margin_bottom,
            self.content[:20]
        )

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
        current_line_height = int(self.line_height * self.font_size)
        atoms_on_this_line = []
        for atom in atoms:
            atom.calculate()
            if self.max_width is not None and x + atom.width > self.max_width:
                y += current_line_height
                for atom_on_line in atoms_on_this_line:
                    atom_on_line.base_line = y
                atoms_on_this_line = []
                if self.max_height is not None and y > self.max_height:
                    break
                x = 0
                current_line_height = int(self.line_height * self.font_size)
            atom.position = (x, y)
            x += atom.width + self.space_width
            current_line_height = max(current_line_height, atom.height)
            atoms_on_this_line.append(atom)
        y += current_line_height
        for atom_on_line in atoms_on_this_line:
            atom_on_line.base_line = y
        self.width = self.max_width
        self.height = y
        self.children = atoms
