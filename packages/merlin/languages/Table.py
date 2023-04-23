# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# support
import merlin


# a table with language specific configurations
class Table(
    merlin.component,
    family="merlin.languages.table",
    implements=merlin.protocols.languages.table,
):
    """
    A table of language specific configurations
    """

    # configurable state
    autogen = merlin.protocols.languages.autogen()
    autogen.doc = "Template expander configuration"

    c = merlin.protocols.languages.c()
    c.doc = "C configuration"

    cxx = merlin.protocols.languages.cxx()
    cxx.doc = "C++ configuration"

    cuda = merlin.protocols.languages.cuda()
    cuda.doc = "CUDA configuration"

    cython = merlin.protocols.languages.cython()
    cython.doc = "cython configuration"

    fortran = merlin.protocols.languages.fortran()
    fortran.doc = "FORTRAN configuration"

    python = merlin.protocols.languages.python()
    python.doc = "python configuration"

    # metamethods
    def __init__(self, **kwds):
        # chain up
        super().__init__(**kwds)
        # make a classifier
        self.classifier = self.assetClassifier()
        # all done
        return

    def __iter__(self):
        """
        Generate a sequence of the supported languages
        """
        # yield each one
        yield self.autogen
        yield self.c
        yield self.cxx
        yield self.cuda
        yield self.cython
        yield self.fortran
        yield self.python
        # all done
        return

    # suffix -> (assetCategory, language)
    def assetClassifier(self) -> dict:
        """
        Build a map of file suffixes to asset category and language
        """
        # make a table of suffixes to category and language
        table = merlin.patterns.vivify(levels=2, atom=set)
        # go through the relevant languages
        for language in self:
            # go through its suffix categories
            for suffix, category in language.assetClassifier.items():
                # add this to the table
                table[suffix][category].add(language)

        # the cleaned up version of {table} becomes my {assetClassifier}
        assetClassifier = {}
        # go through the table and for each suffix
        for suffix in table:
            # grab the table of candidate categories
            categories = table[suffix]
            # unpack
            category, *conflicts = categories.keys()
            # if there is a conflict
            if conflicts:
                # there is something wrong with the configuration of the supported languages
                channel = journal.firewall("merlin.assets.library")
                # so complain
                channel.line(f"found multiple asset categories for suffix '{suffix}'")
                channel.line(f"candidates:")
                # go through the candidates
                for cat, langs in categories.items():
                    # and show me which languages claim which category
                    channel.line(
                        f"  {cat.category}: from  {', '.join(l.name for l in langs)}"
                    )
                # and flush
                channel.log()
                # just in case this firewall is not fatal,
                # set up this suffix as unrecognizable category with no associated language
                assetClassifier[suffix] = "unrecognized", None
                # and move on
                continue
            # now, get the associated languages
            language, *conflicts = categories[category]
            # again, if more than one language competes for this suffix
            if conflicts:
                # the suffix is of unknown language
                language = None
            # mark it
            assetClassifier[suffix] = category, language

        # all done
        return assetClassifier


# end of file
