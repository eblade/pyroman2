import io

from .object import Object, Dictionary

class Stream(Object):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._dictionary = Dictionary()
        self._content = []
        self._total_size = None

    def __str__(self):
        return "%s\nstream\n%s\nendstream" % (self._dictionary, ''.join([str(x) for x in self._content]))

    def put(self, value):
        self._content.append(value) 

    def stream(self, buffer_size=io.DEFAULT_BUFFER_SIZE):
        content = [self._dictionary, "\nstream\n"]
        content.extend(self._content)
        content.extend("\nendstream\n")
        def report_size(size):
            self._total_size = size
        class ObjectStream(io.RawIOBase):
            def __init__(self):
                self.leftover = None
                self.total_size = 0

            def readable(self):
                return True

            def readinto(self, b):
                try:
                    l = len(b)
                    chunk = self.leftover or str(next(content))
                    output, self.leftover = chunk[:l], chunk[l:]
                    l_output = len(output)
                    b[:l_output] = output
                    self.total_size += l_output
                    return l_output
                except StopIteration:
                    report_size(self.total_size)
                    return 0
        return io.BufferedReader(IterStream(), buffer_size=buffer_size)

    def __len__(self):
        if self._total_size is None:
            return len(str(self))
        else:
            return self._total_size

    def Length(self, length):
        "Required Length = Integer"
        self._dictionary.put('/Length', length)

    def Filter(self, filter_):
        "Optional Filter = Name|Array"
        self._dictionary.put('/Filter', filter_)

    def DecodeParms(self, decode_parms):
        "Optional DecodeParms = Dictionary|Array"
        self._dictionary.put('/DecodeParms', decode_parms)

    def F(self, f):
        "Optional F = file specification"
        self._dictionary.put('/F', f)

    def F(self, f_filter):
        "Optional FFilter = Name|Array"
        self._dictionary.put('/FFilter', f_filter)

    def FDecodeParms(self, f_decode_parms):
        "Optional FDecodeParms = Dictionary|Array"
        self._dictionary.put('/DecodeParms', f_decode_parms)

    def DL(self, dl):
        "Optional DL = Integer"
        self._dictionary.put('/DL', dl) 

