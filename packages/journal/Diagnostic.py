# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


# packages
import traceback


# declaration
class Diagnostic:
    """
    Encapsulation of the message recording behavior of channels
    """


    # per-instance public data
    meta = None
    text = None


    # interface
    def line(self, message):
        """
        Add {message} to the diagnostic text
        """
        # check whether i am an active diagnostic
        if self.active:
            # add {message} to my text
            self.text.append(message)
        # and return
        return self


    def log(self, message=None, stackdepth=0):
        """
        Add the optional {message} to my text and make a journal entry
        """
        # bail if I am not active
        if not self.active: return self
        # if {message} is non-empty, add it to the pile
        if message is not None: self.text.append(message)

        # adjust the stack depth
        stackdepth += self.stackdepth

        # infer some more meta data
        trace = traceback.extract_stack()
        filename, line, function, source = trace[stackdepth]
        # decorate
        meta = self.meta
        meta["filename"] = filename
        meta["line"] = line
        meta["function"] = function
        meta["source"] = source

        # record
        self.device.record(page=self.text, metadata=meta)

        # and return
        return self


    # meta methods
    def __init__(self, name, **kwds):
        # chain to the ancestors
        super().__init__(name=name, **kwds)

        # initialize the list of message lines
        self.text = []
        # prime the meta data
        self.meta = {
            "name": name,
            "severity": self.severity
            }

        # all done
        return


    # implementation details
    # per class private data
    stackdepth = -2


# end of file 
