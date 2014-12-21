from .construct import Construct
from .parameters import defaults
from .paragraph import Paragraph


class ListItem(Construct):
    def init(self):
        super().init()
        self.level = self._params.get('level', 1)
        self.bullet = self._params.get('bullet')
        self.indent_bullet = self._params.get('indent-bullet', 0)
        self.indent_content = self._params.get('indent-content', 0)

    def __repr__(self):
        return '<ListItem (%i,%i) %ix%i>' % (self.x, self.y,
                                             self.width, self.height)

    def calculate(self):
        self.parse()
        current_y = 0
        last_bottom_margin = 0
        self.width = self.parent.width - self.margin_left - self.margin_right
        self.bullet.x = self.indent_bullet
        self.bullet.y = current_y
        self.bullet.calculate()
        for child in self.children:
            print("Calculating " + str(child))
            child.x = child.margin_left + self.indent_content
            child.y = current_y + max(last_bottom_margin, child.margin_top)
            child.max_width = self.width - child.margin_left - child.margin_right
            child.calculate()  # should pass "obstacles" into this one
            current_y = child.y + child.height
            last_bottom_margin = child.margin_bottom
            print("Calculated " + str(child))
        self.children = [self.bullet] + self.children


class List(Construct):
    def init(self):
        super().init()
        self.bullet = [self.create_bullet(*x) for x in defaults.get('bullet')]
        self.input_format = self._params.get('input-format', self.document.input_format)
        self.list_indent = self._params.get('list-indent', 10)

    def create_bullet(self, font_family, font_style, font_size, content):
        bullet = Paragraph(self.document, self, {
            'font-family': font_family,
            'font-style': font_style,
            'font-size': font_size,
        })
        bullet.content = content
        return bullet

    def __repr__(self):
        return '<List (%i,%i) %ix%i>' % (self.x, self.y,
                                              self.width, self.height)

    def calculate(self):
        self.parse()
        current_y = 0
        last_bottom_margin = 0
        self.width = self.parent.width - self.margin_left - self.margin_right
        for child in self.children:
            print("Calculating " + str(child))
            child.x = child.margin_left
            child.y = current_y + max(last_bottom_margin, child.margin_top)
            child.max_width = self.width - child.margin_left - child.margin_right
            child.calculate()  # should pass "obstacles" into this one
            current_y = child.y + child.height
            last_bottom_margin = child.margin_bottom
            print("Calculated " + str(child))

    def parse(self):
        if self.input_format == 'pyroman':
            self.parse_pyroman()

    def parse_pyroman(self):
        lines = []
        for line in self.content.split('\n'):
            if line.startswith('*'):
                lines.append(line.strip())
            else:
                lines[-1] += line.strip()
        for line in lines:
            if line.startswith('* '):
                level = 1
                mode = 'bullet'
            elif line.startswith('** '):
                level = 2
                mode = 'bullet'
            elif line.startswith('*** '):
                level = 3
                mode = 'bullet'
            elif line.startswith('**** '):
                level = 4
                mode = 'bullet'
            elif line.startswith('***** '):
                level = 5
                mode = 'bullet'
            elif line.startswith('****** '):
                level = 6
                mode = 'bullet'
            elif line.startswith('******* '):
                level = 7
                mode = 'bullet'
            if mode == 'bullet':
                li = ListItem(self.doc, self, {
                    'indent-bullet': level * self.list_indent,
                    'indent-content': (level + 1) * self.list_indent,
                    'bullet': self.bullet[level]
                })
                li.content = line[level+1:]
                self.children.append(li)
