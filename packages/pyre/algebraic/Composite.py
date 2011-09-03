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

    This class assumes that its instance provide {_operands}, a container of their dependencies
    on other nodes
    """


    # public data
    @property
    def variables(self):
        """
        Traverse my expression graph and return an iterable with all the variables I depend on
        """
        # traverse my operands
        for operand in self._operands:
            # and ask them for their dependencies
            for node in operand.variables:
                # return whatever it discovered
                yield node
        # and no more
        return


    # interface
    def substitute(self, replacements):
        """
        Look through the dictionary {replacements} for any of my operands and replace them with
        the indicated nodes.
        """
        operands = []
        # look through my operands
        for operand in self._operands:
            # does this one show up in the replacement map?
            if operand in replacements:
                # push its replacement to the new operand list
                operands.append(replacements[operand])
            # otherwise
            else:
                # push it
                operands.append(operand)
                # and hand it the replacement list
                operand.substitute(replacements)
        # install the new operands
        self._operands = tuple(operands)
        # and return
        return
                    

# end of file 
