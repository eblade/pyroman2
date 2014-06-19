class Element:
    def __init__(self):
        self._parts = []
        self.init()

    def init(self):
        self.start_tag = None
        self.end_tag = None

    def put(self, value):
        self._parts.append(value)

    def __str__(self):
        output = "%s %s\n%s\n" % (
            self.start_tag,
            '   \n'.join([str(part) for part in self._parts]),
            self.end_tag,
        )
        self._cached_len = len(output)
        return output

    def __len__(self):
        try:
            return self._cached_len
        except AttributeError:
            return len(str(self))

class TextObject(Element):
    def init(self):
        self.start_tag = "BT"
        self.end_tag = "ET"

    def Font(self, font, size):
        self.put("%s %i Tf" % (str(font), int(size)))

    def Position(self, from_left, from_bottom):
        self.put("%i %i Td" % (int(from_left), int(from_bottom)))

    def Render(self, render_mode):
        self.put("%i Tr" % int(render_mode))

    def Width(self, width):
        self.put("%i w" % int(width))

    def Gray(self, gray):
        self.put("%f g" % float(gray))

    def Text(self, string):
        self.put("%s Tj" % (str(string)))
