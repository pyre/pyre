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
    from .exceptions import (
        NodeError,
        CircularReferenceError,
        EmptyExpressionError, ExpressionSyntaxError, EvaluationError,
        UnresolvedNodeError
        )

    # hooks for implementing the expression graph construction
    # the default implementation provided by this package uses the classes defined here
    # access is provided through properties to hide the {import} of subclasses
    # functional
    @property
    def literal(self):
        """
        Grant access to the subclass used to encapsulate foreign values
        """
        # important: must return a type, not an instance
        raise NotImplementedError(
            "class {.__name__!r} must implement 'literal'".format(type(self)))


    @property
    def variable(self):
        """
        Grant access to the subclass used to encapsulate expression nodes
        """
        # important: must return a type, not an instance
        # important: must return a type, not an instance
        raise NotImplementedError(
            "class {.__name__!r} must implement 'variable'".format(type(self)))


    @property
    def operator(self):
        """
        Grant access to the subclass used to encapsulate operators
        """
        # important: must return a type, not an instance
        raise NotImplementedError(
            "class {.__name__!r} must implement 'operator'".format(type(self)))


    @property
    def expression(self):
        """
        Grant access to the subclass used to encapsulate strings that contain named references
        to other nodes. These references get resolved by a symbol table.
        """
        # important: must return a type, not an instance
        raise NotImplementedError(
            "class {.__name__!r} must implement 'expression'".format(type(self)))


    @property
    def interpolation(self):
        """
        Grant access to the subclass used to encapsulate strings that contain named references
        to other nodes. These references get resolved by a symbol table.
        """
        # important: must return a type, not an instance
        raise NotImplementedError(
            "class {.__name__!r} must implement 'interpolation'".format(type(self)))


    @property
    def reference(self):
        """
        Grant access to the subclass used to encapsulate references to other nodes
        """
        # important: must return a type, not an instance
        raise NotImplementedError(
            "class {.__name__!r} must implement 'operator'".format(type(self)))


    @property
    def unresolved(self):
        """
        Grant access to the subclass used to encapsulate unresolved nodes
        """
        # important: must return a type, not an instance
        raise NotImplementedError(
            "class {.__name__!r} must implement 'unresolved'".format(type(self)))


    # structural
    @property
    def leaf(self):
        """
        Grant access to the mix-in class used to build leaf nodes
        """
        # important: must return a type, not an instance
        raise NotImplementedError("class {.__name__!r} must implement 'leaf'".format(type(self)))


    @property
    def composite(self):
        """
        Grant access to the subclass used to build composite node
        """
        # important: must return a type, not an instance
        raise NotImplementedError(
            "class {.__name__!r} must implement 'operator'".format(type(self)))


    # public data
    # value access
    @property
    def value(self):
        """
        Compute and return my value
        """
        # delegate to my interface
        return self.getValue()


    @value.setter
    def value(self, value):
        """
        Set my value
        """
        # delegate to my interface
        return self.setValue(value)


    # by default both read and write access is disabled
    def getValue(self):
        """
        Return my value
        """
        # disabled
        raise NotImplementedError(
            "class {.__class__.__name__!r} does not support 'getValue'".format(self))


    def setValue(self, value):
        """
        Disable value setting
        """
        # disabled
        raise NotImplementedError(
            "class {.__class__.__name__!r} does not support 'setValue'".format(self))


    # interface
    def ref(self, **kwds):
        """
        Build and return a reference to me
        """
        return self.reference(operands=[self], **kwds)


    # default implementations for value management
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


    # implementation support
    @classmethod
    def select(cls, model, existing, replacement):
        """
        Pick either {existing} or {replacement} as the node that will remain in {model}
        """
        # by default, {replacement} always wins
        return replacement.replace(existing)


    # debugging support
    def dump(self, name, indent):
        print('{}{}: {}'.format(indent, name, self.value))
        return self
        

# end of file 
