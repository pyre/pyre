# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2017 all rights reserved
#


class Traversible:
    """
    Mix-in class that provides an implementation of the subset of the interface of {Node} that
    requires traversal of the expression graph rooted at nodes with dependencies.

    This class assumes that its instances provide {operands}, a tuple of their dependencies on
    other nodes
    """


    # types
    from .exceptions import CircularReferenceError


    # public data
    operands = ()


    @property
    def span(self):
        """
        Traverse my graph and yield all nodes in the graph
        """
        # i am one
        yield self
        # now, traverse my operands
        for operand in self.operands:
            # and ask them for their span
            yield from operand.span
        # all done
        return


    @property
    def variables(self):
        """
        Traverse my expression graph and yield all the variables in my graph

        Variables are reported as many times as they show up in my graph. Clients that are
        looking for the set unique dependencies have to prune the results themselves.
        """
        # traverse my operands
        for operand in self.operands:
            # and ask them for their dependencies
            yield from operand.variables
        # and no more
        return


    @property
    def operators(self):
        """
        Traverse my expression graph and yield all operators in my graph

        Operators are reported as many times as they show up in my graph. Clients that are
        looking for unique dependencies have to prune the results themselves.
        """
        # i am one
        yield self
        # now, traverse my operands
        for operand in self.operands:
            # and ask them for their operators
            yield from operand.operators
        # all done
        return


    # graph traversal
    def unique(self, encountered=None):
        """
        Traverse my expression graph and visit all nodes not previously {encountered}
        """
        # if I have been visited before, do nothing
        if self in encountered: return

        # otherwise, add me to the pile
        encountered.add(self)
        # visit all my operands
        for operand in self.operands:
            # and ask them for their unique nodes
            yield from operand.unique(encountered=encountered)

        # all done
        return


    # interface
    def substitute(self, current, replacement, clean=None):
        """
        Traverse my expression graph and replace all occurrences of node {current} with
        {replacement}.

        This method makes it possible to introduce cycles in the expression graph, which causes
        graph evaluation to not terminate. To prevent this, this method checks that I am not in
        the span of {replacement}.
        """
        # if this is the original substitution call
        if clean is None:
            # cycle detection: look for self in the span of {replacement}; do it carefully so
            # that we do not trigger a call to the overloaded __eq__, which does not actually
            # perform the comparison
            for node in replacement.span:
                # match?
                if node is self:
                    # the substitution would create a cycle
                    raise self.CircularReferenceError(node=self)
            # prime the set of clean nodes
            clean = { replacement }

        # now, iterate over composites in my subgraph
        for node in self.operators:
            # skip nodes that we have visited before
            if node in clean: continue
            # otherwise, perform the substitution
            node._substitute(current=current, replacement=replacement)
            # mark this node as clean
            clean.add(node)

        # all done
        return


# end of file
