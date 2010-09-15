# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


from .Evaluator import Evaluator


class Function(Evaluator):
    """
    Base class for evaluators that have a domain, i.e., their value depends on the values of
    other nodes
    """


    # interface
    @property
    def domain(self):
        """
        Return an iterable over the nodes in my domain
        """
        raise NotImplementedError(
            "class {0.__class__.__name__!r} must override 'domain'".format(self))
        

    def validate(self, span, clean):
        """
        Check for faults
        """
        # loop over the nodes in my domain and ask them to do some checking
        for node in self.domain:
            # skip clean nodes
            if node in clean: continue
            # otherwise ask the node to check
            node.validate(span, clean)
        # all done
        return


    # life cycle management
    def initialize(self, owner):
        """
        Prepare to start computing
        """
        # add my owner to the list of observers of all the nodes in my domain
        for node in self.domain:
            node.addObserver(owner.flush)
        # and chain up
        return super().initialize(owner)


    def finalize(self, owner):
        """
        Shut down
        """
        # remove my owner from the list of observers of all the nodes in my domain
        for node in self.domain:
            node.removeObserver(owner.flush)
        # and chain up
        return super().finalize()


    # implementation details
    def _replace(self, old, new):
        """
        Patch my domain by replacing {old} with {new}.

        This is used by the model during node resolution. Please don't use directly unless you
        have thought the many and painful implications through
        """
        raise NotImplementedError(
            "class {0.__class__.__name__!r} must override '_replace'".format(self))


# end of file 
