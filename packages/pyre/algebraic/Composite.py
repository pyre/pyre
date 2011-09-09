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
        Traverse my expression graph and yield all the variables in my graph

        Variables are reported as many times as they show up in my graph. Clients that are
        looking for the set unique dependencies have to prune the results themselves.
        """
        # traverse my operands
        for operand in self._operands:
            # and ask them for their dependencies
            for node in operand.variables:
                # return whatever it discovered
                yield node
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
        for operand in self._operands:
            # and ask them for their operators
            for node in operand.operators:
                # got one
                yield node
        # all done
        return


    # interface
    def substitute(self, current, replacement):
        """
        Traverse my expression graph and replace all occurrences of node {current} with
        {replacement}.

        This method makes it possible to introduce cycles in the expression graph
        inadvertently. It is the client's responsibility to make sure that the graph remains
        cycle-free.
        """
        # cycle detection: iterate over the composites in the subgraph of {replacement}
        for node in replacement.operators:
            # looking for me
            if node is self:
                # in which case, the substitution would create a cycle
                raise self.CircularReferenceError(node=self)

        # marker for nodes that are known not to depend on {replacement}
        clean = { replacement }
        # now, iterate over composites in my subgraph
        for node in self.operators:
            # if we have visited this guy before
            if node in clean:
                # skip it
                continue
            # look over their operands
            for index, operand in enumerate(node._operands):
                # if one of them is our target
                if operand is current:
                    # replace it
                    node._operands[index] = replacement
            # mark this node as clean
            clean.add(node)        
            
        # all done
        return
                    

# end of file 
