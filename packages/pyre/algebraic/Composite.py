# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


class Composite:
    """
    Mix-in class that provides an implementation of the subset of the interface of {Node} that
    requires traversal of the expression graph rooted at nodes with dependencies.

    This class assumes that its instances provide {_operands}, a tuple of their dependencies on
    other nodes
    """


    # types
    from .exceptions import CircularReferenceError


    # public data
    @property
    def variables(self):
        """
        Traverse my expression graph and return an iterable with all the variables I depend on
        """
        # traverse my operands
        for operand in self._operands:
            # and ask them for their dependencies
            for node in operand.variables:
                # return whatever it discovered
                yield node
        # and no more
        return


    # interface
    def validate(self, span=None, clean=None):
        """
        Make sure that the subgraph rooted at me is free of cycles

        parameters:
            {span}: the set of nodes previously visited; if i am in this set, there are cycles
            {clean}: the set of nodes known to be cycle free because they were previously cleared
        """
        # initialize my optional parameters
        span = set() if span is None else span
        clean = set() if clean is None else clean
        # if i am in the span
        if self in span:
            # we have a cycle
            raise self.CircularReferenceError(node=self, path=span)
        # if i am clean
        if self in clean:
            # go no further
            return self
        # so far so good; add me to the span
        span.add(self)
        # and visit my operands
        for operand in self._operands:
            # ask each one to validate its subgraph
            operand.validate(span=span, clean=clean)
        # if i made it this far without an exception being raised, i must be clean
        # so add myself to the clean pile
        clean.add(self)
        # and return
        return self



    def substitute(self, replacements):
        """
        Look through the dictionary {replacements} for any of my operands and replace them with
        the indicated nodes.
        """
        operands = []
        # look through my operands
        for operand in self._operands:
            # does this one show up in the replacement map?
            if operand in replacements:
                # push its replacement to the new operand list
                operands.append(replacements[operand])
            # otherwise
            else:
                # push it
                operands.append(operand)
                # and hand it the replacement list
                operand.substitute(replacements)
        # install the new operands
        self._operands = tuple(operands)
        # and return
        return
                    

    # private data
    _operands = ()

# end of file 
