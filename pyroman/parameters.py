from .constants import ALIGN_LEFT, ALIGN_RIGHT, ALIGN_CENTER, ALIGN_JUSTIFY

defaults = {
    'text': {
        'font-family': 'Times',
        'font-size': 11,
        'margin-top': 5,
        'margin-bottom': 10,
        'first-indent': 0,
    },
    'title': {
        'font-family': 'Helvetica',
        'font-style': 'bold',
        'font-size': 32,
        'margin-top': 40,
        'margin-bottom': 10,
    },
    'subtitle': {
        'font-family': 'Helvetica',
        'font-style': 'bold',
        'font-size': 16,
        'margin-top': 10,
        'margin-bottom': 20,
    },
    'author': {
        'font-family': 'Times',
        'font-style': 'bold',
        'font-size': 12,
        'margin-top': 20,
        'margin-bottom': 10,
    },
    'date': {
        'font-family': 'Times',
        'font-size': 12,
        'margin-bottom': 30,
    },
    'code': {
        'font-family': 'Courier',
        'font-size': 10,
        'margin-bottom': 10,
        'margin-bottom': 10,
        'preformatted': True,
    },
    'heading1': {
        'font-family': 'Helvetica',
        'font-style': 'bold',
        'font-size': 24,
        'margin-top': 30,
        'margin-bottom': 20,
        'min-after': 50,
    },
    'heading2': {
        'font-family': 'Helvetica',
        'font-style': 'bold',
        'font-size': 20,
        'margin-top': 20,
        'margin-bottom': 15,
        'min-after': 50,
    },
    'heading3': {
        'font-family': 'Helvetica',
        'font-style': 'bold',
        'font-size': 16,
        'margin-top': 20,
        'margin-bottom': 15,
        'min-after': 50,
    },
    'heading4': {
        'font-family': 'Helvetica',
        'font-style': 'bold',
        'font-size': 12,
        'margin-top': 20,
        'margin-bottom': 15,
        'min-after': 50,
    },
    'heading5': {
        'font-family': 'Times',
        'font-style': 'bold',
        'font-size': 11,
        'margin-top': 10,
        'margin-bottom': 10,
        'min-after': 50,
    },
    'heading6': {
        'font-family': 'Times',
        'font-style': 'bolditalic',
        'font-size': 11,
        'margin-top': 10,
        'margin-bottom': 10,
        'min-after': 50,
    },
    'heading7': {
        'font-family': 'Times',
        'font-style': 'italic',
        'font-size': 11,
        'margin-top': 10,
        'margin-bottom': 10,
        'min-after': 50,
    },
    'bullet': [
        ('Helvetica', 'bold', 12, '*'),
        ('Helvetica', 'bold', 12, '+'),
        ('Helvetica', 'standard', 12, '-'),
        ('Helvetica', 'standard', 12, '...'),
        ('Helvetica', 'standard', 12, ':'),
        ('Helvetica', 'standard', 12, '.'),
        ('Helvetica', 'standard', 12, ','),
    ],
}
        

class Parameters:
    def __init__(self):
        self.parameters = {
            'word-wrap': {'type': bool, 'default': True},
            'align': {'type': str, 'default': ALIGN_LEFT},
            'font-family': {'type': str, 'default': 'Helvetica'},
            'font-style': {'type': str, 'default': 'standard'},
            'font-size': {'type': int, 'default': 12},
            'text-color': {'type': str, 'default': '#000000'},
            'max-width': {'type': int, 'default': None},
            'max-height': {'type': int, 'default': None},
            'line-height': {'type': float, 'default': 1.2},
            'space-width': {'type': int, 'default': 3},
            'first-indent': {'type': int, 'default': 0},
            'input-format': {'type': str, 'default': 'pyroman'},
        }

    def get_default(self, field):
        p = self.parameters.get(field)
        if p is None:
            return None
        return p.get('default', None)

    def get_type(self, field):
        p = self.parameters.get(field)
        if p is None:
            return None
        return p.get('type', str)

    def get_defaults(self):
        return {n: p.get('default', None) for n, p in self.parameters.items()}

    # to make it picklable
    def __getstate__(self):
        odict = self.__dict__.copy()
        odict['class'] = self.__class__.__name__
        internals = [k for k in odict.keys() if k.startswith('_')]
        for k in internals:
            del odict[k]
        return odict
