import json


def dumps(o, indent=2):
    return json.dumps(o, indent=2, default=picklable, sort_keys=True)


def picklable(o):
    if hasattr(o, '__getstate__') and callable(o.__getstate__):
        return o.__getstate__()
    else:
        return o

def dumph(o, current_indentation=0):
    output = '  '*current_indentation + repr(o)
    if hasattr(o, 'children') and len(o.children):
        output += ':\n'
        for child in o.children:
            output += dumph(child, current_indentation + 1)
    else:
        output += '\n'
    return output
