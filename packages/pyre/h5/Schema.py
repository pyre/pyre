#-*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2022 all rights reserved


# superclass
from pyre.patterns.AttributeClassifier import AttributeClassifier
# the base class for my descriptors
from .Identifier import Identifier


# dataset harvester
class Schema(AttributeClassifier):
    """
    Harvest dataset descriptors from h5 groups
    """


    # metamethods
    def __new__(cls, name, bases, attributes, **kwds):
        """
        Build the class record of a new h5 group
        """
        # N.B.:
        #  if there are any additional class variables to be attached to the class record
        #  they must be added carefully to make sure {__setattr__} doesn't trigger
        #  here, for example, we modify {attributes} before chaining up in order to build and
        #  attach the {pyre_identifiers}

        # make a table with the known identifiers and add it to the pile of attributes
        attributes["pyre_identifiers"] = {
            name: identifier
            for name, identifier in cls.pyre_harvestIdentifiers(attributes=attributes)
        }

        # build the record and return it
        return super().__new__(cls, name, bases, attributes, **kwds)


    def __call__(self, **kwds):
        """
        Build an instance of one of my classes
        """
        # build the instance
        location = super().__call__(**kwds)
        # and return the new instance
        return location


    def __getattr__(self, name):
        """
        Look up the value of {name} in one of my instances
        """
        # we are here only when normal attribute look up fails in one of my instances
        # currently, there is nothing useful for me to do here, so complain
        raise AttributeError # as of 3.10: AttributeError(name=name, obj=self)


    def __setattr__(self, name, value):
        """
        Assign {name} to {value} in one of my instances
        """
        # check whether
        try:
            # {name} is one the identifiers in my {pyre_identifiers}
            identifier = self.pyre_identifiers[name]
        # if not
        except KeyError:
            # move on
            pass
        # if it is
        else:
            # interpret this assignment as an attempt to set a new default value for it
            identifier.default = value
            # and done
            return

        # if {value} is an {Identifier} instance
        if isinstance(value, Identifier):
            # add it to {pyre_identifiers}
            self.pyre_identifiers[name] = value

        # chain up to handle normal assignment
        return super().__setattr__(name, value)


    # implementation details
    @classmethod
    def pyre_harvestIdentifiers(cls, attributes):
        """
        Scan {attributes} for identifiers
        """
        # examine the attributes and select the identifiers
        yield from cls.pyre_harvest(attributes=attributes, descriptor=Identifier)
        # all done
        return


# end of file
