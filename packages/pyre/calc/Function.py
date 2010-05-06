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
    def validate(self, span, clean):
        """
        Check for faults
        """
        # loop over the nodes in my domain and ask them to do some checking
        for node in self.getDomain():
            node.validate(span, clean)
        # all done
        return


    def getDomain(self):
        """
        Return an iterable over the nodes in my domain
        """
        raise NotImplementedError(
            "class {0.__class__.__name__!r} must override 'getDomain'".format(self))


    # life cycle management
    def initialize(self, owner):
        """
        Prepare to start computing
        """
        # add me to the list of observers of all the nodes in my domain
        for node in self.getDomain():
            node.addObserver(self._flush)
        # and chain up
        return super().initialize(owner)


    def finalize(self):
        """
        Shut down
        """
        # remove me from the list of observers of all the nodes in my domain
        for node in self.getDomain():
            node.removeObserver(self._flush)
        # and chain up
        return super().finalize()


    # implementation details
    def _flush(self, node):
        """
        Callback invoked by the nodes in my domain to notify me that their values have changed
        """
        # pass the information on to my node
        return self._owner.flush()


    def _replace(self, name, old, new):
        """
        Patch my domain by replacing {old} with {new}.

        This is used by the model during node resolution. Please don't use directly unless you
        have thought the many and painful implications through
        """
        raise NotImplementedError(
            "class {0.__class__.__name__!r} must override '_replace'".format(self))


# end of file 
