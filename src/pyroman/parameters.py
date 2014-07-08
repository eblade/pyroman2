from .constants import *

class Parameters:
    def __init__(self):
        self.parameters = {
            'word-wrap': {'type': bool, 'default': True},
            'align': {'type': str, 'default': ALIGN_LEFT},
            'font-family': {'type': str, 'default': 'Ubuntu-R'},
            'font-size': {'type': int, 'default': 12},
            'text-color': {'type': str, 'default': '#000000'},
            'max-width': {'type': int, 'default': None},
            'max-height': {'type': int, 'default': None},
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
        return {p: p.get('default', None) for p in self.parameters}
