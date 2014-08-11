from pyroman.pdf.document import Document, DocumentCatalog, next_id, PageTreeNode, Page, Font
from pyroman.pdf.object import Dictionary, Array, Rectangle, Name, String
from pyroman.pdf.stream import Stream
from pyroman.pdf.content import TextObject
from pyroman.pdf.dimension import A4, MarginDefault, get_page_box, cm_to_points


def convert(document):
    doc = Document()

    cat = DocumentCatalog(id=next_id())
    doc.body.put(cat)

    pages = PageTreeNode(id=next_id())
    page_list = Array()
    pages.Kids(page_list)
    doc.body.put(pages)
    cat.Pages(pages.reference)

    name_helvetica = Name("F1")
    name_helvetica_bold = Name("F2")
    font_helvetica = Font(next_id())
    font_helvetica.BaseFont("/Helvetica")
    font_helvetica.Encoding("/WinAnsiEncoding")
    font_helvetica.SubType("/Type1")
    font_helvetica.Name(name_helvetica)
    font_helvetica_bold = Font(next_id())
    font_helvetica_bold.BaseFont("/Helvetica-Bold")
    font_helvetica_bold.Encoding("/WinAnsiEncoding")
    font_helvetica_bold.SubType("/Type1")
    font_helvetica_bold.Name(name_helvetica_bold)

    fonts = Dictionary(next_id())
    fonts.put(name_helvetica, font_helvetica.reference)
    fonts.put(name_helvetica_bold, font_helvetica_bold.reference)

    resources = Dictionary(next_id())
    resources.put("/Font", fonts.reference)

    doc.body.put(font_helvetica)
    doc.body.put(font_helvetica_bold)
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
        
        for atom in page.atoms:
            text = TextObject()
            text.Font(name_helvetica_bold, 12)
            text.Position(atom.x, page.height - atom.y)
            text.Text(String(atom.content))
            pdf_page_contents.put(text)
            pdf_page_contents_length += len(text)

        pdf_page_contents.Length(pdf_page_contents_length)
        pdf_page.Contents(pdf_page_contents.reference)
        doc.body.put(pdf_page_contents)
            
    pages.Count(page_list.count)

    doc.trailer.Root(cat.reference)
    doc.trailer.Size(next_id())
        
    return doc
