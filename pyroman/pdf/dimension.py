from .object import Rectangle

def cm_to_points(cm):
    return int(float(cm)*28.3464567)

def get_page_box(p):
    (w, h) = p
    return Rectangle(0, 0, w, h)

# Page sizes
Letter = (612, 792)
LetterSmall = (612, 792)
Tabloid = (792, 1224)
Ledger = (1224, 792)
Legal = (612, 1008)
Statement = (396, 612)
Executive = (540, 720)
A0 = (2384, 3371)
A1 = (1685, 2384)
A2 = (1190, 1684)
A3 = (842, 1190)
A4 = (595, 842)
A4Small = (595, 842)
A5 = (420, 595)
B4 = (729, 1032)
B5 = (516, 729)
Folio = (612, 936)
Quarto = (610, 780)


MarginDefault = (
    cm_to_points(2.5), # top
    cm_to_points(2.0), # right
    cm_to_points(1.5), # bottom
    cm_to_points(2.0), # left
)

