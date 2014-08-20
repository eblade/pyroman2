from pyroman.document import Document
from pyroman.page import Page, Layout
from pyroman.box import Box
from pyroman.paragraph import Paragraph
from pyroman.pdf.dimension import A4, MarginDefault
from pyroman.parameters import defaults


def get_new_page(document, layout):
    page = Page(document)
    page.layout = layout
    document.append(page)
    box = Box(document, page, {
        'box-class': 'main',
    })
    page.append(box)
    return page, box


def convert(title, content):
    page_width, page_height = A4
    document = Document({
        'width': page_width,
        'height': page_height
    })
    document.margin = MarginDefault

    layout = Layout()
    layout.define_area(
        'main',
        (document.margin_left, document.margin_top),
        (document.width - document.margin_right,
         document.height - document.margin_bottom))

    first_page, first_box = get_new_page(document, layout)
    titlep = Paragraph(document, first_box, defaults.get('code'))
    titlep.content = title
    titlep.font_style = 'bold'
    paragraph = Paragraph(document, first_box, defaults.get('code'))
    paragraph.content = content

    first_box.append(titlep)
    first_box.append(paragraph)

    orphans = first_box.calculate()

    while len(orphans) > 0:
        new_page, new_box = get_new_page(document, layout)
        new_box.children = orphans
        orphans = new_box.calculate()

    return document
