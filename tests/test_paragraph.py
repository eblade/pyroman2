from pyroman.paragraph import Paragraph
from pyroman.parse.rst.paragraph import parse_paragraph
from tests.fixture import a4doc

import pyroman.json as json


class TestParagraph:
    def test_calculate(self):
        document, page, box = a4doc()

        p = Paragraph(document, box)
        p.children = parse_paragraph('This is some text that is too long to fit in one line')
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

        p1 = Paragraph(document, box)
        p1.children = parse_paragraph('This is the content of the first paragraph')
        box.append(p1)

        p2 = Paragraph(document, box)
        p2.children = parse_paragraph('This is the content of the second paragraph')
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

    def test_parse_rst_plain(self):
        atoms = list(parse_paragraph('one two three'))
        assert len(atoms) == 3
        assert atoms[0].content == 'one'
        assert atoms[1].content == 'two'
        assert atoms[2].content == 'three'

    def test_parse_rst_format(self):
        atoms = list(parse_paragraph('one *two* **three** `four`'))
        assert len(atoms) == 4
        assert atoms[0].content == 'one'
        assert atoms[0].font_style == ''
        assert atoms[0].font_family == None
        assert atoms[1].content == 'two'
        assert atoms[1].font_style == 'bold'
        assert atoms[1].font_family == None
        assert atoms[2].content == 'three'
        assert atoms[2].font_style == 'italic'
        assert atoms[2].font_family == None
        assert atoms[3].content == 'four'
        assert atoms[3].font_style == ''
        assert atoms[3].font_family == 'Courier'
