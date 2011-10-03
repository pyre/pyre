# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


class Cast:
    """
    A mix-in class that ensures node values have undergone special processing

    Implementation note: it is important to run the value through the processor during both
    {setValue} and {getValue} below. This guarantees that value changes that do not go through
    this interface will get processed properly on demand. For example, this enables {Cast} to
    coöperate with {Memo}, which caches the value and provides infrastructure for the dynamic
    re-calculation of expression graphs.
    """


    # public data
    processor = None


    # interface
    def getValue(self):
        """
        Intercept the node value retriever and make sure that the value the caller gets has
        been through my {processor}
        """
        # get the value
        value = super().getValue()
        # if I have a registered processor
        if self.processor is not None:
            # process it
            value = self.processor(value)
        # and return it
        return value


    def setValue(self, value, **kwds):
        """
        Intercept the value setter and make sure the value that gets stored has been through my
        {processor}
        """
        # if I have a registered processor
        if self.processor is not None:
            # process the value
            value = self.processor(value)
        # and store it
        return super().setValue(value=value, **kwds)


    # meta methods
    def __init__(self, processor=None, **kwds):
        super().__init__(**kwds)
        self.processor = processor
        return


# end of file 
