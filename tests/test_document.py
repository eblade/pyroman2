from pyroman.document import Document
from pyroman.page import Page, Layout
from pyroman.box import Box
from pyroman.paragraph import Paragraph
from pyroman.construct import Construct
import pyroman.json as json
from pyroman.pdf.dimension import A4, MarginDefault
from tests.fixture import a4doc
from pyroman.parameters import defaults

#from pyroman.pdf.dimension import A4

class TestDocument:
    """ Test that the basic hierachy is working """
    def test_hierarchy(self):
        page_width, page_height = A4
        document = Document({
            'width': page_width,
            'height': page_height
        })
        assert document.width == page_width
        assert document.height == page_height

        document.margin = MarginDefault
        assert document.margin_top == MarginDefault[0]
        assert document.margin_right == MarginDefault[1]
        assert document.margin_bottom == MarginDefault[2]
        assert document.margin_left == MarginDefault[3]

        page = Page(document)

        layout = Layout()
        layout.define_area(
            'main',
            (page.margin_left, page.margin_top),
            (page.width - page.margin_right, page.height - page.margin_bottom))
        page.layout = layout

        document.append(page)

        assert page.width == page_width
        assert page_height == page_height

        box = Box(document, page, {
            'box-class': 'main',
        })
        page.append(box)

        assert box.y == MarginDefault[0] # top
        assert box.x == MarginDefault[3] # left
        assert box.width == page_width - MarginDefault[1] - MarginDefault[3]
        assert box.height == page_height - MarginDefault[0] - MarginDefault[2]

    """ Test that a Construct acts as a paragraph """
    def test_construct(self):
        document, page, box = a4doc()

        construct = Construct(document, box)
        construct.height = 200
        box.append(construct)
        
        p1 = Paragraph(document, construct, defaults.get('text'))
        p1.content = "some text in a paragraph in a construct"
        construct.append(p1)

        box.calculate()

        print(json.dumph(document))

        # must actually test stuff here
