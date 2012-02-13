# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


# declaration
class AbstractNode:
    """
    The base class for hierarchies that implement the algebraic protocol

    The mix-in classes {Number}, {Ordering} and {Boolean} overload the methods that are invoked
    by the evaluation of expressions involving python operators. The implementation of these
    methods expect {AbstractNode} subclasses to provide access to two subclasses, {Literal} and
    {Operator}, that are used to build a representation of the python expression. {Literal} is
    used to encapsulate objects that are foreign to the {Node} class hierarchy, e.g. integers,
    and {Operation} encodes the operator encountered and its operands. This access must be
    provided through two {Node} properties, {literal} and {operation}, which provide an extra
    layer of abstraction by hiding the actual {Node} subclasses.
    """


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
    @property
    def value(self):
        """
        Compute and return my value
        """
        return self.getValue()


    @value.setter
    def value(self, value):
        """
        Set my value
        """
        return self.setValue(value)


    # interface
    def ref(self):
        """
        Build and return a reference to me
        """
        return self.reference(operands=[self])


# end of file 
