from pyroman.pdf.document import Document, DocumentCatalog, next_id, \
    PageTreeNode, Page, Font
from pyroman.pdf.object import Dictionary, Array, Name, String
from pyroman.pdf.stream import Stream
from pyroman.pdf.content import TextObject
from pyroman.pdf.dimension import get_page_box


def convert(document):
    doc = Document()

    cat = DocumentCatalog(id=next_id())
    doc.body.put(cat)

    pages = PageTreeNode(id=next_id())
    page_list = Array()
    pages.Kids(page_list)
    doc.body.put(pages)
    cat.Pages(pages.reference)

    font_objects = []
    font_names = {}
    fc = 1
    for font_info in document.fonts:
        font_key = font_info.get('font-key')
        print(font_key)
        if font_key in font_names:
            continue
        name = Name('F%i' % fc)
        font = Font(id=next_id())
        font.BaseFont(Name(font_info.get('pdf')))
        font.Encoding("/WinAnsiEncoding")
        font.SubType("/Type1")
        font.Name(name)
        font_objects.append((name, font.reference))
        font_names[font_key] = name
        doc.body.put(font)
        fc += 1

    fonts = Dictionary(id=next_id())
    for font_name, reference in font_objects:
        fonts.put(font_name, reference)
    resources = Dictionary(id=next_id())
    resources.put("/Font", fonts.reference)

    doc.body.put(fonts)
    doc.body.put(resources)

    for page in document.children:
        pdf_page = Page(id=next_id())
        doc.body.put(pdf_page)
        page_list.put(pdf_page.reference)
        pdf_page.Parent(pages.reference)
        pdf_page.Resources(resources)
        pdf_page.MediaBox(get_page_box(page.dimension))

        pdf_page_contents = Stream(next_id())
        pdf_page_contents_length = 0

        for paragraph in page.paragraphs:
            text = TextObject()
            px, py = paragraph.absolute_position
            text.Td(px + paragraph.first_indent,
                    page.height - paragraph.absolute_base_line)
            for n, atom in enumerate(paragraph.atoms):
                text.Tf(font_names.get(atom.font_key), atom.font_size)
                if atom.beginning_of_line and n > 0:
                    text.Td(atom.indent, -atom.line_height)
                    text.Tw(atom.word_spacing)
                text.Tj(String(atom.content))
            pdf_page_contents.put(text)
            pdf_page_contents_length += len(text)

        pdf_page_contents.Length(pdf_page_contents_length)
        pdf_page.Contents(pdf_page_contents.reference)
        doc.body.put(pdf_page_contents)

    pages.Count(page_list.count)

    doc.trailer.Root(cat.reference)
    doc.trailer.Size(next_id())

    return doc
