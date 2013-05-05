# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# externals
import itertools # for count
import functools # for total_ordering
import collections # for defaultdict


# auto-implement the ordering methods
@functools.total_ordering
# declaration
class Priority:


    # the priority category types; patched later in this file
    uninitialized = None
    defaults = None
    boot = None
    package = None
    user = None
    command = None
    explicit = None
    framework = None


    # meta-methods
    def __init__(self):
        self.rank = next(self.collator[self.category])
        return


    # ordering
    def __eq__(self, other):
        return (self.category, self.rank) == (other.category, other.rank)
        
    def __lt__(self, other):
        return (self.category, self.rank) < (other.category, other.rank)


    # debug support
    def __str__(self):
        return "({0.category},{0.rank})".format(self)


    # private data
    collator = collections.defaultdict(itertools.count)
    # narrow the footprint 
    __slots__ = ("category", "rank")


# build a counter
categories = itertools.count(start=-1)

# specific priority categories
class Uninitialized(Priority):
    """
    Category for unspecified priorities; meant to be used as default values for arguments to
    functions
    """
    # public data
    category = next(categories)

class Defaults(Priority):
    """
    Category for the priorities of the default values of traits, i.e. the values in the class
    declarations
    """
    # public data
    category = next(categories)

class Boot(Priority):
    """
    Category for the priorities of values assigned while the framework is booting
    """
    # public data
    category = next(categories)

class Package(Priority):
    """
    Category for the priorities of values assigned while package configurations are being
    retrieved
    """
    # public data
    category = next(categories)

class User(Priority):
    """
    Category for the priorities of values assigned during the processing of user configuration
    events
    """
    # public data
    category = next(categories)

class Command(Priority):
    """
    Category for the priorities of values assigned during the processing of the command line
    """
    # public data
    category = next(categories)

class Explicit(Priority):
    """
    Category for the priorities of values assigned explicitly by the user program
    """
    # public data
    category = next(categories)

class Framework(Priority):
    """
    Category for the priorities of read-only values assigned by the framework
    """
    # public data
    category = next(categories)


# patch Priority
Priority.uninitialized = Uninitialized
Priority.defaults = Defaults
Priority.boot = Boot
Priority.package = Package
Priority.command = Command
Priority.user = User
Priority.explicit = Explicit
Priority.framework = Framework


# end of file 
