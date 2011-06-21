# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


class LineComments:
    """
    The line based commenting strategy
    """


    # implemented interface
    def commentBlock(self, lines):
        """
        Create a comment block out of the given {lines}
        """
        # iterate over the {lines}
        for line in lines:
            # if the line is not empty
            if line:
                # render it
                yield self.comment + ' ' + line
            # otherwise
            else:
                # render just the comment marker
                yield self.comment

        # all done
        return


    def commentLine(self, line):
        """
        Mark {line} as a comment
        """
        # if the line is non-empty
        if line:
            # mark it
            return self.comment + ' ' + line
        # otherwise, just return the comment characters
        return self.comment


    # meta methods
    def __init__(self, comment, **kwds):
        super().__init__(**kwds)
        self.comment = comment
        return


# end of file 
