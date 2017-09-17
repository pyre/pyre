# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2017 all rights reserved
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
    variable = None # the base class of my native nodes
    operator = None # operations among my native nodes


    # interface
    # graph traversal
    @property
    def operands(self):
        """
        A sequence of my direct dependents
        """
        # by default, empty
        return ()


    @property
    def span(self):
        """
        Return a sequence over my entire dependency graph
        """
        # by default, empty
        return ()


    # node classifiers
    @property
    def variables(self):
        """
        Return a sequence over the leaf nodes in my dependency graph
        """
        # by default, empty
        return ()


    @property
    def operators(self):
        """
        Return a sequence over the composite nodes in my dependency graph
        """
        # by default, empty
        return ()


    @property
    def literals(self):
        """
        Return a sequence over the nodes in my dependency graph that encapsulate foreign objects
        """
        # by default, empty
        return ()


    # interface
    def replace(self, obsolete):
        """
        Take ownership of any information held by the {obsolete} node, which is about to be
        destroyed

        At this level, there is no mechanism for performing the actual replacement. The node
        interface guarantees that i can compute my {span}, so all i can do is check for whether
        the obsolete node shows up in my upstream graph.
        """
        # print("AbstractNode.replace:")
        # print("    self:", self)
        # print("        span:", tuple(self.span))
        # print("    obsolete:", obsolete)
        # print("        span:", tuple(obsolete.span))

        # smarter nodes may know how to do this; assuming the clean up has already taken place
        # by the time they chain here, let's verify that it was done correctly and {obsolete}
        # is not in my span; this must be done carefully so as not to trigger operator {__eq__},
        # which may be overloaded by the {boolean} mixin
        for node in self.span:
            # if it matches {obsolete}
            if node is obsolete:
                # report the error
                raise self.CircularReferenceError(node=obsolete)
        # all done
        return self


    # implementation details
    _pyre_hasAlgebra = False


    # debugging support
    def dump(self, name, indent):
        print('{}{}: {}'.format(indent, name, self.value))
        return self


# end of file
