# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2021 all rights reserved


# framework
import merlin


# a foundry that collects language specific information
class Language(merlin.foundry):
    """
    Decorate a language foundry
    """


    # my protocols
    language = merlin.protocols.language


    def __new__(cls, implements=language, **kwds):
        """
        Trap the invocation with meta-data and delay the decoration of the callable
        """
        # chain up with my new default protocol
        return super().__new__(cls, implements=implements, **kwds)


    def __init__(self, factory, language=None, **kwds):
        # chain up
        super().__init__(factory=factory, **kwds)

        # check that the language common name was supplied at the foundry call site
        assert language, "please specify the common name for the language"

        # register the foundry with the {language} protocol
        self.language.supported[language] = factory

        # all done
        return


# end of file
