# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
import collections.abc

# support
from .. import tracking


# declaration
class Map(collections.abc.MutableMapping):
    """
    The base class of the maps that hold the values of {Dict} traits; they behave like
    dictionaries, and turn into one when copied or pickled
    """

    # meta-methods
    def __init__(self, trait, factory, **kwds):
        # chain up
        super().__init__(**kwds)
        # the trait whose values i hold
        self.trait = trait
        # the factory of the slots of my entries
        self.factory = factory
        # my storage
        self.map = {}
        # the instance that owns me, once it reads me
        self.client = None
        # all done
        return

    def __delitem__(self, name):
        """
        Remove {name} from my map
        """
        # easy enough
        del self.map[name]
        # tell my owner
        self.notify()
        # all done
        return

    def __iter__(self):
        """
        Create an iterator over my map
        """
        # easy enough
        return iter(self.map)

    def __len__(self):
        """
        Compute my size
        """
        # easy enough
        return len(self.map)

    def __contains__(self, name):
        """
        Check whether {name} is in my map
        """
        # easy enough
        return name in self.map

    def __setitem__(self, name, value):
        """
        Store {value} in the map under {name}
        """
        # an assignment in the code
        priority = self.trait.pyre_nameserver.priority.explicit()
        # says where it is made in plain words
        locator = tracking.simple(f"while setting '{name}' in '{self.trait.name}'")
        # store it
        self.insert(name=name, value=value, priority=priority, locator=locator)
        # tell my owner
        self.notify()
        # all done
        return

    def __or__(self, other):
        """
        Merge {other} into a copy of me
        """
        # into a dictionary, the way dictionaries merge
        return {**self, **other}

    def __ror__(self, other):
        """
        Merge a copy of me into {other}
        """
        # into a dictionary, the way dictionaries merge
        return {**other, **self}

    def __repr__(self):
        """
        Render my contents the way a dictionary would
        """
        # by becoming one
        return repr(dict(self))

    def __reduce__(self):
        """
        Pickle my contents as a dictionary, since the slots of my entries stay behind
        """
        # by becoming one
        return (dict, (dict(self),))

    # interface
    def copy(self):
        """
        Make a dictionary with my contents
        """
        # easy enough
        return dict(self)

    def notify(self):
        """
        Tell the instance that owns me that its map has changed
        """
        # get my owner
        client = self.client
        # if i don't have one, or it is still being built
        if client is None or not client.pyre_cooked:
            # there is no one to tell
            return
        # get my slot
        slot = client.pyre_inventory[self.trait]
        # and tell my owner; the map is the same slot before and after the change
        client.pyre_traitModified(trait=self.trait, new=slot, old=slot)
        # all done
        return


# end of file
