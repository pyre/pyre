# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import datetime
import decimal
import uuid

# the exceptions of the package
from ... import exceptions

# the special value {NULL}
from ...schema import literals

# superclass
from .Visitor import Visitor


# declaration
class Parameters(Visitor):
    """
    The values of a statement that travel beside it, rather than inside it as literals

    Each value is checked by the literals of the language, so a value they refuse is refused
    here too; it is then kept in the form the bindings of the back end take, and a placeholder
    takes its place in the statement. A value of a column takes a bare placeholder, which the
    column gives a type; a value that belongs to no column is cast to the type its literal would
    have carried, since nothing else says what it is

    The slots of a prepared statement take placeholders the same way, but their values are given
    later, when {bind} fills them in; a slot that appears more than once takes one placeholder
    """

    # the types of the values that belong to no column, by the type of the value
    types = {
        bool: "BOOLEAN",
        float: "DOUBLE PRECISION",
        decimal.Decimal: "NUMERIC",
        str: "CLOB",
        bytes: "BLOB",
        datetime.date: "DATE",
        datetime.time: "TIME",
        datetime.datetime: "TIMESTAMP",
    }
    # and of the integers, by the bits they need
    integers = ((32, "INTEGER"), (64, "BIGINT"))

    # interface
    def literal(self, table, column, value):
        """
        Keep {value}, a value of {column} of {table}, and render its placeholder
        """
        # {NULL} is the same whatever the column
        if value is literals.null:
            # so it is written as it is
            return "NULL"
        # keep the value in the form the bindings take
        self._values.append(self.bound(table=table, column=column, value=value))
        # and leave it to the column to give its placeholder a type
        return self._placeholder()

    def bound(self, table, column, value):
        """
        Build the form the bindings take of {value}, a value of {column} of {table}; a missing
        value and {NULL} are both {None}
        """
        # a missing value and {NULL}
        if value is None or value is literals.null:
            # are what the bindings take for {NULL}
            return None
        # let the literals refuse what the language has no type for
        self.mill._literals.literal(table=table, column=column, value=value)
        # convert the value to the type of the column
        value = column.coerce(value=value)
        # and hand over the form the bindings take
        return column._pyre_identify(authority=self, table=table, column=column, value=value)

    def placeholders(self, count):
        """
        Render the placeholders of a statement whose {count} values travel beside it, in order,
        without keeping any values
        """
        # one per value
        return tuple(self._numbered(index=index) for index in range(1, count + 1))

    def value(self, value):
        """
        Keep {value}, a value that belongs to no column, and render its placeholder
        """
        # {NULL} is the same whatever its type
        if value is None or value is literals.null:
            # so it is written as it is
            return "NULL"
        # let the literals refuse what the language has no literal for
        text = self.mill._literals.value(value=value)
        # the type of its placeholder
        cast = self._cast(value=value)
        # a value whose type a placeholder cannot carry
        if cast is None:
            # keeps its literal, which the literals have already checked
            return text
        # keep it in the form the bindings take
        self._values.append(self._handlers[type(value)](schema=None, value=value))
        # and render its placeholder, with its type
        return self._typed(placeholder=self._placeholder(), cast=cast)

    def slot(self, table, column, parameter):
        """
        Keep {parameter}, a slot for a value of {column} of {table}, and render its placeholder
        """
        # its value takes the type of the column when it is given
        index = self._keep(
            parameter=parameter,
            convert=lambda value: self.bound(table=table, column=column, value=value),
        )
        # and the column gives its placeholder a type
        return self._numbered(index=index)

    def valueSlot(self, parameter):
        """
        Keep {parameter}, a slot for a value that belongs to no column, and render its placeholder
        """
        # the type of the slot is the only thing that says what it holds
        schema = parameter.schema
        # so a slot that does not say
        if schema is None:
            # is a mistake in the code that declared it
            import journal

            # so complain
            raise journal.firewall("pyre.db").log(
                f"the slot {parameter.name!r} stands where no column gives it a type, so it must "
                f"say what it holds"
            )
        # its value takes the type of the slot when it is given
        index = self._keep(
            parameter=parameter, convert=lambda value: self._schemaValue(schema=schema, value=value)
        )
        # and its placeholder says what it is
        return self._typed(
            placeholder=self._numbered(index=index), cast=self.mill._columns.cast(schema=schema)
        )

    def countSlot(self, parameter):
        """
        Keep {parameter}, a slot for the number of rows a bound of a selection counts, and render
        its placeholder
        """
        # the type of its value, which my mill knows
        schema = self.mill.rowCount
        # its value takes that type when it is given
        index = self._keep(
            parameter=parameter, convert=lambda value: self._schemaValue(schema=schema, value=value)
        )
        # and the place of the bound says what it is, so its placeholder is bare
        return self._numbered(index=index)

    def slots(self):
        """
        Generate the slots kept since the last call to {drain}, by name, with their placeholders
        """
        # go through them, in the order of their placeholders
        for name, (index, _) in self._slots.items():
            # and hand each one over
            yield name, index
        # all done
        return

    def bind(self, values):
        """
        Build the values of the statement in the order of their placeholders, with each slot filled
        by its entry in {values}, converted to the type it stands for
        """
        # a value for a slot the statement does not have
        unknown = sorted(set(values) - set(self._slots))
        # is a mistake
        if unknown:
            # so refuse it
            raise exceptions.InterfaceError(
                diagnostic=f"the statement has no slots for {', '.join(map(repr, unknown))}"
            )
        # and so is a slot without a value
        missing = [name for name in self._slots if name not in values]
        # so refuse that too
        if missing:
            # naming the slots
            raise exceptions.InterfaceError(
                diagnostic=f"no values for the slots {', '.join(map(repr, missing))}"
            )
        # start with the values that were kept as the statement was built
        bound = list(self._values)
        # and fill in the slots
        for name, (index, convert) in self._slots.items():
            # with their values, converted
            bound[index - 1] = convert(values[name])
        # hand them over
        return tuple(bound)

    def drain(self):
        """
        Hand over the values kept since the last call, in the order of their placeholders, and
        start over, so the next statement numbers its placeholders from the first
        """
        # the values
        values = tuple(self._values)
        # start over, with no values
        self._values = []
        # and no slots
        self._slots = {}
        # and hand them over
        return values

    # the forms the bindings take, by the type of the column
    def _pyre_onSchema(self, schema, value, **kwds):
        """
        Keep a value as it is
        """
        # which is how the bindings take most values
        return value

    def _pyre_onBoolean(self, schema, value, **kwds):
        """
        Keep a truth value
        """
        # as it is
        return value

    def _pyre_onDecimal(self, schema, value, **kwds):
        """
        Keep a fixed point number
        """
        # as it is
        return value

    def _pyre_onDate(self, schema, value, **kwds):
        """
        Keep a date
        """
        # as it is
        return value

    def _pyre_onTime(self, schema, value, **kwds):
        """
        Keep a time of day
        """
        # as it is
        return value

    def _pyre_onTimestamp(self, schema, value, **kwds):
        """
        Keep a moment in time
        """
        # as it is
        return value

    def _pyre_onJSON(self, schema, value, **kwds):
        """
        Keep a json document
        """
        # as it is
        return value

    # implementation details
    def _keep(self, parameter, convert):
        """
        Keep {parameter}, a slot whose values {convert} turns into the form the bindings take, and
        hand back the position of its placeholder
        """
        # a slot seen before
        if parameter.name in self._slots:
            # takes its placeholder again
            index, _ = self._slots[parameter.name]
            # so hand it back
            return index
        # the others hold a place among the values, filled in when the statement is bound
        self._values.append(None)
        # which is the position of their placeholder
        index = len(self._values)
        # remember it, with the conversion of the values
        self._slots[parameter.name] = (index, convert)
        # and hand it back
        return index

    def _schemaValue(self, schema, value):
        """
        Build the form the bindings take of {value}, given for a slot whose type is {schema}
        """
        # a missing value and {NULL}
        if value is None or value is literals.null:
            # are what the bindings take for {NULL}
            return None
        # convert the value to the type of the slot
        value = schema.coerce(value=value)
        # and hand over the form the bindings take
        return schema._pyre_identify(authority=self, value=value)

    def _placeholder(self):
        """
        Render the placeholder of the value kept last
        """
        # by its position among the values kept so far
        return self._numbered(index=len(self._values))

    def _numbered(self, index):
        """
        Render the placeholder of the value at {index}, counting from one
        """
        # the language marks every placeholder the same way, and fills them in order
        return "?"

    def _typed(self, placeholder, cast):
        """
        Render {placeholder}, which stands for a value of type {cast}
        """
        # by converting it, which is how the language gives a placeholder a type
        return f"CAST({placeholder} AS {cast})"

    def _cast(self, value):
        """
        Build the type of the placeholder of {value}, a value that belongs to no column; a value
        whose type a placeholder cannot carry has none
        """
        # an integer
        if type(value) is int:
            # takes the narrowest type that holds it
            for bits, name in self.integers:
                # among those the language has
                if -(2 ** (bits - 1)) <= value < 2 ** (bits - 1):
                    # and that is the one
                    return name
            # integers wider than all of them are fixed point numbers without a fraction
            return "NUMERIC"
        # the others are looked up by their type
        return self.types.get(type(value))

    # meta-methods
    def __init__(self, **kwds):
        # chain up
        super().__init__(**kwds)
        # the values of the statement in progress, in the order of their placeholders
        self._values = []
        # and its slots, by name, with the position of their placeholders and the conversion of
        # their values
        self._slots = {}
        # the forms the bindings take of the values that belong to no column, by their type
        self._handlers = {
            bool: self._pyre_onBoolean,
            int: self._pyre_onSchema,
            float: self._pyre_onSchema,
            decimal.Decimal: self._pyre_onDecimal,
            str: self._pyre_onSchema,
            bytes: self._pyre_onSchema,
            datetime.date: self._pyre_onDate,
            datetime.time: self._pyre_onTime,
            datetime.datetime: self._pyre_onTimestamp,
            uuid.UUID: self._pyre_onSchema,
            dict: self._pyre_onJSON,
        }
        # all done
        return


# end of file
