from .element import Element
from .constants import LABEL_CLASS_MARK, ALIGN_JUSTIFY


class TextAtom(Element):
    def init(self):
        self.content = self._params.get('content', '')
        self.font_family = self._params.get('font-family')
        self.font_style = self._params.get('font-style')
        self.font_size = self._params.get('font-size')
        self.text_color = self._params.get('text-color')
        self.base_line = self._params.get('base_line')
        self.line_height = self._params.get('line_height')
        self.rise = self._params.get('rise')
        self.offset = self._params.get('offset')
        self.gray = self._params.get('gray')
        self.indent = self._params.get('indent')
        self.scale = self._params.get('scale')
        self.beginning_of_line = self._params.get('beginning-of-line', False)
        self.end_of_line = self._params.get('end-of-line', False)
        self.end_of_word = self._params.get('end-of-word', True)
        self.word_spacing = self._params.get('word-spacing', 0)
        self.char_spacing = self._params.get('char-spacing', 0)
        self.length = len(self.content)

    def __repr__(self):
        specials = ''
        if self.beginning_of_line:
            specials += "\u03B1"
        if self.end_of_word:
            specials += "."
        if self.end_of_line:
            specials += "\u00B6"
        if specials:
            specials = ' ' + specials
        return '<Atom %s%i _%s |%i w%i "%s"%s>' % ('+' if self.indent is not None and self.indent  >= 0 else '', 
                                                    int(self.indent or 0),
                                                    '?' if self.base_line is None else str(int(self.base_line)),
                                                    self.line_height,
                                                    self.width,
                                                    self.content[:20],
                                                    specials)

    @property
    def font_key(self):
        return "%s-%s" % (self.font_family, self.font_style)
    
    @property
    def font_key_ext(self):
        return "%s-%s-%i" % (self.font_family, self.font_style, self.font_size)
    
    def calculate(self):
        font = self.doc.get_font(self.font_family, self.font_style, self.font_size)
        self.width, self.height = font.getsize(self.content)
        self.line_height = self.font_size * self.parent.line_height


class TextLine:
    def __init__(self, top, width, indent=0):
        self.atoms = []
        self.max_char_spacing = 3.0
        self.max_word_spacing = .25
        self.line_height = None
        self.top = top
        self.width = width
        self.indent = indent
        self.base_line = None

    def add_atom(self, atom):
        self.atoms.append(atom)
        self.add_spaces()
        all_words_width = float(sum([x.width for x in self.atoms]))
        return self.width - self.indent - all_words_width

    def add_spaces(self):
        for atom in self.atoms[:-1]:
            if atom.end_of_word and not atom.content.endswith(' '):
                atom.content += ' '
                atom.calculate()
            atom.end_of_line = False
        self.atoms[0].beginning_of_line = True   
        self.atoms[0].indent = self.indent   
        self.atoms[-1].end_of_line = True   

    def calculate_line_height(self):
        if len(self.atoms) == 0:
            self.line_height = 0 
            return 0
        self.line_height = max([x.line_height for x in self.atoms])
        self.atoms[0].line_height = self.line_height
        self.base_line = self.top + self.line_height
        for atom in self.atoms:
            atom.base_line = self.base_line
            atom.y = self.base_line - atom.height
        return self.line_height

    def justify(self):
        width = float(self.width) - float(self.indent)
        all_words_width = float(sum([x.width for x in self.atoms]))
        nr_of_chars = sum([x.length for x in self.atoms])
        nr_of_words = len([x for x in self.atoms if x.end_of_word or x.end_of_line])
        missing = width - all_words_width
        self.atoms[0].word_spacing = missing / float(nr_of_words - 1)


class Paragraph(Element):
    def init(self):
        self.label_class = LABEL_CLASS_MARK
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
        self.gray = self._params.get(
            'gray')
        self.scale = self._params.get(
            'scale')
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
            'margin-top', 0)
        self.margin_right = self._params.get(
            'margin-right', 0)
        self.margin_bottom = self._params.get(
            'margin-bottom', 0)
        self.margin_left = self._params.get(
            'margin-left', 0)
        self.first_indent = self._params.get(
            'first_indent', self.parent.first_indent)
        self.base_line = 0

    def __repr__(self):
        return '<Paragraph (%i, _%i/%i) %i+%i+%i "%s">' % (
            self.x,
            self.base_line,
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
        self.width = self.max_width
        self.height = 0
        x = 0
        y = 0
        words = self.content.split(' ')
        lines = []
        line_no = 0
        current_line = TextLine(0, self.width, indent=self.first_indent)
        left = self.width
        for word in words:
            atom = TextAtom(self.doc, self, {
                'content': word,
                'font-family': self.font_family,
                'font-style': self.font_style,
                'font-size': self.font_size,
                'text-color': self.text_color,
                'gray': self.gray,
                'scale': self.scale,
            })
            atom.calculate()
            if atom.width <= left:
                left = current_line.add_atom(atom)
            else:
                line_height = current_line.calculate_line_height()
                self.height += line_height
                last_top = current_line.top
                lines.append(current_line)
                current_line = TextLine(last_top + line_height, self.width)
                line_no += 1
                if line_no == 1 and self.first_indent > 0:  # second line
                    current_line.indent = -self.first_indent
                left = current_line.add_atom(atom)
        self.height += current_line.calculate_line_height()
        lines.append(current_line)
        for line in lines:
            if self.align == ALIGN_JUSTIFY:
                line.justify()
        self.children = [] 
        for line in lines:
            for atom in line.atoms:
                self.children.append(atom)
        self.base_line = self.y + lines[0].base_line

    @property
    def atoms(self):
        for atom in self.children:
            copy_of_atom = atom.copy()
            copy_of_atom.x += self.parent.x + self.parent.parent.x
            copy_of_atom.y += self.parent.y + self.parent.parent.y
            copy_of_atom.base_line += self.parent.parent.y + self.parent.y
            yield copy_of_atom
