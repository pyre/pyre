# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


import operator


class Dimensional:
    """
    This class comprises the fundamental representation of quantities with units
    """


    # meta methods
    def __init__(self, value, derivation):
        """
        Constructor:
            {value}: the magnitude
            {derivation}: a tuple of the exponents of the seven fundamental SI units
        """
        self.value = value
        self.derivation = derivation
        return


    # addition
    def __add__(self, other):
        """
        Addition
        """
        # check compatibility
        if not self.derivation == other.derivation:
            raise self.IncompatibleUnits("add")
        # otherwise build one and return it
        return Dimensional(self.value + other.value, self.derivation)


    # subtraction
    def __sub__(self, other):
        """
        Subtraction
        """
        # check compatibility
        if not self.derivation == other.derivation:
            raise self.IncompatibleUnits("subtract")
        # compute the value
        value = self.value - other.value
        # if it is zero, return a float
        if value == 0: return 0
        # otherwise build one and return it
        return Dimensional(self.value - other.value, self.derivation)


    # multiplication
    def __mul__(self, other):
        """
        Multiplication
        """
        # bail out quickly if {other} is 0
        if other == 0: return 0

        # attempt to interpret {other} as a dimensional
        try:
            value = self.value * other.value
        except AttributeError:
            # the only legal alternative is that {other} is a numeric type
            # scale the magnitude and return the new dimensional
            return Dimensional(other*self.value, self.derivation)
        # otherwise, compute the units
        derivation = tuple(map(operator.add, self.derivation, other.derivation))
        # if the units canceled out, return a float
        if derivation == self._zero: return value
        # otherwise build a new one and return it
        return Dimensional(value, derivation)


    # division
    def __truediv__(self, other):
        """
        True division
        """
        # attempt to interpret {other} as a dimensional
        try:
            value = self.value / other.value
        except AttributeError:
            # the only legal alternative is that {other} is a numaric type
            return Dimensional(self.value/other, self.derivation)
        # otherwise compute the units
        derivation = tuple(map(operator.sub, self.derivation, other.derivation))
        # check whether the units canceled
        if derivation == self._zero: return value
        # and return a new dimensional
        return Dimensional(value, derivation)


    # exponentiation
    def __pow__(self, other):
        """
        Exponentiation
        """
        # if the exponent is zero, return unit
        if other == 0: return 1 
        # otherwise compute magnitude
        value = self.value ** other
        # and dimensions
        derivation = tuple(map(operator.mul, [other]*7, self.derivation))
        # build a new dimensional and return it
        return Dimensional(value, derivation)
        

    # unary plus
    def __pos__(self):
        """
        Unary plus
        """
        # not much to do
        return self


    # unary minus
    def __neg__(self):
        """
        Unary minus
        """
        # return a new one with the value sign reversed
        return Dimensional(-self.value, self.derivation)


    # absolute value
    def __abs__(self):
        """
        Absolute value
        """
        # build a new one with positive value
        return Dimensional(abs(self.value), self.derivation)


    # inversion
    def __invert__(self):
        """
        Inversion
        """
        # compute the value
        value = 1/self.value
        # and the dimensions
        derivation = tuple(map(operator.mul, self._negativeOne, self.derivation))
        # build a new one and return it
        return Dimensional(value, derivation)


    # right multiplication
    def __rmul__(self, other):
        """
        Right multiplication
        """
        # if the left operand was a zero, return a zero
        if other == 0: return 0
        # build a new one and return it
        return Dimensional(other*self.value, self.derivation)


    # right division
    def __rtruediv__(self, other):
        """
        Right division
        """
        # if the left operand was a zero, return a zero
        if other == 0: return 0
        # otherwise compute the value
        value = other/self.value
        # and the dimensions
        derivation = tuple(map(operator.mul, self._negativeOne, self.derivation))
        # build a new one and return it
        return Dimensional(value, derivation)


    # coercion to float
    def __float__(self):
        """
        Conversion to float
        """
        # if i happen to be a disguised float, convert me
        if self.derivation == self._zero:
            # must cast explicitly because an actual float is expected
            return float(self.value)
        # otherwise
        raise self.InvalidConversion(self)


    # ordering
    def __lt__(self, other):
        """
        Ordering: less than
        """
        # if the dimensions match
        if self.derivation == other.derivation:
            # check
            return self.value < other.value
        # otherwise the operartion is illegal
        raise self.IncompatibleUnits("compare")

    def __le__(self, other):
        """
        Ordering: less than or equal to
        """
        if self.derivation == other.derivation:
            # check
            return self.value <= other.value
        # otherwise the operartion is illegal
        raise self.IncompatibleUnits("compare")

    def __eq__(self, other):
        """
        Ordering: equality
        """
        # check whether {other} is zero
        if other == 0: 
            # must be false since i convert dimensional to floats whenever possible
            # if this fails, it's a bug...
            # NYI: firewall this
            return False

        # if the dimensions match
        if self.derivation == other.derivation:
            # check
            return self.value == other.value
        # otherwise the operartion is illegal
        raise self.IncompatibleUnits("compare")

    def __ne__(self, other):
        """
        Ordering: not equal to
        """
        # if the dimensions match
        if self.derivation == other.derivation:
            # check
            return self.value != other.value
        # otherwise the operartion is illegal
        raise self.IncompatibleUnits("compare")

    def __gt__(self, other):
        """
        Ordering: greater than
        """
        # if the dimensions match
        if self.derivation == other.derivation:
            # check
            return self.value > other.value
        # otherwise the operartion is illegal
        raise self.IncompatibleUnits("compare")

    def __ge__(self, other):
        """
        Ordering: greater than or equal to
        """
        # if the dimensions match
        if self.derivation == other.derivation:
            # check
            return self.value >= other.value
        # otherwise the operartion is illegal
        raise self.IncompatibleUnits("compare")


    def __str__(self):
        """
        Conversion to str
        """
        return str(self.value) + ' ' + self._strDerivation()


    def __format__(self, code):
        """
        Formatting support

        The parameter {code} is a string of the form
            value={format_spec},base={scale},label={label}
        where
            {format_spec}: a format specification appropriate for representing floats
            {scale}: a dimensional quantity to be used as a scale for the value
            {label}: the label with units that should follow the magnitude of the quantity

        Example:
            >>> from pyre.units.SI import m,s
            >>> g = 9.81*m/s
            >>> "{accel:value=.2f,base={scale},label=g}".format(accel=100*m/s**2, scale=g)
            '10.2 g'
        """
        # spit out the code
        # establish the formatting defaults
        fields = {
            'value': '',
            'base': Dimensional(value=1, derivation=self.derivation),
            'label': self._strDerivation()
            }
        # if the user supplied a format specifier
        if code:
            # update the formatting fields
            fields.update(field.split('=') for field in code.split(','))
        # show what we have so far
        # get the fields
        value = fields['value']
        base = fields['base']
        label = fields['label']
        # convert the base specification if necessary
        if isinstance(base, str):
            # get the parser factory
            from . import parser
            # access the singleton
            p = parser()
            # make the conversion
            base = p.parse(base)
        # build the string and return it
        try:
            return format(self/base, value) + ' ' + label
        except TypeError as error:
            raise


    # implementation details
    def _strDerivation(self):
        """
        Build a representation of the fundamental unit labels raised to the exponents specified
        in my derivation.

        The unit parser can parse this textual representation and convert it back into a
        dimensional quantity.
        """
        return '*'.join(
            "{}**{}".format(label,exponent) if exponent != 1 else label
            for label, exponent in zip(self._fundamental, self.derivation) if exponent)
              

    # exceptions
    from .exceptions import IncompatibleUnits, InvalidConversion
            

    # private data
    _fundamental = ('kg', 'm', 's', 'A', 'K', 'mol', 'cd') # the SI fundamental units
    _zero = (0,) * len(_fundamental)
    _negativeOne = (-1, ) * len(_fundamental)


    # public data: default values
    value = 0
    derivation = _zero


# instances
one = dimensionless = Dimensional(1, Dimensional._zero)


# end of file 
