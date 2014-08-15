from pyroman.convert import pyroman2pdf
from pyroman.paragraph import Paragraph
import pyroman.json as json

from tests.fixture import a4doc


class TestConvert:
    def test_single_page(self):
        document, page, box = a4doc()

        h1 = Paragraph(document, box, {
            'content': 'This Is The First Heading',
            'font-size': 24,
            'font-style': 'bold',
            'margin-bottom': 10,
        })
        assert h1.font_size == 24
        assert h1.font_style == 'bold'
        assert h1.margin_bottom == 10

        p1 = Paragraph(document, box, {
            'content': 'This is the contents of the first paragraph. '*10,
            'margin-bottom': 5,
            'first-indent': 30,
        })

        h2 = Paragraph(document, box, {
            'content': 'This Is The Second Heading',
            'font-size': 24,
            'font-style': 'bold',
            'margin-top': 20,
            'margin-bottom': 10,
        })
        assert h2.margin_top == 20

        p2 = Paragraph(document, box, {
            'content': 'This is the contents of the second paragraph. '*10,
            'font-family': 'Times',
            'font-style': 'standard',
            'margin-bottom': 5,
            'first-indent': 30,
        })

        box.append(h1)
        box.append(p1)
        box.append(h2)
        box.append(p2)

        box.calculate()

        print(json.dumph(document))

        assert h1.y == h1.margin_top
        assert p1.y == h1.height + max(h1.margin_bottom, p1.margin_top)
        assert h2.y == p1.y + p1.height + max(p1.margin_bottom, h2.margin_top)
        assert p2.y == h2.y + h2.height + max(h2.margin_bottom, p2.margin_top)

        pdf = pyroman2pdf.convert(document)

        with open('/tmp/test_single_page.pdf', 'w') as f:
            f.write(str(pdf))

        #assert False
