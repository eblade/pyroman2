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

    def Tf(self, font, size):
        """ Set font """
        self.put("%s %i Tf" % (str(font), int(size)))

    def Td(self, tx, ty):
        """ First time: go to (tx, ty) 
            Then: go to next line and offset by (tx, ty) """
        self.put("%i %i Td" % (int(tx), int(ty)))

        """ Set render mode 
            0 - Fill text
            1 - Stroke text
            2 - Fill, then stroke
            3 - Invisible
            4 - Fill text and add path for clipping
            5 - Stroke text and add path for clipping
            6 - Fill text and stroke and add path for clipping
            7 - Add test to path for clipping """
    def Tr(self, render_mode):
        self.put("%i Tr" % int(render_mode))

    def w(self, width):
        """ Set stroke width """
        self.put("%i w" % int(width))

    def g(self, gray):
        """ Set gray level 0.0 - 1.0"""
        self.put("%f g" % float(gray))

    def Tj(self, string):
        """ Show text """
        self.put("%s Tj" % (str(string)))

    def Tc(self, charSpace):
        """ Set char spacing (defaults to 0) """
        self.put("%i Tc" % (int(charSpace)))

    def Tw(self, wordSpace):
        """ Set word spacing (defaults to 0) """
        self.put("%i Tw" % (int(wordSpace)))

    def Tz(self, scaling):
        """ Set horizontal scaling in percent (defaults to 100) """
        self.put("%i Tz" % (int(scaling)))

    def TL(self, leading):
        """ Set text leading (line height) """
        self.put("%i TL" % (int(leading)))

    def Ts(self, rise):
        """ Set text rise """
        self.put("%i Ts" % (int(rise)))

    def Tstar(self):
        """ Equivalent to 0 <Tl> Td """
        self.put("T*")

    def Ttick(self, string):
        """ Equivalent to T* string Tj """
        self.put("%s '" % (str(string)))

    def Tticktick(self, aw, ac, string):
        """ Equivalent to aw Tw ac Tc string ' """
        self.put("%i %i %s \"" % (int(aw), int(ac), str(string)))
