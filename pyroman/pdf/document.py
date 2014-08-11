from .object import Object, Dictionary

def next_id():
    next_id._id += 1
    return next_id._id
next_id._id = 0

class Header:
    def __init__(self, version):
        self.version = version

    def __str__(self):
        return "%%PDF-%.1f\n" % self.version

class Body(Object):
    pass

class CrossReferenceTable(Object):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.put(0, 65536, keyword='f') # i think it should be there

    def __str__(self):
        return "xref\n%i %i\n%s\n" % (
            0, len(self._content),
            '\n'.join(['%010i %05i %s ' % x for x in self._content])
        )
    
    def put(self, offset, generation=0, keyword='n'):
        self._content.append((int(offset), int(generation), keyword))


class Trailer:
    def __init__(self):
        self.offset_to_cross_reference_table = 0
        self._dictionary = Dictionary()

    def __str__(self):
        if self.offset_to_cross_reference_table == 0:
            raise ValueError("Must set offset to first cross reference table")
        return "trailer\n%s\nstartxref\n%i\n%%%%EOF" % (
            self._dictionary,
            self.offset_to_cross_reference_table
        )

    def Size(self, value):
        "Required Size = Integer"
        self._dictionary.put('/Size', value)

    def Root(self, value):
        "Required Root = ref Dictionary"
        self._dictionary.put('/Root', value)

    def Info(self, value):
        "Optional Info = ref Dictionary"
        self._dictionary.put('/Info', value)

    def ID(self, value):
        "Optional ID = Array"
        self._dictionary.put('/ID', value)

class DocumentCatalog(Dictionary):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.put("/Type", "/Catalog")

    def Pages(self, value):
        "Required Pages = ref Dictionary"
        self.put("/Pages", value)

    def PageLabels(self, value):
        "Optional Pages = Number Tree"
        self.put("/PageLabels", value)

    def Names(self, value):
        "Optional Names = Name Dictionary"
        self.put("/Names", value)

    def Dests(self, value):
        "Optional Dests = ref Dictionary"
        self.put("/Dests", value)

    def ViewerPreferences(self, value):
        "Optional ViewerPreferences = Dictionary"
        self.put("/ViewerPreferences", value)

    def PageLayout(self, value):
        "Optional PageLayout = Name"
        self.put("/PageLayout", value)

    def PageMode(self, value):
        "Optional PageMode = Name"
        self.put("/PageMode", value)

    def Outlines(self, value):
        "Optional Outlines = ref Dictionary (Document Outline)"
        self.put("/Outlines", value)

    def Threads(self, value):
        "Optional Threads = ref Array (of references to Articel Threads)"
        self.put("/Threads", value)

    def Metadata(self, value):
        "Optional Metadata = ref Metadata Stream"
        self.put("/Metadata", value)

    def StructTreeRoot(self, value):
        "Optional StructTreeRoot = ref Dictionary"
        self.put("/StructTreeRoot", value)

    def MarkInfo(self, value):
        "Optional MarkInfo = ref Dictionary"
        self.put("/MarkInfd", value)

    def Lang(self, value):
        "Optional Lang = String"
        self.put("/MarkInfd", value)

    def OutputIntents(self, value):
        "Optional OutputIntents = Array"
        self.put("/OutputIntents", value)

    def PieceInfo(self, value):
        "Optional PieceInfo = Dictionary"
        self.put("/PieceInfo", value)

    def Legal(self, value):
        "Optional Legal = Dictionary"
        self.put("/Legal", value)

    def Requirements(self, value):
        "Optional Requirements = Dictionary"
        self.put("/Requirements", value)

class PageTreeNode(Dictionary):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.put("/Type", "/Pages")
    
    def Parent(self, value):
        "Required Parent = ref Dictionary"
        self.put("/Parent", value)
    
    def Kids(self, value):
        "Required Kids = Array of ref Dictionary"
        self.put("/Kids", value)

    def Count(self, value):
        "Required Count = Integer (sum of leaf nodes)"
        self.put("/Count", value)

