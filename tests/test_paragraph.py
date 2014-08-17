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

        assert p.absolute_position == (page.margin_left, page.margin_top)
        assert len(p.children) == 13
        assert int(p.height) == 28
        assert p.width == 200
        first_atom = p.children[0]
        assert first_atom.position[0] == p.first_indent  # x
        assert first_atom.position[1] == first_atom.base_line - first_atom.height  # y

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

        assert p2.base_line == p2.children[0].line_height
