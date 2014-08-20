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


def convert(processor):
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

    for o in processor.objects:
        if o.object_name == 'Paragraph':
            if o.content.startswith('= ') or o.content.startswith('.h1'):
                p = Paragraph(document, first_box, defaults['heading1'])
                c = o.content[2:-2]
            elif o.content.startswith('== ') or o.content.startswith('.h2'):
                p = Paragraph(document, first_box, defaults['heading2'])
                c = o.content[3:-3]
            elif o.content.startswith('=== ') or o.content.startswith('.h3'):
                p = Paragraph(document, first_box, defaults['heading3'])
                c = o.content[4:-4]
            elif o.content.startswith('==== ') or o.content.startswith('.h4'):
                p = Paragraph(document, first_box, defaults['heading4'])
                c = o.content[5:-5]
            elif o.content.startswith('===== ') or o.content.startswith('.h5'):
                p = Paragraph(document, first_box, defaults['heading5'])
                c = o.content[6:-6]
            elif (o.content.startswith('====== ') or
                  o.content.startswith('.h6')):
                p = Paragraph(document, first_box, defaults['heading6'])
                c = o.content[7:-7]
            elif (o.content.startswith('======= ') or
                  o.content.startswith('.h7')):
                p = Paragraph(document, first_box, defaults['heading7'])
                c = o.content[8:-8]
            else:
                p = Paragraph(document, first_box, defaults['text'])
                c = o.content
            p.content = c or ''
            first_box.append(p)
        elif o.object_name == 'Title':
            pt = Paragraph(document, first_box, defaults['title'])
            pt.content = o.arguments.get('title', '')
            first_box.append(pt)
            if o.arguments.get('subtitle') is not None:
                pst = Paragraph(document, first_box, defaults['subtitle'])
                pst.content = o.arguments.get('subtitle', '')
                first_box.append(pst)
            if o.arguments.get('author') is not None:
                pa = Paragraph(document, first_box, defaults['author'])
                pa.content = o.arguments.get('author', '')
                first_box.append(pa)
            if o.arguments.get('date') is not None:
                pd = Paragraph(document, first_box, defaults['date'])
                pd.content = o.arguments.get('date', '')
                first_box.append(pd)
        elif o.object_name == 'Code':
            code = Paragraph(document, first_box, defaults['code'])
            code.content = o.content
            first_box.append(code)

    orphans = first_box.calculate()

    while len(orphans) > 0:
        new_page, new_box = get_new_page(document, layout)
        new_box.children = orphans
        orphans = new_box.calculate()

    return document
