from pyroman.paragraph import TextAtom

__author__ = 'johan'

def _create_atom(content, bold, italic, code):
    if len(content) > 0:
        t = TextAtom()
        t.content = content
        t.font_style = '%s%s' % ('bold' if bold else '', 'italic' if italic else '')
        t.font_family = 'Courier' if code else None
        return t
    else:
        return None


def parse_paragraph(content):
    """
    Parse a reStructuredText-formatted paragraph and yield a sequence of TextAtoms. Supported markups are `code`,
    *bold*, **italic** and ***bold italic***.

    :param str content: The content to parse
    :rtype: list of pyroman.paragraph.TextAtom
    """

    content = content.strip()
    length = len(content)
    current = ''
    bold = False
    italic = False
    code = False

    n = 0
    while n < length:
        c = content[n]
        cp = content[n+1] if (n < length - 1) else ''
        cpp = content[n+2] if (n < length - 2) else ''
        print((c, cp, cpp))
        if c in ' \t\n\r':
            t = _create_atom(current, bold, italic, code)
            current = ''
            if t is not None: yield t

        elif c == '*':
            t = _create_atom(current, bold, italic, code)
            current = ''
            if t is not None: yield t

            if cp == '*' and cpp == '*':
                if bold and italic:
                    bold = False
                    italic = False
                else:
                    bold = True
                    italic = True
                n += 2
            elif cp == '*':
                italic = not italic
                n += 1
            elif c == '*':
                bold = not bold

        elif c == '`':
            t = _create_atom(current, bold, italic, code)
            current = ''
            if t is not None: yield t

            code = not code

        else:
            current += c

        n += 1

    if len(current) > 0:
        t = TextAtom()
        t.content = current
        t.font_style = '%s%s' % ('bold' if bold else '', 'italic' if italic else '')
        t.font_family = 'Courier' if code else None
        yield t

def parse_code(content):
    current = ''
    for c in content:
        if c == ' ':
            t = TextAtom()
            t.content = ' '
            yield t
        elif c == ' ':
            t = TextAtom()
            t.content = ' '

