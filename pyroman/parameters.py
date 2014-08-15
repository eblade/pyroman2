from .constants import ALIGN_LEFT, ALIGN_RIGHT, ALIGN_CENTER, ALIGN_JUSTIFY


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
