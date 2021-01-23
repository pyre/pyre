# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2021 all rights reserved


class Composite:
    """
    Mix-in class that provides an implementation of the subset of the interface of {Node} that
    requires traversal of the expression graph rooted at nodes with dependencies.

    This class assumes that its instances provide {operands}, a tuple of their dependencies on
    other nodes
    """


    # types
    from .exceptions import CircularReferenceError


    # interface
    @property
    def operands(self):
        """
        A sequence of my direct dependents
        """
        # the default implementation stores my operands in a private member
        return self._operands


    @operands.setter
    def operands(self, operands):
        """
        Adjust my operands
        """
        # process the incoming sequence and save
        self._operands = self._store(self._ingest(operands=operands))
        # all done
        return


    @property
    def span(self):
        """
        Return a sequence over my entire dependency graph
        """
        # i am a node in my dependency graph
        yield self
        # go through my operands
        for operand in self.operands:
            # and ask them for their span
            yield from operand.span
        # all done
        return


    # classifiers
    @property
    def literals(self):
        """
        Return a sequence over the nodes in my dependency graph that encapsulate foreign objects
        """
        # go through my operands
        for operand in self.operands:
            # and ask them for literals in their span
            yield from operand.literals
        # all done
        return


    @property
    def operators(self):
        """
        Return a sequence over the composite nodes in my dependency graph
        """
        # i am one
        yield self
        # go through my operands
        for operand in self.operands:
            # and ask them for operators in their span
            yield from operand.operators
        # all done
        return


    @property
    def variables(self):
        """
        Return a sequence over the variables in my dependency graph
        """
        # go through my operands
        for operand in self.operands:
            # and ask them for variables in their span
            yield from operand.variables
        # all done
        return


    # structural classifiers
    @property
    def leaves(self):
        """
        Return a sequence over the leaves in my dependency graph
        """
        # go through my operands:
        for operand in self.operands:
            # and ask them for leaves in their span
            yield from operand.leaves
        # all done
        return


    @property
    def composites(self):
        """
        Return a sequence over the composites in my dependency graph
        """
        # i am one
        yield self
        # go through my operands:
        for operand in self.operands:
            # and ask them for leaves in their span
            yield from operand.composites
        # all done
        return


    # metamethods
    def __init__(self, operands, **kwds):
        # chain up
        super().__init__(**kwds)
        # save my direct dependencies
        self.operands = operands
        # all done
        return


    # implementation details
    def _ingest(self, operands):
        """
        Convert {operands} into nodes
        """
        # go through operands
        for operand in operands:
            # if this is not a node instance
            if not isinstance(operand, self.node):
                # make it a literal
                operand = self.literal(value=operand)
            # hand it off
            yield operand
        # all done
        return


    def _substitute(self, current, replacement, clean):
        """
        Adjust the operands by substituting {replacement} for {current} in the sequence of operands
        """
        # if i'm the one being replaced
        if current is self:
            # just return the {replacement}
            return replacement

        # if i'm among the {clean} nodes
        if self in clean:
            # do nothing
            return self

        # add me to the clean pile
        clean.add(self)

        # otherwise, make a pile for my potentially adjusted operands
        operands = []
        # initially, i am not known to have replaced any of my operands
        modified = False
        # go through my operands
        for op in self.operands:
            # if this one is marked {clean}
            if op in clean:
                # add it to the list of operands
                operands.append(op)
                # and carry on
                continue
            # otherwise, ask it to perform the substitution
            r = op._substitute(current=current, replacement=replacement, clean=clean)
            # add it or its replacement to the pile
            operands.append(r)
            # record whether an update was performed
            modified |= (r is not op)

        # if any substitutions were made
        if modified:
            # replace my operands
            self.operands = operands

        # all done
        return self


    # the default storage mechanism for operands
    _store = tuple
    # storage for the operands
    _operands = ()


# end of file
