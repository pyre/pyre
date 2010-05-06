# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


import re
from .Polyadic import Polyadic


class Expression(Polyadic):
    """
    Evalutor that computes arbitrary python expression among nodes referenced by name
    """

    # interface
    def compute(self):
        """
        Evaluate my program
        """
        return eval(self._program, self._nodeTable)


    # exceptions
    from . import ExpressionError


    # meta methods
    def __init__(self, expression, model, **kwds):
        super().__init__(domain=self._compile(expression, model), **kwds)
        return


    # implementation details
    def _compile(self, formula, model):
        """
        Convert {expression} into a form that the python interpreter can evaluate by resolving
        references to other nodes against {model}
        """
        # install the symbol table
        self._symbolTable = {} # the map: {node name} -> {identifier}
        # convert node references to legal python identifiers
        expression = self._scanner.sub(self._identifierHandler, formula)
        # compile the resulting expression
        try:
            self._program = compile(expression, filename='expression', mode='eval')
        except SyntaxError as error:
            raise self.ExpressionError(self, error, formula) from error
        # build my evaluation context
        self._nodeTable = {
            self._symbolTable[name]: model.resolveNode(client=self, name=name)
            for name in self._symbolTable }
        # and compute and return my domain
        return set(self._nodeTable.values())


    def _identifierHandler(self, match):
        """
        Callback for re.sub that extracts node references, adds them to my symbol table and
        converts them into legal python identifiers
        """
        # extract the name from the match
        identifier = match.group('identifier')
        # if the identifier has been seen before
        try:
            # translate it and return it
            return self._symbolTable[identifier]
        except KeyError:
            # build a new name
            symbol = "_node_{0:04d}".format(len(self._symbolTable))
            # add it to the symbol table
            self._symbolTable[identifier] = symbol
            # and build and return the matching expression fragment
            return "(" + symbol + ".value)"


    def _replace(self, name, old, new):
        """
        Patch my domain by replacing {old} with {new}.

        This is used by the model during node resolution. Please don't use directly unless you
        have thought through the many and painful implications
        """
        # replace the node in the node table 
        # don't forget that the node name has been converted into a local sysmbol, so we need
        # an extra look up through the symbol table
        self._nodeTable[self._symbolTable[name]] = new
        # and let my ancestors take care of my domain
        return super()._replace(name, old, new)


    # private data
    _program = None # the compiled form of my expression
    _nodeTable = None # the map from node names to nodes
    _symbolTable = None # the map: {node name} -> {identifier}

    # regex choices
    _open = re.escape('{')
    _close = re.escape('}')
    _scanner = re.compile(r"{0}(?P<identifier>[^{1}]+){1}".format(_open, _close))
    

# end of file 
