# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


# externals
import pyre


# declaration
class Language(pyre.protocol, family="pyre.weaver.languages"):
    """
    The protocol specification for output languages
    """


    # constants
    # the language normalization table
    languages = {
        "c++": "cxx",
        "fortran": "f77",
        "fortran77": "f77",
        }


    # framework hooks
    @classmethod
    def pyre_convert(cls, language):
        # first, convert to lower case
        language = language.lower()
        # now, translate
        return cls.languages.get(language, language)


    # interface
    @pyre.provides
    def render(self, document, stationery):
        """
        Layout the {document} using {stationery} for the header and footer
        """


# end of file 
