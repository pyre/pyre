# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2013 all rights reserved
#


# externals
import pyre


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


    # public interface
    @pyre.export
    def weave(self, document=None):
        """
        Assemble and print the {document} into the given {stream}
        """
        # create an empty {document} if none was given
        document = () if document is None else document
        # render it
        yield from self.language.render(document=document)
        # and return
        return


# end of file 
