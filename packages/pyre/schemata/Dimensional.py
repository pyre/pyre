# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# the quantities, and the parser of their text
from ..units import dimensional as Quantity, parser as Parser

# the ways an evaluation can fail, the units can fail to mix, and a name can fail to be a unit
from ..calc.evaluation import errors
from ..units.exceptions import UnitError, UnknownUnitError

# the refusal of a builtin
from ..calc.exceptions import DisallowedNameError

# my superclass
from .Number import Number


# declaration
class Dimensional(Number):
    """
    A type declarator for quantities with units
    """

    # constants
    typename = "dimensional"  # the name of my type
    # the complaint about values that are not quantities
    complaint = "could not coerce {0.value!r} into a dimensional quantity"

    # public data
    # the parser of the text of quantities
    parser = Parser()

    # interface
    def coerce(self, value, **kwds):
        """
        Attempt to convert {value} into a dimensional quantity with my {units}
        """
        # quantities, and numbers, which are the quantities without units
        if self._measurable(value=value):
            # are checked against my units
            return self._check(value=value, candidate=value)
        # text
        if isinstance(value, str):
            # is parsed
            candidate = self._parse(value=value)
            # text that spells {None}
            if candidate is None:
                # is respected
                return None
            # anything else must evaluate to a quantity
            if not self._measurable(value=candidate):
                # and does not here
                raise self.CastingError(value=value, description=self.complaint)
            # which is checked against my units
            return self._check(value=value, candidate=candidate)
        # anything else is not a quantity
        raise self.CastingError(value=value, description=self.complaint)

    def json(self, value):
        """
        Generate a JSON representation of {value}
        """
        # represent as a string
        return self.string(value)

    # visiting
    def _pyre_identify(self, authority, **kwds):
        """
        Let {authority} know i am a dimensional quantity
        """
        # attempt to
        try:
            # ask {authority} for my handler
            handler = authority._pyre_onDimensional
        # if it doesn't understand
        except AttributeError:
            # chain up
            return super()._pyre_identify(authority=authority, **kwds)
        # otherwise, invoke the handler
        return handler(schema=self, **kwds)

    # meta-methods
    def __init__(self, units=None, quantity=None, **kwds):
        # chain up; with no default of my own, mine is {None}, as for any schema
        super().__init__(**kwds)
        # the name of what i measure, if there is one, is text
        if quantity is not None and (not isinstance(quantity, str) or not quantity.strip()):
            # and anything else is a mistake in the declaration
            self._firewall(
                message=f"the quantity of a dimensional must be a name, not {quantity!r}"
            )
        # units, if there are any, are given by a quantity that has them
        if units is not None and not isinstance(units, Quantity):
            # and anything else is a mistake in the declaration
            self._firewall(message=f"the units of a dimensional must be a quantity, not {units!r}")
        # save my units
        self.units = units
        # and the name of what i measure
        self.quantity = quantity
        # all done
        return

    # implementation details
    def _parse(self, value):
        """
        Evaluate the text in {value}, with the unit symbols in scope
        """
        # attempt to
        try:
            # invoke the {units} parser
            quantity = self.parser.parse(value, context=self.context)
        # if it uses a function or a name the value of a setting may not
        except DisallowedNameError as error:
            # say so, in words the user can act on
            raise self.CastingError(value=value, description=str(error), error=error)
        # if it uses a name the parser does not know
        except UnknownUnitError as error:
            # say which one
            raise self.CastingError(
                value=value,
                description=self.complaint + ": {0.error.name!r} is not a unit",
                error=error,
            )
        # if it fails in any of the ways an evaluation can, or its units don't mix
        except (*errors, UnitError) as error:
            # complain
            raise self.CastingError(value=value, description=self.complaint, error=error)
        # if all goes well, return the {quantity}
        return quantity

    def _measurable(self, value):
        """
        Check whether {value} is a quantity, or a number, which is a quantity without units
        """
        # quantities are
        if isinstance(value, Quantity):
            # clearly
            return True
        # and so are integers and floats, but not booleans, even though python counts them as
        # integers
        return isinstance(value, (int, float)) and not isinstance(value, bool)

    def _check(self, value, candidate):
        """
        Check that {candidate}, converted from {value}, has my units, and hand it back
        """
        # with no units of my own, or with units that match
        if self.units is None or self.units.isCompatible(candidate):
            # the {candidate} is fine
            return candidate
        # otherwise, spell out the units i expected
        expected = self._spell(value=self.units)
        # and the ones i got
        actual = self._spell(value=candidate)
        # when i know what i measure and it has units
        if self.quantity is not None and expected:
            # the complaint names both
            target = "units of {0.quantity!r} ({0.expected})"
        # when i know what i measure, but it has no units
        elif self.quantity is not None:
            # the complaint says so
            target = "units of {0.quantity!r} (none)"
        # when i only know my units
        elif expected:
            # the complaint names them
            target = "units of {0.expected}"
        # and otherwise
        else:
            # it says there are none
            target = "a quantity without units"
        # then it says what the value has instead
        reason = "it is in {0.actual}" if actual else "it has no units"
        # build the refusal
        refusal = self.CastingError(
            value=value, description=f"could not convert {{0.value!r}} to {target}: {reason}"
        )
        # with what i measure
        refusal.quantity = self.quantity
        # the units i expected
        refusal.expected = expected
        # and the ones i got
        refusal.actual = actual
        # and complain
        raise refusal

    def _spell(self, value):
        """
        Spell out the units of {value}; a number has no units, and spells nothing
        """
        # a number
        if not isinstance(value, Quantity):
            # has no units
            return ""
        # a quantity knows how to spell its own
        return value.label()

    def _firewall(self, message):
        """
        Report a mistake in the declaration of a dimensional, which is the developer's to fix
        """
        # access the journal
        import journal

        # and complain
        raise journal.firewall("pyre.schemata").log(message)


# end of file
