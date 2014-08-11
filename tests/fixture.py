from pyroman.document import Document
from pyroman.page import Page, Layout
from pyroman.box import Box
from pyroman.pdf.dimension import MarginDefault, A4, A5

def a4doc():
    page_width, page_height = A4
    document = Document({
        'width': page_width,
        'height': page_height,
        'font-size': 12,
    })

    document.margin = MarginDefault
    page = Page(document)

    layout = Layout()
    layout.define_area(
        'main',
        (page.margin_left, page.margin_top),
        (page.width - page.margin_right, page.height - page.margin_bottom))
    page.layout = layout

    document.append(page)

    box = Box(document, page, {
        'box-class': 'main',
    })
    page.append(box)
    return document, page, box

def a5doc():
    page_width, page_height = A5
    document = Document({
        'width': page_width,
        'height': page_height,
        'font-size': 12,
    })

    document.margin = MarginDefault
    page = Page(document)

    layout = Layout()
    layout.define_area(
        'main',
        (page.margin_left, page.margin_top),
        (page.width - page.margin_right, page.height - page.margin_bottom))
    page.layout = layout

    document.append(page)

    box = Box(document, page, {
        'box-class': 'main',
    })
    page.append(box)
    return document, page, box

