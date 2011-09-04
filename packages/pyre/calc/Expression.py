# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


import re
from .Node import Node


class Expression(Node):
    """
    Support for building evaluation graphs involving nodes that have names registered with an
    {AbstractModel} instance
    """


    # types
    # exceptions
    from .exceptions import EmptyExpressionError, ExpressionError


    # factory
    @classmethod
    def parse(cls, expression, model):
        """
        Examine the input string {expression} and attempt to convert it into an
        Expression. Named references to other nodes are resolved against the symbol table
        {model}, which is expected to be an {AbstractModel} instance
        """
        # initialize the symbol table
        symbols = {}
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
                raise cls.ExpressionError(formula=expression, error="unmatched brace")
            # only one case left: a valid node reference
            # extract the name from the match
            identifier = match.group('identifier')
            # if the identifier has been seen before
            try:
                # translate it and return it
                return symbols[identifier]
            except KeyError:
                # build a new name
                symbol = "_{}".format(len(symbols))
                # add it to the symbol table
                symbols[identifier] = symbol
                # build and return the matching expression fragment
                return "(" + symbol + ".value)"
        # convert node references to legal python identifiers
        # print("Expression.parse: expression={!r}".format(expression))
        normalized = cls.scanner.sub(handler, expression)
        # print("  normalized: {!r}".format(normalized))
        # print("  symbols:", symbols)
        # raise an exception if there were no symbols
        if not symbols:
            raise cls.EmptyExpressionError(formula=expression)
        # now, attempt to compile the expression
        try:
            program = compile(normalized, filename='expression', mode='eval')
        except SyntaxError as error:
            raise cls.ExpressionError(formula=expression, error=error) from error
        # all is well if we get this far
        # build the domain as a map of nodes to their normalized names
        domain = { model.resolve(name=used): norm for used, norm in symbols.items() }
        # print("  domain:", domain)
        # build the node table as a map of normalized names to nodes
        nodes = { norm: node for node, norm in domain.items() }
        # print("  nodes:", nodes)
        # we have all the parts; make the evaluator
        return Expression(expression=expression, program=program, domain=domain, nodes=nodes)


    # public data
    formula = None # the expression supplied by the client


    @property
    def value(self):
        """
        Compute and return my value
        """
        # if my cached value is invalid
        if self._value is None:
            # evaluate my program
            self._value = eval(self._program, self._nodes)
        # and return it
        return self._value


    # interface
    def flush(self):
        """
        Invalidate my cache and notify my observers
        """
        # N.B.: there is another copy of this method in {Dependent}
        # bail out if I am already marked as invalid
        if self._value is None: return
        # otherwise, invalidate my cache
        self._value = None
        # notify my observers
        self.notifyObservers()
        # and return
        return self


    # meta methods
    def __init__(self, expression, program, domain, nodes, **kwds):
        super().__init__(**kwds)
        self.formula = expression
        self._program = program
        self._nodes = nodes
        self._domain = domain
        return


    # private data
    _value = None # my value cache
    _program = None # the compiled form of my expression
    _domain = None # the set on nodes i depend on
    _nodes = None # the map from node names to nodes

    # the expression tokenizer
    scanner = re.compile(
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
