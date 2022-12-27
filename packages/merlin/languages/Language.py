# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# support
import journal
# framework
import merlin


# base class for all supported languages
class Language(merlin.component, implements=merlin.protocols.language, internal=True):
    """
    A category of source artifacts, usually associated with a family of processing workflows
    """


    # constants
    # the language tag
    name = None
    # properties of the canonical toolchains associated with this language
    linkable = False        # whether the products are recognized by the system linker
    assetClassifier = None  # a {suffix} -> {assetCategory} map
    # default asset category factories
    source = merlin.assets.source
    header = merlin.assets.header

    # required state
    categories = merlin.properties.catalog()
    categories.doc = "a map from file categories to a list of suffixes"


    # interface
    @classmethod
    def recognize(cls, name):
        """
        Attempt to determine the asset category based on the {name} of an asset
        """
        # extract the suffix of the filename
        suffix = merlin.primitives.path(name).suffix
        # and ask my {assetClassifier}
        return cls.assetClassifier.get(suffix)


    # merlin hooks
    def identify(self, visitor, **kwds):
        """
        Ask {visitor} to process an unknown language type
        """
        # attempt to
        try:
            # ask the {visitor} for a handler for a source file of any language
            handler = visitor.language
        # if it doesn't exist
        except AttributeError:
            # this is almost certainly a bug; make a channel
            channel = journal.firewall("merlin.languages.identify")
            # complain
            channel.line(f"unable to find a handler for {self.name} sources")
            channel.line(f"while looking through the interface of '{visitor.pyre_name}'")
            # flush
            channel.log()
            # and fail, just in case firewalls aren't fatal
            return None
        # if it does, invoke it
        return handler(language=self, **kwds)


    # framework hooks
    @classmethod
    def pyre_classRegistered(cls):
        """
        Hook that gets invoked by the framework after the class record has been registered but
        before any configuration events
        """
        # if this is not a publicly visible class
        if cls.pyre_internal:
            # leave it alone and chain up
            return super().pyre_classRegistered()

        # otherwise, there is some extra set up to do
        # initialize the map from suffix to asset category
        table = {}
        # go through the asset category catalog
        for category, suffixes in cls.categories.items():
            # and through each suffix
            for suffix in suffixes:
                # look it up in the table
                conflict = table.get(suffix)
                # if it's there
                if conflict:
                    # we have a bug
                    channel = journal.firewall(f"merlin.languages.{cls.name}")
                    # complain
                    channel.line(f"conflicting asset categories for suffix '{suffix}'")
                    channel.line(f"found '{conflict}' while processing '{category}'")
                    channel.line(f"while initializing '{cls.name}'")
                    # flush
                    channel.log()
                    # and move on, in case this firewall isn't fatal
                    continue
                # if not already in the table, add it
                table[suffix] = getattr(merlin.assets, category)

        # attach the table
        cls.assetClassifier = table
        # and chain up
        return super().pyre_classRegistered()


# end of file
