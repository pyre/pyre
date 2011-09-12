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
    # nodes
    from .Node import Node as node
    from .Variable import Variable as var
    from .Expression import Expression as expression
    from .UnresolvedNode import UnresolvedNode as unresolved
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

        This is expected to return the complete sequence of nodes, regardless of the storage
        details implemented by AbstractModel descendants
        """
        raise NotImplementedError(
            "class {0.__class__.__name__!r} must implement 'nodes'".format(self))


    # interface
    def eval(self, program):
        """
        Evaluate the compiled object {program} in the context of my registered nodes
        """
        raise NotImplementedError(
            "class {0.__class__.__name__!r} must implement 'eval'".format(self))


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
            Callback for re.sub that extracts node references, adds them to my local symbol
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
            node, identifier = self._resolve(name=identifier)
            # add the node to the operands
            operands.append(node)
            # build and return the matching expression fragment
            return "(" + identifier + ".value)"

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
        return self.expression(
            model=self, expression=expression, program=program, operands=operands)


    # meta methods
    def __init__(self, **kwds):
        super().__init__(**kwds)
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
        # N.B.: the logic here is tricky; modify carefully
        # initialize
        node = None
        # is value already a node?
        if isinstance(value, self.node):
            # save it
            node = value
        # is it a string?
        elif isinstance(value, str):
            # attempt to convert it to an expression
            try:
                node = self.parse(expression=value)
            # empty expressions are raw data; other errors propagate through
            except self.EmptyExpressionError:
                pass
        # at this point, either {node} is not {None} and {value} has been converted, or {node}
        # is {None} and the value is raw data
        # resolve the name 
        existing, identifier = self._resolve(name=name)
        # if the existing node is a regular variable and we have a value for it
        if node is None and isinstance(existing, self.var):
            # update it
            existing.value = value
            # and return 
            return
        # otherwise, convert raw data into a new node
        if node is None: node = self.var(value=value)
        # patch the model
        self._patch(discard=existing, replacement=node)
        # and register the new node
        return self._register(identifier=identifier, node=node)


    # implementation details
    def _patch(self, discard, replacement):
        """
        Replace {discard} with {replacement}

        N.B.: subclasses must implement this carefully as there are many model invariants that
        must be maintained...
        """
        # iterate over the observers of the discarded node
        for observer in tuple(discard.observers):
            # substitute the discarded node with its replacement
            observer.substitute(current=discard, replacement=replacement)
        # and return
        return


    def _register(self, *, name, identifier, node):
        """
        Add {node} into the model and make it accessible through {name}
        """
        raise NotImplementedError(
            "class {0.__class__.__name__!r} must implement '_register'".format(self))


    def _resolve(self, *, name):
        """
        Find the named node
        """
        raise NotImplementedError(
            "class {0.__class__.__name__!r} must implement '_resolve'".format(self))


    # private data
    # the expression tokenizer
    _scanner = re.compile(
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
