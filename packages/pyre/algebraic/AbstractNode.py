# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# declaration
class AbstractNode:
    """
    The base class for hierarchies that implement the algebraic protocol

    The mix-in classes {Arithmetic}, {Ordering} and {Boolean} overload the methods that are invoked
    by the evaluation of expressions involving python operators. The implementation of these
    methods expect {AbstractNode} subclasses to provide access to two subclasses, {Literal} and
    {Operator}, that are used to build a representation of the python expression. {Literal} is
    used to encapsulate objects that are foreign to the {Node} class hierarchy, e.g. integers,
    and {Operation} encodes the operator encountered and its operands. This access must be
    provided through two {Node} properties, {literal} and {operation}, which provide an extra
    layer of abstraction by hiding the actual {Node} subclasses.
    """


    # exceptions; included here for client convenience
    from .exceptions import NodeError, CircularReferenceError


    # hooks for implementing the expression graph construction
    # structural
    leaf = None # nodes with no dependencies to other nodes
    composite = None # nodes with dependencies to other nodes

    # the node types
    literal = None # nodes that capture foreign values
    variable = None # base class my native nodes 
    operator = None # operations among my native nodes


    # interface
    def replace(self, obsolete):
        """
        Take ownership of any information held by the {obsolete} node, which is about to be
        destroyed
        """
        # print("AbstractNode.replace:")
        # print("    self:", self)
        # print("        span:", tuple(self.span))
        # print("    obsolete:", obsolete)
        # print("        span:", tuple(obsolete.span))
        # protection against circular references: verify that {obsolete} is not in my span by
        # iterating over all nodes. this must be done carefully so as not to trigger the
        # overloaded operator __eq__
        for node in self.span:
            # if it matches {obsolete} 
            if node is obsolete:
                # report the error
                raise self.CircularReferenceError(node=obsolete)
        # all done
        return self


# end of file 
