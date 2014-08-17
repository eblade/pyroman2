import re

from pyroman.utils import getkey, varsub

## @class Generic
#
# Describes a Generic  Object with standard methods. All special object
# classes must inherit the Generic class.
class Generic:

    ## @fn __init__
    #
    # Generic initialisation
    #
    # @param _globalvars Array pointer to the processor's global vars
    # @param _source Array of lines of source code
    # @param _is_first Set true if this is the first object in the document
    # 
    # @return Generic object
    def __init__(self, _globalvars = {},_source=None, _is_first=False, _is_main_file=True, _filepath='', _lineno=0):
        self.object_name = 'None'
        self.arguments = {}
        self.content = ''
        self.is_first = _is_first
        self.is_main_file = _is_main_file
        self.needs_rerun = False
        self.localvars = {}
        self.globalvars = _globalvars 
        self.sub_objects = []
        self.lines = [] # store the source lines
        self.filepath = _filepath
        self.lineno = _lineno

        # Output stuff
        self.removed = False 
        self.body = ''
        self.style = ''
        self.prescript = ''
        self.script = ''

        if (_source):
            self.from_array(_source)
    
    ## @fn getid
    #
    # Gets the unique id for this object
    def getid(self):
        return self.id

    ## @fn from_array
    #
    # Generates data structure from a line array
    #
    # @param _source Array of lines of source code
    #
    # @return True if process succeeded
    def from_array(self, _source):
        self.lines = _source
        first_line = True
        done_with_arguments = False
        re_def = '^([A-Za-z0-9]+?):'
        for line in _source:
            if first_line:
                parts = re.match(re_def, line)
                if (not parts):
                    if self.is_first and self.is_main_file: # Special fallback for first object as title
                        self.object_name = 'Title'
                        self.arguments['title'] = line
                    else:
                        self.object_name = 'Paragraph' # fallback, but can also be SyntaxSugar
                        self.content = line
                        done_with_arguments = True
                else:
                    self.object_name = parts.group(1)
                    self.arguments['primary'] = line[len(self.object_name)+2:].strip()
                first_line = False
            else: # not first line
                if not done_with_arguments:
                    if (line == '-'): # use - as separetor if contents start with argoid line
                        done_with_arguments = True
                    else:
                        parts = re.match(re_def, line)
                        if (not parts):
                            if self.is_first: # Special fallback for first object as subtitle
                                self.arguments['subtitle'] = line
                            else:
                                self.content = ''.join([self.content,'\n',line])
                                done_with_arguments = True
                        else:
                            self.arguments[parts.group(1)] = line[len(parts.group(1))+2:].strip()
                else:
                    self.content = ''.join([self.content,'\n',line])
        self.upgrade()
        return True

    ## @fn upgrade
    #
    # Upgrade from the base object class to a specialised variant (if there is any)
    #
    # @return True upon success
    def upgrade(self):
        class_name = self.object_name
        if class_name == 'vim':
            return False
        if class_name is 'Input':
            self.__class__ = Input
        self.post_upgrade()
        return True

    ## @fn process
    #
    # Processes the template with data from the hashes. Builds a text representation
    # of the object using the templates.
    def process(self):
        template_name = getkey(self.arguments, 'template', self.object_name)
        template = getkey(self.globalvars['$Templates'], template_name)
        self.body = getkey(template, 'body')
        self.pre_process()

        self.body = self.body.replace('%content%', self.content)
        
        self.body = varsub(self.body, 
                           [self.localvars,
                           self.arguments,
                           self.globalvars],
                           getkey(self.globalvars, '$Templates', False),
                           recursive=getkey(self.arguments, 'substitute', 'yes') != 'no')
    
    ## @fn pre_process
    #
    # Generic Pre-process function   
    #
    # @param _template The template content
    #
    # @return No returns, only altering of object and/or global vars
    def pre_process(self):
        return
    
    ## @fn post_process
    #
    # Generic Post-process function   
    #
    # @param _template The template content
    #
    # @return No returns, only altering of object and/or global vars
    def post_process(self):
        return
    
    ## @fn post_upgrade
    #
    # Generic Post-Upgrade function   
    #
    # @param _template The template content
    # @param _globals Hash of global variables
    #
    # @return No returns, only altering of object and/or global vars
    def post_upgrade(self):
        return
    
    ## @fn setup
    #
    # @return dummy setup function
    def setup(self):
        return

    ## @fn transform
    #
    # @return recreates itselft from the sourcelines
    def transform(self):
        self.from_array(self.lines)
        return

    ## @fn process_inline (override to use inline syntax sugars)
    #
    # @return No returns
    def process_inline(self):
        return

    ## @fn dump
    #
    # @return textual representation of object contents
    def dump(self):
        l_object_name = ''.join(['object_name: ',self.object_name])
        l_removed = ''.join(['removed: ',str(self.removed)])
        l_needs_rerun = ''.join(['needs_rerun: ',str(self.needs_rerun)])
        l_sourcelines = ' - SOURCELINES - '
        for l in self.lines:
            l_sourcelines = '\n'.join([l_sourcelines, l])
        l_arguments = ' - ARGUMENTS - '
        for l in self.arguments:
            l_arguments = '\n'.join([l_arguments, ' = '.join([l, self.arguments[l]])])
        l_localvars = ' - LOCALVARS - '
        for l in self.localvars:
            l_localvars = '\n'.join([l_localvars, ' = '.join([l, self.localvars[l]])])
        l_content = '\n'.join([' - CONTENT - ', self.content])
        l_body = '\n'.join([' - BODY - ', self.body])
        l_style = '\n'.join([' - STYLE - ', self.style])
        l_prescript = '\n'.join([' - SCRIPT - ', self.prescript])
        l_script = '\n'.join([' - SCRIPT - ', self.script])
        return '\n'.join([l_object_name,
                          l_removed,
                          l_needs_rerun,
                          l_sourcelines,
                          l_arguments,
                          l_localvars,
                        # l_globalvars,
                          l_content,
                          l_body,
                          l_style,
                          l_script,
                          ])

