# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


import pyre


class Weaver(pyre.component, family="pyre.weaver", resolver=True):
    """
    The base component for content generation
    """

    # types
    from .Language import Language

    # traits
    language = pyre.facility(interface=Language, default=None)
    language.doc = "the desired output language"


    # public interface
    @pyre.export
    def weave(self, document=None):
        """
        Assemble and print the {document} into the given {stream}
        """
        # create an empty {document} if none was give
        document = () if document is None else document
        # render the document
        for line in self.language.render(document=document):
            yield line
        # and return
        return


    # resolver protocol obligations
    @classmethod
    def pyre_translateSymbol(cls, context, symbol):
        """
        Convert {symbol} into its canonical form
        """
        # the first two parts of {context} must be my family name
        assert(context[:2]) == cls.pyre_family
        # if that's all there is
        if len(context) == 2:
            # what do I know?
            return symbol

        # now, if the remainder is "languages"
        if context[2] == "languages":
            # convert it to lowercase
            symbol = symbol.lower()
            # try to look it up in the language alias table
            try:
                return cls.languages[symbol]
            # if not there
            except KeyError:
                # convert it to lower case and pass it on
                return symbol
            
        # no special processing necessary
        return symbol


    @classmethod
    def pyre_componentSearchPath(cls, context):
        """
        Build a sequence of locations where component descriptors from {context} may be found
        """
        # nothing to say at this point
        return []


    # the language aliases table
    languages = {
        "c++": "cxx",
        "fortran": "f77",
        "fortran77": "f77",
        }


# end of file 
