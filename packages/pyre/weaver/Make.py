# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2023 all rights reserved
#


# access to the pyre package
import pyre
# my ancestor
from .LineMill import LineMill


# my declaration
class Make(LineMill):
    """
    Support for makefiles
    """


    # user configurable state
    languageMarker = pyre.properties.str(default='Makefile')
    languageMarker.doc = "the language marker"


    # interface
    def builtin(self, func, args=[]):
        """
        Evaluate a builtin function
        """
        # the arguments are a comma separated list
        rargs = ",".join(
           # of space separated words
           "".join(word for word in words)
           # made up from the arguments to the built in
           for words in args
        )

        # render
        yield f"${{{func} {rargs}}}"

        # and done
        return


    def call(self, func, args=[]):
        """
        Call a user defined function
        """
        # the arguments are a comma separated list
        rargs = ",".join(
           # of space separated words
           "".join(word for word in words)
           # made up from the arguments to the built in
           for words in args
        )

        # render
        yield f"${{call {func},{rargs}}}"
        # all done
        return


    def ifeq(self, op1, op2, onTrue, onFalse=None):
        """
        Build a conditional block
        """
        # render the operands
        rop1 = ''.join(op1)
        rop2 = ''.join(op2)

        # build the condition
        yield f"ifeq ({rop1},{rop2})"

        # render the true part
        yield from onTrue

        # if there is an else part
        if onFalse:
            # render
            yield "else"
            # render the false part
            yield from onFalse

        # close out
        yield "endif"

        # and done
        return


    def literal(self, value):
        """
        Render {value} as a literal
        """
        # just the value
        yield value
        # and done
        return


    def set(self, name, value="", multi=[]):
        """
        Set {name} to {value} immediately
        """
        # pick the operator and delegate
        return self._set(name=name, value=value, multi=multi, op=":=")


    def setq(self, name, value="", multi=[]):
        """
        Set {name} to {value}, delaying the evaluation of the wight hand side until used
        """
        # pick the operator and delegate
        return self._set(name=name, value=value, multi=multi, op="=")


    def setu(self, name, value="", multi=[]):
        """
        Set {name} to {value} iff {name} is uninitialized
        """
        # pick the operator and delegate
        return self._set(name=name, value=value, multi=multi, op="?=")


    def value(self, var):
        """
        Build an expression to evaluate {var}
        """
        # easy enough
        yield f"$({var})"
        # and done
        return


    # implementation details
    def _set(self, name, value, multi, op):
        """
        Support for variable assignments
        """
        # if it's a single line assignment
        if not multi:
            # assemble the value
            rvalue = "".join(value)
            # render
            yield f"{name} {op} {rvalue}"
            # and done
            return

        # pull the continuation mark
        mark = self.continuationMark
        # prime the multiline assignment
        yield f"{name} {op} {mark}"
        # append the multiline content
        for line in multi:
            # assemble the line
            rvalue = "".join(line)
            # and render it
            yield f"    {rvalue} {mark}"

        # all done
        return


    # private data
    comment = '#'
    continuationMark = '\\'


# end of file
