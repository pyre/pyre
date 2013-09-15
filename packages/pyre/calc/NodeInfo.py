# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2013 all rights reserved
#


# declaration
class NodeInfo:
    """
    The base class for nodal metadata maintained by symbol tables
    """


    # public data
    key = None # the hashed version of the symbol name
    name = None # the string version of the symbol name
    split = None # the symbol name split on the table separator


    # meta-methods
    def __init__(self, model, key=None, name=None, split=None, **kwds):
        # chain up
        super().__init__(**kwds)
        # if we know both the full and split versions of the name
        if name and split:
            # save them
            self.name = name
            self.split = split
            # save the key
            self.key = key or model._hash.hash(items=split)
            # all done
            return
        # if we only know the name
        if name:
            # save it
            self.name = name
            # and form the split version
            split = tuple(model.split(name))
            # save it
            self.split = split
            # save the key
            self.key = key or model._hash.hash(items=split)
            # all done
            return
        # if i know the split version
        if split:
            # save it
            self.split = split
            # assemble the name
            self.name = model.join(split)
            # save the key
            self.key = key or model._hash.hash(items=split)
            # all done
            return

        # at the very least I should know the key
        if key:
            # save it
            self.key = key
            # and the rest get their default values
            self.name = name
            self.split = split
            # all done
            return

        # get the journal
        import journal
        # complain
        raise journal.firewall('pyre.calc').log('insufficient nodal metadata')


# end of file 
