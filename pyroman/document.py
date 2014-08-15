from PIL import ImageFont

from .element import Element
from .parameters import Parameters

font_names = {
    'Courier': {
         'standard':    ('NimbusMonL-Regu', 'Courier'),
         'bold':        ('NimbusMonL-Bold', 'Courier-Bold'),
         'italic':      ('NimbusMonL-ReguObli', 'Courier-Oblique'),
         'bolditalic':  ('NimbusMonL-BoldObli', 'Courier-BoldOblique'),
    },
    'Helvetica': {
         'standard':    ('NimbusSanL-Regu', 'Helvetica'),
         'bold':        ('NimbusSanL-Bold', 'Helvetica-Bold'),
         'italic':      ('NimbusSanL-ReguItal', 'Helvetica-Oblique'),
         'bolditalic':  ('NimbusSanL-BoldItal', 'Helvetica-BoldOblique'),
    },
    'Times': {
         'standard':    ('NimbusRomNo9L-Regu', 'Times-Roman'),
         'bold':        ('NimbusRomNo9L-Medi', 'Times-Bold'),
         'italic':      ('NimbusRomNo9L-ReguItal', 'Times-Italic'),
         'bolditalic':  ('NimbusRomNo9L-MediItal', 'Times-BoldItalic'),
    },
    'Symbol': {
         'standard':    ('StandardSymL', 'Symbol'),
    },
    'Dingbats': {
         'standard':    ('Dingbats', 'ZapfDingbats'),
    },
}

class Document(Element):
    def __init__(self, params={}):
        super().__init__(params=params)

    def init(self):
        self.parameters = Parameters()
        all_params = self.parameters.get_defaults()
        all_params.update(self._params)
        self._params = all_params

        self.word_wrap = self._params.get('word-wrap')
        self.font_family = self._params.get('font-family')
        self.font_style = self._params.get('font-style')
        self.font_size = self._params.get('font-size')
        self.text_color = self._params.get('text-color')
        self.align = self._params.get('align')
        self.content = self._params.get('content', '')
        self.width = self._params.get('width')
        self.height = self._params.get('height')
        self.line_height = self._params.get('line-height')
        self.space_width = self._params.get('space-width')
        self.first_indent = self._params.get('first-indent')

        self._font_cache = {}

    def get_font(self, font_family, font_style, font_size):
        key = '%s-%s-%i' % (font_family, font_style, font_size)
        ttf, pdf = font_names.get(font_family, {}).get(font_style)
        if ttf is None:
            raise ValueError("No such font %s %s" % (font_family, font_style))
        font_info = self._font_cache.get(key, None)
        if font_info is None:
            font = ImageFont.truetype('fonts/%s.ttf' % ttf, font_size)
            self._font_cache[key] = {
                'font-key': '%s-%s' % (font_family, font_style),
                'font': font,
                'ttf': ttf,
                'pdf': pdf,
                'font-family': font_family,
                'font-style': font_style,
                'font-size': font_size,
            }
        else:
            font = font_info.get('font')
        return font

    @property
    def fonts(self):
        sent = []
        for k, font_info in self._font_cache.items():
            sent_key = "%s-%s" % (
                font_info.get('font-family'),
                font_info.get('font-style')
            )
            if not sent_key in sent:
                sent.append(sent_key)
                yield font_info

    def __repr__(self):
        return '<Document>'
