from .generic import Generic
from .processor import Processor


class Input(Generic):
    def __init__(self):
        super(Input, self).__init__()
        self.init()
    
    # An Input Object must load all subobjects so that they can be included
    # in the main object list.
    def pre_process(self):
        filename = getkey(self.arguments,'primary', False)
        if not filename:
            return
        p = None
        if os.path.isfile(getkey(self.globalvars,'root')+filename):
            p = Processor(getkey(self.globalvars,'root'), filename, _is_main_file=False)
        if os.path.isfile(getkey(self.globalvars,'root')+'templates/'+filename):
            p = Processor(getkey(self.globalvars,'root')+'templates/', filename, _is_main_file=False)
        elif os.path.isfile(getkey(self.globalvars,'templatedir')+filename):
            p = Processor(getkey(self.globalvars,'templatedir'), filename, _is_main_file=False)
        elif os.path.isfile(G.template_dir+filename):
            p = Processor(G.template_dir, filename, _is_main_file=False)
        else:
            return

        # Use the uppermost globalvars dictionary
        p.globalvars = self.globalvars

        # Load the objects
        if p.init_file():
            p.load_objects()
            p.close_file()
        
        # Copy objects from the processor to the object
        self.sub_objects = p.objects

        self.removed = True

    def get_text():
        return ''

