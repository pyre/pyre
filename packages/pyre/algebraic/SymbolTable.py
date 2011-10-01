# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


# regular expressions
import re
# access to the base class
from ..patterns.Named import Named


# declaration
class SymbolTable(Named):
    """
    The base class for node evaluation contexts

    {SymbolTable} provides the interface for managing nodes. The storage mechanism is delegated
    to subclasses.
    """


    # types
    # exceptions
    from .exceptions import (
        CircularReferenceError,
        EmptyExpressionError, ExpressionSyntaxError, EvaluationError,
        UnresolvedNodeError
        )


    # public data
    @property
    def nodes(self):
        """
        Create an iterable over the nodes in my graph.
        """
        return self._nodes.values()


    # interface
    def parse(self, expression):
        """
        Examine the input string {expression} and attempt to convert it into an {Expression}
        node. Resolve all named references to other nodes against my symbol table.
        """
        # initialize the symbol table
        operands = []
        # define the re.sub callback as a local function so it has access to the symbol table
        def handler(match):
            """
            Callback for {re.sub} that extracts node references, adds them to my local symbol
            table and converts them into legal python identifiers
            """
            # if the pattern matched an escaped opening brace, return it as a literal
            if match.group("esc_open"): return "{"
            # if the pattern matched an escaped closing brace, return it as a literal
            if match.group("esc_close"): return "}"
            # unmatched braces
            if match.group("lone_open") or match.group("lone_closed"):
                raise self.ExpressionSyntaxError(formula=expression, error="unmatched brace")
            # only one case left: a valid node reference
            # extract the name from the match
            identifier = match.group('identifier')
            # resolve it
            node, _ = self._resolve(name=identifier)
            # add the node to the operands
            operands.append(node)
            # build and return the matching expression fragment
            return "(model[{!r}])".format(identifier)

        # convert node references to legal python identifiers
        # print("Expression.parse: expression={!r}".format(expression))
        normalized = self._scanner.sub(handler, expression)
        # print("  normalized: {!r}".format(normalized))
        # print("  symbols:", symbols)
        # raise an exception if there were no symbols
        if not operands:
            raise self.EmptyExpressionError(formula=expression)
        # now, attempt to compile the expression
        try:
            program = compile(normalized, filename='expression', mode='eval')
        except SyntaxError as error:
            raise self.ExpressionSyntaxError(formula=expression, error=error) from error

        # all is well if we get this far
        return self.node.expression(
            model=self, expression=expression, program=program, operands=operands)


    # meta methods
    def __init__(self, node=None, **kwds):
        super().__init__(**kwds)

        # if i didn't get a node factory
        if node is None:
            # use the one from this package
            from .Node import Node as node
        # record the node factory
        self.node = node
        # initialize the node storage
        self._nodes = {}
        # all done
        return


    # subscripted access to the model
    def __getitem__(self, name):
        """
        Resolve {name} into a node and return its value
        """
        # delegate
        node,_ = self._resolve(name=name)
        # compute the value and return it
        return node.value


    def __setitem__(self, name, value):
        """
        Add/update the named node with the given {value}
        """
        # build a node from {value}
        replacement = self._recognize(value)
        # fetch the node already registered under {name}
        existing, identifier = self._resolve(name)
        # update the model
        self._update(identifier=identifier, existing=existing, replacement=replacement)
        # and return
        return


    # implementation details
    def _recognize(self, value):
        """
        Attempt to convert {value} into a {pyre.calc} node
        """
        # N.B.: the logic here is tricky; modify carefully
        # is value already a node?
        if isinstance(value, self.node):
            # return it
            return value
        # is it a string?
        if isinstance(value, str):
            # attempt to convert it to an expression
            try:
                return self.parse(expression=value)
            # empty expressions are raw data; other errors propagate through
            except self.EmptyExpressionError:
                # build a node with the string as value
                return self.node.variable(value=value)
        # in all other cases, make a node whose value is the raw data
        return self.node.variable(value=value)


    def _resolve(self, name):
        """
        Find the named node
        """
        # attempt
        try:
            # to look it up and return it
            return self._nodes[name], name
        # if that fails
        except KeyError:
            # no worries
            pass
        # make an unresolved node
        unresolved = self.node.unresolved(name=name)
        # add it to the pile
        self._nodes[name] = unresolved
        # and return it
        return unresolved, name

 
    def _update(self, identifier, existing, replacement):
        """
        Update the model by resolving the name conflict among the two nodes, {existing} and
        {replacement}
        """
        # my variable type
        variable = self.node.variable
        # if both nodes are variables
        if isinstance(existing, variable) and isinstance(replacement, variable):
            # just transfer the value
            existing.value = replacement.value
            # and return
            return self
        # otherwise, verify that the old node is not in the span of the new node
        # by iterating over all nodes
        for node in replacement.span:
            # if {existing} is a member
            if node is existing:
                # report the error
                raise self.CircularReferenceError(node=existing)

        # if we get this far, just replace the old node
        self._nodes[identifier] = replacement
        # and return
        return
        

    # private data
    _nodes = None # node storage
    _scanner = re.compile( # the expression tokenizer
        r"(?P<esc_open>{{)"
        r"|"
        r"(?P<esc_close>}})"
        r"|"
        r"{(?P<identifier>[^}{]+)}"
        r"|"
        r"(?P<lone_open>{)"
        r"|"
        r"(?P<lone_closed>})"
        )
    

# end of file 
