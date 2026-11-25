# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# superclass
from ..patterns.AttributeClassifier import AttributeClassifier


class Templater(AttributeClassifier):
    """
    Metaclass that inspects record declarations and endows their instances with the necessary
    infrastructure to support

    * named access of the fields in a record
    * composition via inheritance
    * derivations, i.e. fields whose values depend on the values of other fields
    """

    # types: the descriptor categories
    from . import field as pyre_field
    from . import measure as pyre_measure
    from . import derivation as pyre_derivation
    from . import literal as pyre_literal

    # the tuples
    from .Mutable import Mutable as pyre_mutableTupleType
    from .Immutable import Immutable as pyre_immutableTupleType

    # my field selector
    from .Selector import Selector as pyre_selector

    # my field value accessor
    from .Accessor import Accessor as pyre_accessor

    # the value extractors
    from .Extractor import Extractor as pyre_extractor  # simple immutable tuples
    from .Evaluator import Evaluator as pyre_evaluator  # complex immutable tuples
    from .Calculator import Calculator as pyre_calculator  # simple mutable tuples
    from .Compiler import Compiler as pyre_compiler  # complex mutable tuples

    # meta-methods
    def __new__(cls, name, bases, attributes, id=None, **kwds):
        """
        The builder of a new record class.

        Scans through the attributes of the class record being built and harvests the meta-data
        descriptors. These descriptors are removed from the attribute dictionary and replaced
        later with accessors appropriate for each type of record.
        """
        # make a pile for the field descriptors
        localFields = []
        # harvest them
        for fieldName, field in cls.pyre_harvest(attributes, cls.pyre_field):
            # bind them
            field.bind(name=fieldName)
            # and add them to the pile
            localFields.append(field)

        # record my name, which {id} replaces when it is given
        attributes["pyre_name"] = name if id is None else id
        # and the fields declared locally
        attributes["pyre_localFields"] = tuple(localFields)

        # remove the field descriptors; we replace them in {__init__} with selectors
        for field in localFields:
            # one at a time
            del attributes[field.name]

        # build the class record
        record = super().__new__(cls, name, bases, attributes, **kwds)

        # now that the class record is built, gather the fields of its ancestors along with its
        # own; the classes are visited in reverse {__mro__}, which is the order in which they
        # shadow one another, so each comes after every class it can shadow and the layout of a
        # record starts with that of its first base; a field whose name is in the layout already
        # shadows the field there, and takes its slot

        # the fields, in order
        fields = []
        # the slot of each name
        slots = {}
        # and the field that replaces each shadowed one
        shadows = {}
        # for each base class
        for base in reversed(record.__mro__):
            # skip the ones that are not records themselves
            if not isinstance(base, cls):
                # by moving on
                continue
            # go through the fields it declares
            for field in base.pyre_localFields:
                # find the slot of its name
                slot = slots.get(field.name)
                # a new name
                if slot is None:
                    # gets the next slot
                    slots[field.name] = len(fields)
                    # and the field goes there
                    fields.append(field)
                    # moving on
                    continue
                # otherwise, the field shadows the one in the slot
                shadowed = fields[slot]
                # so the fields that one replaced earlier now stand for this one
                for old, new in shadows.items():
                    # by finding them
                    if new is shadowed:
                        # and pointing them here
                        shadows[old] = field
                # as does the shadowed field itself
                shadows[shadowed] = field
                # and the field takes its slot
                fields[slot] = field

        # sort the fields into measures
        measures = []
        # and derivations
        derivations = []
        # go through them
        for field in fields:
            # if it is a measure
            if cls.pyre_isMeasure(field):
                # add it to the measure pile
                measures.append(field)
            # if it is a derivation
            elif cls.pyre_isDerivation(field):
                # add it to the pile of derivations
                derivations.append(field)
            # otherwise
            else:
                # we have a problem; get the journal
                import journal

                # and complain
                raise journal.firewall("pyre.records").log(f"unknown field type: {field}")

        # attach them to the class record
        record.pyre_fields = tuple(fields)
        # filter the measures
        record.pyre_measures = tuple(measures)
        # the derivations
        record.pyre_derivations = tuple(derivations)
        # and the map of the fields it shadows to the ones that replace them
        record.pyre_shadows = shadows

        # a shadowing derivation may close a loop among the derivations
        cls.pyre_checkLoops(record=record)

        # all done
        return record

    def __init__(self, name, bases, attributes, **kwds):
        """
        Decorate a newly minted record

        Now that the class record is built and all the meta-data have been harvested, we can
        build the generators of my instances. There are two of them: one for immutable instances,
        built using a named tuple whose fields are the actual values of the various fields;
        and one for mutable instances, built from a named tuple whose fields are {pyre.calc}
        nodes.
        """
        # chain up
        super().__init__(name, bases, attributes, **kwds)

        # the map from my fields to their positions in the tuples of my instances
        columns = {}
        # add selectors for all my fields we removed in {__new__}
        for index, field in enumerate(self.pyre_fields):
            # map this field to its column number
            columns[field] = index
            # build a selector
            selector = self.pyre_selector(field=field, index=index)
            # attach it
            setattr(self, field.name, selector)
        # the fields i shadow lead to the columns of the fields that replace them, so code that
        # holds the field of a base finds the column it means
        for shadowed, field in self.pyre_shadows.items():
            # one at a time
            columns[shadowed] = columns[field]
        # attach the column map
        self.pyre_columns = columns

        # build value accessors for the data tuples
        attributes = dict(
            # map the name of the field to an accessor
            (field.name, self.pyre_accessor(field=field, index=index))
            # for each of my fields
            for index, field in enumerate(self.pyre_fields)
        )

        # build the helper classes that generate my instances: the mutable ones
        mutable = type("mutable", (self.pyre_mutableTupleType,), attributes)
        # and the immutable ones
        immutable = type("immutable", (self.pyre_immutableTupleType,), attributes)

        # if i have derivations
        if self.pyre_derivations:
            # attach the value extraction strategies that are aware of derivations: one that
            # builds the nodes of mutable instances
            mutable.pyre_extract = self.pyre_compiler()
            # and one that evaluates the values of immutable ones
            immutable.pyre_extract = self.pyre_evaluator()
        # otherwise
        else:
            # attach the fast value extraction strategies: one for mutable instances
            mutable.pyre_extract = self.pyre_calculator()
            # and one for immutable ones
            immutable.pyre_extract = self.pyre_extractor()

        # mark them as mine: the mutable instances
        mutable.pyre_layout = self
        # and the immutable ones
        immutable.pyre_layout = self
        # and attach them: the mutable helper
        self.pyre_mutableTuple = mutable
        # and the immutable one
        self.pyre_immutableTuple = immutable

        # all done
        return

    # predicates
    @classmethod
    def pyre_isMeasure(cls, field):
        """
        Predicate that tests whether {field} is a measure
        """
        # easy...
        return field.category == "descriptor"

    @classmethod
    def pyre_isDerivation(cls, field):
        """
        Predicate that tests whether {field} is a derivation
        """
        # easy...
        return field.category == "operator"

    # consistency checks
    @classmethod
    def pyre_checkLoops(cls, record):
        """
        Fire a firewall if a derivation of {record} depends on itself, which a shadowing
        derivation can make happen
        """
        # the derivations whose operands lead to no loop
        done = set()
        # go through the derivations of the record
        for derivation in record.pyre_derivations:
            # follow its operands
            loop = cls.pyre_findLoop(
                node=derivation, shadows=record.pyre_shadows, path=[], done=done
            )
            # if they lead back to a derivation on the way
            if loop is not None:
                # name the fields around the loop
                names = " -> ".join(f"'{step.name}'" for step in loop if step.name is not None)
                # get the journal
                import journal

                # make a channel
                channel = journal.firewall("pyre.records")
                # and complain
                channel.log(
                    f"the derivations of '{record.pyre_name}' depend on themselves: {names}"
                )
                # one loop is enough to report
                break
        # all done
        return record

    @classmethod
    def pyre_findLoop(cls, node, shadows, path, done):
        """
        Follow the operands of {node} to the fields they stand for, and return the nodes around
        a loop that comes back to one on {path}, or {None}; the nodes are compared by identity,
        since their {__eq__} builds expressions
        """
        # a node the record shadows stands for the field that replaces it
        node = shadows.get(node, node)
        # only derivations have operands to follow
        if not cls.pyre_isDerivation(node):
            # so the others lead nowhere
            return None
        # a node already on the path
        for start, step in enumerate(path):
            # closes a loop
            if step is node:
                # from where it was met first, back to it
                return path[start:] + [node]
        # a node whose operands were followed already
        if id(node) in done:
            # leads nowhere new
            return None
        # otherwise, step onto it
        path.append(node)
        # and follow each of its operands
        for operand in node.operands:
            # looking for a loop
            loop = cls.pyre_findLoop(node=operand, shadows=shadows, path=path, done=done)
            # and report the first one
            if loop is not None:
                # by handing it over
                return loop
        # step back off the node
        path.pop()
        # and remember that it leads to no loop
        done.add(id(node))
        # all done
        return None


# end of file
