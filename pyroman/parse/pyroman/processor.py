import sys
import io
import datetime

from pyroman.utils import getkey, varsub
from .generic import Generic


## @class Processor
# 
# This class takes a filename, processes it using objects and split out 
# output. 
class Processor:
    ## @fn __init__
    #
    # The initialiser for the Processor class
    #
    # @param _root The root folder where the file is
    # @param _filename The filename part of the path
    def __init__(self, _root, _filename, _is_main_file=True):
        self.root = _root
        self.filename = _filename
        self.filepath = '' # calculated by get_line()
        self.is_main_file = _is_main_file
        self.globalvars = {'root': _root, 'filename': _filename} # A hash for storing document data while processing
        self.finished_once = False # The processing needs to be done several times
        self.objects = [] # The sequence of objects that makes the document
        self.process_queue = [] # A list of objects that need to be processed again
        self.document = 'unproduced'
        self.lineno = 0 # line number in file, incremented by get_line()
        
        # SyntaxSugar 
        self.globalvars['$SyntaxSugar'] = []

        # Templates
        self.globalvars['$Templates'] = {} 

        # Labels
        self.globalvars['$Labels'] = {} 
    
    ## @fn init_file
    # 
    # Open the file and store the pointer to the object
    #
    # @return True on success, False on failure
    def init_file(self):
        self.first_lines = []  #list(getkey(first_lines, self.output, [])) if self.is_main_file else []
        self.filepath = ''.join([self.root,self.filename])
        self.lineno = 0
        try:
            self.file = io.open(self.filepath, 'r')
        except IOError:
            return False
        else:
            return True
    
    ## @fn get_line 
    # 
    # Get the next line
    #
    # @return The line as a string
    def get_line(self):
        if len(self.first_lines):
            self.doing_first_lines = True
            return self.first_lines.pop(0) # shift
        if self.doing_first_lines:
            self.first_object = True
            self.doing_first_lines = False
        try:
            line = self.file.readline()
            self.lineno += 1
        except IOError:
            return ''
        else:
            return line
    
    ## @fn close_file
    # 
    # Close the file opened for process
    #
    # @return True on success, False on failure
    def close_file(self):
        try:
            self.file.close()
        except IOError:
            return False
        else:
            return True
    
    ## @fn load_objects
    # 
    # Reads file line by line and strips out objects.
    def load_objects(self):
        self.doing_first_lines = True
        self.first_object = True # First object will be treated differently
        last_line = False # A flag for last line (eof) detection
        lines = [] # A object line buffer, cleared after each object stored
        object_start_line = 0 # line number of object start
        while (True):
            next_line = self.get_line()
            # Detect last line before stripping away te \n
            if len(next_line) == 0:
                last_line = True
            next_line = next_line.strip('\n\r')

            # Check if it is an empty line, if so, finish object
            if not next_line:
                if len(lines):
    
                    # Create a Generic Object that can later be upgraded
                    obj = Generic(self.globalvars, lines, self.first_object, 
                        self.is_main_file, _filepath=self.filepath,
                        _lineno=object_start_line)
    
                    # Prepare for next round and save the current object
                    lines = []
                    if not self.doing_first_lines:
                        self.first_object = False
    
                    if not obj.removed:
                        self.objects.append(obj)

                object_start_line = self.lineno + 1
            else:
                lines.append(next_line)
                #lines.append(next_line.strip())
            if last_line:
                return

    ## @fn preprocess_objects
    #
    # Loops through the object list until there are no objects left to (re)propress
    # Takes care of Input and Use objects before general processing
    # and puts all other objects in the process queue for later handling
    def preprocess_objects(self):
        rerun = True
        turn_count = 0
        while (rerun and turn_count < 100):
            turn_count += 1
            rerun = False
            i = 0
            o = len(self.objects)
            while i < o:
                obj = self.objects[i]
                if obj.object_name in ['Input']:
                    obj.process()
                    s = len(obj.sub_objects)
                    if s > 0: # if there are subobjects in object
                        result = []
                        for j in range(0, i):
                            result.append(self.objects[j])
                        for j in range(0, s):
                            result.append(obj.sub_objects[j])
                        for j in range(i+1, o):
                            result.append(self.objects[j])
                        self.objects = result
                        i -= 1
                        o += s - 1
                elif 'Wrapper' in obj.object_name:
                    pass  # The wrapper is omitted in the process queue
                else:
                    self.process_queue.append(obj)
                i += 1
    
    ## @fn process_objects_for_syntax_sugar
    #
    # Loops through the object list until there are no objects left to (re)propress
    # Takes care of Input and Use objects before general processing
    # and puts all other objects in the process queue for later handling
    def process_objects_for_syntax_sugar(self):
        for obj in self.objects:
            # SyntaxSugar translation (for paragraphs, which is the fallback object type)
            if obj.object_name == "Paragraph" and len(obj.lines):    
                if '$SyntaxSugar' in self.globalvars:
                    for sugar in self.globalvars['$SyntaxSugar']:
                        if not sugar.broken:
                            if sugar.translate(obj.lines[0]):
                                obj.content = '' # clear object content from old syntax sugar
                                obj.lines.pop(0)
                                obj.lines[:0] = sugar.result
                                obj.transform() # reload object from new source
            obj.process_inline()
                        
            # Look for %Inlineobject% things and add those at the end of the document
            # This must also create a hash $InlineObjects with the keys as hashes of
            # the inline call. Those hashes are later used for inline varsub
            # The proccess will be recursicve since the Inline objects are added last
            # to the object queue.
            #
            # This code must both look for correct inline object definitions as well
            # as the costumizable short forms, which should be stored as SyntaxSugars in
            # a special hash $InlineSyntaxSugar.

    ## @fn process_object_queue
    #
    # Loops through the object list until there are no objects left to (re)propress
    def process_object_queue(self):
        subprocessors = getkey(self.globalvars, '$Subprocessors', [])
        while(len(self.process_queue)):
            obj = self.process_queue.pop(0)
            if not obj.removed:
                for sp in subprocessors:
                    new_objects = sp.run(obj)
                    if len(new_objects):
                        for no in new_objects:
                            self.objects.append(no)
                            self.process_queue.append(no)
                        obj.needs_rerun = True
                obj.process()
                if obj.needs_rerun:
                    self.process_queue.append(obj)

    ## @fn generate
    # 
    # A aggregate wrapper that calls all functions needed to generate the output.
    # This is the interface to the user application.
    # 
    # @param _template The template name (without path)
    #
    # @return True on success, False on failure
    def generate(self):
        # Store todays date
        self.globalvars['today'] = str(datetime.date.today())

        if not self.init_file():
            return False
        self.load_objects()
        self.close_file()
        self.preprocess_objects()
        self.process_objects_for_syntax_sugar()
        self.process_object_queue()
        #self.perform_wrapping()

    ## @fn get_objects_as_strings
    #
    # Concatenates all objects' types and primaries and returns them
    #
    # @return Text represenation of all objects
    def get_objects_as_string(self):
        output = ''
        for obj in self.objects:
            output = '\n'.join([output, '============================================',obj.dump()])
        return output
