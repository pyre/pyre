# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


# externals
import pyre


# helpers
# the language normalization table
languages = {
    "c++": "cxx",
    "fortran": "f77",
    "fortran77": "f77",
    }

# the language name converter
def convertLanguageName(language):
    """
    Map {language} into the set of known language identifiers
    """
    # first, convert to lower case
    language = language.lower()
    
    # attempt to
    try:
        # find the canonical name
        language = languages[language]
    # if it's not there
    except KeyError:
        # no problem
        pass
    # return the transformed symbol
    return language


# declaration
class Weaver(pyre.component, family="pyre.weaver"):
    """
    The base component for content generation
    """

    # types
    # protocols for my traits
    from .Language import Language


    # public state
    language = Language()
    language.doc = "the desired output language"
    language.converters = [ convertLanguageName ]


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


# end of file 