class Page(Dictionary):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.put("/Type", "/Page")
    
    def Parent(self, value):
        "Required Parent = ref Dictionary"
        self.put("/Parent", value)
    
    def Resources(self, value):
        "Required Resources = Resource Dictionary"
        self.put("/Resources", value)
    
    def MediaBox(self, value):
        "Optional MediaBox = Rectangle"
        self.put("/MediaBox", value)

    def CropBox(self, value):
        "Optional CropBox  = Rectangle"
        self.put("/CropBox", value)

    def BleedBox(self, value):
        "Optional BleedBox  = Rectangle"
        self.put("/BleedBox", value)

    def TrimBox(self, value):
        "Optional TrimBox  = Rectangle"
        self.put("/TrimBox", value)

    def ArtBox(self, value):
        "Optional ArtBox  = Rectangle"
        self.put("/ArtBox", value)

    def BoxColorInfo(self, value):
        "Optional BoxColorInfo  = Dictionary"
        self.put("/BoxColorInfo", value)

    def Contents(self, value):
        "Optional Contents  = Content Stream|Array of Content Streams"
        self.put("/Contents", value)

    def Rotate(self, value):
        "Optional Rotate  = Integer"
        self.put("/Integer", value)

    def Thumb(self, value):
        "Optional Thumb  = Stream"
        self.put("/Thumb", value)

    def B(self, value):
        "Optional B  = Array of ref Articles"
        self.put("/B", value)

    def Dur(self, value):
        "Optional Dur  = Integer (Presentation mode advance time)"
        self.put("/Dur", value)

    def Trans(self, value):
        "Optional Trans  = Dictionary (Presentation mode transition effects)"
        self.put("/Trans", value)

    def Annots(self, value):
        "Optional Annots  = Array"
        self.put("/Annots", value)

    def Metadata(self, value):
        "Optional Metadata = ref Metadata Stream"
        self.put("/Metadata", value)

    def StructParents(self, value):
        "Optional StructParents = Integer"
        self.put("/StructParents", value)

    def PZ(self, value):
        "Optional PZ = Real"
        self.put("/PZ", value)

    def SeparationInfo(self, value):
        "Optional SeparationInfo = Dictionary"
        self.put("/SeparationInfo", value)

    def Tabs(self, value):
        "Optional Tabs = Name"
        self.put("/Tabs", value)

    def TemplateInstantiated(self, value):
        "Optional TemplateInstantiated = Name"
        self.put("/TemplateInstantiated", value)

    def PresSteps(self, value):
        "Optional PresSteps = Name"
        self.put("/PresSteps", value)

    def UserUnit(self, value):
        "Optional UserUnit = Real"
        self.put("/UserUnit", value)

    def VP(self, value):
        "Optional VP = Array of Viewport Dictionarys"
        self.put("/VP", value)

class NameDictionary(Dictionary):
    def Dests(self, value):
        "Optional Dests = Name Tree"
        self.put("/Dests", value)

class Font(Dictionary):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.put("/Type", "/Font")

    def BaseFont(self, value):
        "Required BaseFont = Name"
        self.put("/BaseFont", value)

    def Encoding(self, value):
        "Required Encoding = Name"
        self.put("/Encoding", value)

    def SubType(self, value):
        "Required SubType = Name"
        self.put("/SubType", value)

    def Name(self, value):
        "Required Name = Name"
        self.put("/Name", value)

class Document:
    def __init__(self, version=1.7):
        self.object_identifier = 0
        self.header = Header(version)
        self.body = Body()
        self.cross_reference_table = CrossReferenceTable()
        self.trailer = Trailer()

    def __str__(self):
        header = str(self.header)
        ack = len(header)
        for o in self.body._content:
            self.cross_reference_table.put(ack)
            ostr = str(o.obj)
            ack += len(ostr)
        self.trailer.offset_to_cross_reference_table = ack
        return ''.join([
            header,
            self.body.objects,
            str(self.cross_reference_table),
            str(self.trailer),
        ])
