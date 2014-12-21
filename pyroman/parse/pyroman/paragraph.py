__author__ = 'johan'

import pyroman.parse.rst.paragraph

def parse_paragraph(content):
    content = content.replace('<b>', '*')
    content = content.replace('</b>', '*')
    content = content.replace('<i>', '**')
    content = content.replace('</i>', '**')
    content = content.replace('<code>', '`')
    content = content.replace('</code>', '`')
    for t in pyroman.parse.rst.paragraph.parse_paragraph(content):
        yield t
