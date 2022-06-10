#-*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2022 all rights reserved


# superclass
from .Object import Object


# a dataset container
class Group(Object):
    """
    A container of datasets
    """

    # public data
    @property
    def pyre_marker(self):
        """
        Generate an identifying mark
        """
        # use my type name
        return "g"


    # interface
    def pyre_datasets(self):
        """
        Generate a sequence of my datasets
        """
        # get the {dataset} base class
        from .Dataset import Dataset
        # filter and return
        return filter(lambda loc: issubclass(loc, Dataset), self.pyre_locations())


    def pyre_groups(self):
        """
        Generate a sequence of my subgroups
        """
        # filter and return
        return filter(lambda loc: issubclass(loc, Group), self.pyre_locations())


    def pyre_locations(self):
        """
        Generate a sequence of contents
        """
        # N.B.:
        # currently, there are two possible sources of identifiers in my contents
        # - the static layout of my {mro}, with each superclass contributing the identifiers it
        #    declares
        # - the pile of identifiers added programmatically
        #
        # collating identifiers from these sources requires taking shadowing into account
        # shadowing is determined by the {pyre_location} of an identifier, not its {pyre_name}
        # inconsistencies caused by decorrelations between names and locations are considered bugs

        # make a pile of identifier names that have been encountered
        known = set()

        # go through my pedigree
        for base in type(self).mro():
            # attempt to
            try:
                # look up the static identifiers i inherit from this ancestor
                identifiers = base.pyre_identifiers.values()
            # if it doesn't have any
            except AttributeError:
                # no problem; move on
                continue
            # go through them
            for identifier in identifiers:
                # get their location
                location = identifier.pyre_location
                # if this location is being shadowed
                if location in known:
                    # move on
                    continue
                # otherwise, add it to the pile of {known} locations
                known.add(location)
                # and send off the {identifier}
                yield identifier
        # all done
        return


    # metamethods
    def __str__(self):
        """
        Human readable description
        """
        return "a group"


    # framework hooks
    def pyre_sync(self, instance, **kwds):
        """
        Hook invoked when the {inventory} lookup fails and a value must be generated
        """
        # build a clone of mine to hold my client's values for my structure
        group = type(self)(name=self.pyre_name, at=self.pyre_location)
        # attach it
        self.pyre_set(instance=instance, value=group)
        # and return it
        return group


# end of file
