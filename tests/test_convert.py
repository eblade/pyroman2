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
            'margin-bottom': 10,
        })

        p1 = Paragraph(document, box, {
            'content': 'This is the contents of the first paragraph. '*10,
            'margin-bottom': 5,
        })

        h2 = Paragraph(document, box, {
            'content': 'This Is The Second Heading',
            'font-size': 24,
            'margin-top': 20,
            'margin-bottom': 10,
        })

        p2 = Paragraph(document, box, {
            'content': 'This is the contents of the second paragraph. '*10,
            'margin-bottom': 5,
        })

        box.append(h1)
        box.append(p1)
        box.append(h2)
        box.append(p2)

        box.calculate()

        print(json.dumph(document))
        print([atom for atom in page.atoms])
        
        pdf = pyroman2pdf.convert(document)
            
        with open('/tmp/test_single_page.pdf', 'w') as f:
            f.write(str(pdf))
