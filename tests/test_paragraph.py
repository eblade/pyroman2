from pyroman.paragraph import Paragraph
from tests.fixture import a4doc

import pyroman.json as json


class TestParagraph:
    def test_calculate(self):
        document, page, box = a4doc()

        p = Paragraph(document, box)
        p.content = 'This is some text that is too long to fit in one line'
        p.max_width = 200
        box.append(p)

        p.calculate()

        print(json.dumph(document))

        assert len(p.children) == 13
        assert p.height == 28
        assert p.width == 200
        assert p.children[0].position == (0, 0)

    def test_two_paragraphs(self):
        document, page, box = a4doc()

        p1 = Paragraph(document, box, {
            'content': 'This is the content of the first paragraph',
        })
        box.append(p1)

        p2 = Paragraph(document, box, {
            'content': 'This is the content of the second paragraph',
        })
        box.append(p2)

        orphans = box.calculate()
        print(json.dumph(document))
        assert len(orphans) == 0
        assert p1.y == 0
        assert p2.y == p1.height

        paragraphs = [p for p in page.paragraphs]
        assert len(paragraphs) == 2
        for p in paragraphs:
            assert len(p.children) == 8
