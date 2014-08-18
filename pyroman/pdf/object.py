class Object:
    def __init__(self, id=0):
        self.object_identifier = id
        self._content = []

    def __str__(self):
        return ''.join([x.__str__() for x in self._content])

    def put(self, obj):
        self._content.append(obj)

    @property
    def obj(self):
        if self.object_identifier == 0:
            raise TypeError("Indirect object must be given an object identifiier")
        return "%i 0 obj\n%s\nendobj\n" % (self.object_identifier, self.inline)

    @property
    def inline(self):
        if self.object_identifier == 0:
            raise TypeError("Indirect object must be given an object identifiier")
        return self.__str__()

    @property
    def objects(self):
        return ''.join([x.obj for x in self._content])

    @property
    def reference(self):
        if self.object_identifier == 0:
            raise TypeError("Indirect object must be given an object identifiier")
        return "%i 0 R" % self.object_identifier

    def __len__(self):
        return sum([len(x) for x in self._content])

    @property
    def count(self):
        return len(self._content)

class Boolean(Object):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._content = True 

    def __str__(self):
        return 'true' if self._content else 'false'

    def put(self, value):
        self._content = bool(value)

class Integer(Object):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._content = 0 

    def __str__(self):
        return str(self._content)

    def put(self, value):
        self._content = int(value)

class Real(Object):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._content = 0.0 

    def __str__(self):
        return str(self._content)

    def put(self, value):
        self._content = float(value)

class String(Object):
    def __init__(self, value, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._content = value

    def __str__(self):
        return "(%s)" % super().__str__().replace(')', '\)').replace('(', '\(')

class HexadecimalString(Object):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._content = ''

    def __str__(self):
        return "<%s>\n" % self._content

    def put(self, value):
        self._content = str(value)

class Name(HexadecimalString):
    def __init__(self, value, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._content = value

    def __str__(self):
        return "/%s" % self._content

class Array(Object):
    def __str__(self):
        return "[ %s ]" % '\n'.join([x.__str__() for x in self._content])

class Dictionary(Object):
    def put(self, key, value):
        self._content.append((key, value))

    def __str__(self):
        return "<< %s >>" % '\n   '.join(["%s %s" % (x[0].__str__(), 
            x[1].__str__()) for x in self._content])

class Null:
    def __str__(self):
        return "null"

class Rectangle(Object):
    def __init__(self, llx, lly, urx, ury, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.llx = llx 
        self.lly = lly 
        self.urx = urx 
        self.ury = ury 

    def __str__(self):
        return "[%s %s %s %s]" % (
            str(self.llx),
            str(self.lly),
            str(self.urx),
            str(self.ury)
        )

    def marginize(self, top, bottom, left, right):
        return Rectangle(self.llx+left, self.lly+bottom, self.urx-right, self.ury-top)
