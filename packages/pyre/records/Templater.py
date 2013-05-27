# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# superclass
from ..patterns.AttributeClassifier import AttributeClassifier


class Templater(AttributeClassifier):
    """
    Metaclass that inspects record declarations and endows their instances with the necessary
    infrastructure to support

    * named access of the entries in a record
    * composition via inheritance
    * derivations, i.e. fields whose values depend on the values of other fields
    """


    # types: the descriptor categories
    from . import entry as pyre_entry
    from . import measure as pyre_measure
    from . import derivation as pyre_derivation
    # my value accessor
    from .Accessor import Accessor as pyre_accessor
    # the value extractors
    from .Extractor import Extractor as pyre_extractor # simple immutable tuples
    from .Evaluator import Evaluator as pyre_evaluator # complex immutable tuples
    from .Calculator import Calculator as pyre_calculator # simple mutable tuples
    from .Compiler import Compiler as pyre_compiler # complex mutable tuples


    # meta-methods
    def __new__(cls, name, bases, attributes, *, slots=(), **kwds):
        """
        The builder of a new record class.

        Scans through the attributes of the class record being built and harvests the meta-data
        descriptors. These descriptors are removed for the attribute dictionary and replaced
        later with accessors appropriate for each type of record.
        """
        # make a pile foe the meta-data descriptors
        localEntries = []
        # harvest them
        for entryName, entry in cls.pyre_harvest(attributes, cls.pyre_entry):
            # initialize them
            entry.attach(name=entryName)
            # and add them to the pile
            localEntries.append(entry)

        # build an attribute to hold the locally declared entries
        attributes["pyre_localEntries"] = tuple(localEntries)
        # disable the wasteful {__dict__}
        if slots is not None: attributes['__slots__'] = slots

        # build the class record
        record = super().__new__(cls, name, bases, attributes, **kwds)

        # now that the class record is built, we can look for inherited entries as well; we
        # traverse the {__mro__} in reverse order and place inherited entries ahead of local
        # ones; this corresponds to the intuitive layout that users expect. further,
        # derivations are expressions involving any of the entries accessible at the point of
        # their declaration, so all of them must have been populated already

        # initialize the three piles
        entries = []
        measures = []
        derivations = []
        # for each base class
        for base in reversed(record.__mro__):
            # skip the ones that are not records themselves
            if not isinstance(base, cls): continue
            # get all of the locally declared record entries
            for entry in base.pyre_localEntries:
                # add this to the pile
                entries.append(entry)
                # if it is a measure
                if cls.pyre_isMeasure(entry):
                    # add it to the measure pile
                    measures.append(entry)
                # if it is a derivation
                elif cls.pyre_isDerivation(entry):
                    # add it to the pile of derivations
                    derivations.append(entry)
                # otherwise
                else:
                    # we have a problem; get the journal
                    import journal
                    # and complain
                    raise journal.firewall('pyre.records').log(
                        'unknown entry type: {}'.format(entry))

        # attach them to the class record
        record.pyre_entries = tuple(entries)
        # filter the measures
        record.pyre_measures = tuple(measures)
        # and the derivations
        record.pyre_derivations = tuple(derivations)
        
        # finally, some clients need a map from entries to their index in our underlying tuple
        record.pyre_index = dict((entry, index) for index, entry in enumerate(entries))

        # show me
        # print("{}:".format(name))
        # print("  entries: {}".format(tuple(entry.name for entry in record.pyre_entries)))
        # print("  measures: {}".format(tuple(entry.name for entry in record.pyre_measures)))
        # print("  derivations: {}".format(tuple(entry.name for entry in record.pyre_derivations)))
        # print("  index:")
        # for entry, index in record.pyre_index.items():
            # print("    {.name} -> {}".format(entry, index))

        # all done
        return record


    def __init__(self, names, bases, attributes, **kwds):
        """
        Decorate a newly minted record

        Now that the class record is built and all the meta-data have been harvested, we can
        build the generators of my instances. The are two of them: one for immutable instances,
        built using a named tuple whose entries are the actual values of the various entries;
        and one for mutable instances, built from a named tuple whose entries are {pyre.calc}
        nodes.
        """
        # chain up
        super().__init__(names, bases, attributes, **kwds)

        # build the tuple attributes: start with the value accessors
        attributes = dict(
            # map the name of the entry to an accessor
            (entry.name, self.pyre_accessor(entry=entry, index=index))
            # for each of my entries
            for index, entry in enumerate(self.pyre_entries))

        # build the helper classes that generate my instances
        mutable = type('mutable', (self.pyre_mutableTuple,), attributes)
        immutable = type('immutable', (self.pyre_immutableTuple,), attributes)

        # if i have derivations
        if self.pyre_derivations:
            # attach the value extraction strategies that are aware of derivations
            mutable.pyre_extract = self.pyre_compiler()
            immutable.pyre_extract = self.pyre_evaluator()
        # otherwise
        else:
            # attach the fast value extraction strategies
            mutable.pyre_extract = self.pyre_calculator()
            immutable.pyre_extract = self.pyre_extractor()

        # and attach them
        self.pyre_mutable = mutable
        self.pyre_immutable = immutable

        # all done
        return


    # predicates
    @classmethod
    def pyre_isMeasure(cls, entry):
        """
        Predicate that tests whether {entry} is a measure
        """
        # easy...
        return entry.category == 'variable'


    @classmethod
    def pyre_isDerivation(cls, entry):
        """
        Predicate that tests whether {entry} is a derivation
        """
        # easy...
        return entry.category == 'operator'
        

# end of file
