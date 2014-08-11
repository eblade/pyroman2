from .element import Element


class Page(Element):
    def init(self):
        self.word_wrap = self._params.get('word-wrap', self.parent.word_wrap)
        self.font_family = self._params.get('font-family', self.parent.font_family)
        self.font_size = self._params.get('font-size', self.parent.font_size)
        self.text_color = self._params.get('text-color', self.parent.text_color)
        self.align = self._params.get('align', self.parent.align)
        self.width = self._params.get('width', self.parent.width)
        self.height = self._params.get('height', self.parent.height)
        self.line_height = self._params.get('line-height', self.parent.line_height)
        self.space_width = self._params.get('space-width', self.parent.space_width)
        self.margin_left = self._params.get('margin-left', self.parent.margin_left)
        self.margin_right = self._params.get('margin-right', self.parent.margin_right)
        self.margin_top = self._params.get('margin-top', self.parent.margin_top)
        self.margin_bottom = self._params.get('margin-bottom', self.parent.margin_bottom)
        self.page_number = self._params.get('page_number', 0)

        self.layout = None

    def append(self, box):
        if self.layout is None:
            raise ValueError("No layout set for this page")
        pos, dim = self.layout.get_dimensions(box.box_class)
        box.position = pos
        box.dimension = dim
        super().append(box)
    
    @property
    def atoms(self):
        for box in self.children:
            for paragraph in box.children:
                for atom in paragraph.children:
                    copy_of_atom = atom.copy()
                    copy_of_atom.x += box.x + paragraph.x
                    copy_of_atom.y += box.y + paragraph.y
                    yield copy_of_atom

    def __repr__(self):
        return '<Page %s (%ix%i)>' % (str(self.page_number), self.width, self.height)

class Layout(Element):
    def init(self, areas={}):
        self.areas = areas

    # box_class param is a per-page unique string
    # p1 is the upper-left corner of the area, measured from the upper-left corner of the page
    # p2 is the lower-right corner of the area, measured from the upper-left corner of the page
    def define_area(self, box_class, p1, p2):
        self.areas[box_class] = (p1, p2)

    def get_dimensions(self, box_class):
        boundaries = self.areas.get(box_class)
        if boundaries is None:
            raise KeyError("No area named %s is defined", box_class)
        (x1, y1), (x2, y2) = boundaries
        return (x1, y1), (x2-x1, y2-y1)
