# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


from ..config.Slot import Slot as Base


class Slot(Base):
    """
    A specialization of {pyre.config.Slot} for storing the traits of components

    This slot enhances the calculation of the slot's value by running it through the casting
    and validation procedures specified by the associated trait
    """


    # interface
    def getValue(self):
        """
        Refresh my value, if necessary, and return it
        """
        # access my value
        value = self._value
        # if the value cache is not None, it contains a value that has already gone through the
        # descriptor's casting and validation process, so there is nothing further to do
        if value is not None: return value
        # access my evaluator
        evaluator = self._evaluator
        # further, uninitialized traits have both value and evaluator set to None; leave such
        # alone as well
        if evaluator is None: return None
        # the only case remaining is: null value but non-null evaluator
        # get the evaluator to compute the value
        try:
            value = evaluator.compute()
        # re-raise errors associated with unresolved nodes
        except self.UnresolvedNodeError as error:
            error.node = self
            raise
        # dress up anything else as an evaluation error
        except Exception as error:
            raise self.EvaluationError(evaluator=evaluator, error=error) from error
        #  bind my value
        return self.bind(value)
        

    def setValue(self, value, locator=None):
        """
        Set my value to {value} and notify my observers
        """
        # if {value} is an evaluator
        if isinstance(value, self.Evaluator):
            # get rid of mine, if i have one
            self._evaluator and self._evaluator.finalize(owner=self)
            # install this one
            self._evaluator = value
            # and initialize it
            self._evaluator.initialize(owner=self)
            # try to get it to compute the value
            try:
                value = self._evaluator.compute()
            # it is not ready yet...
            except self.UnresolvedNodeError as error:
                value = None
        # bind it
        return self.bind(value)


    def bind(self, value):
        """
        Walk {value} through casting and validation, refresg my cache and notify my observers
        """
        # walk {value} through casting and validation
        if value is not None:
            # access the processor
            processor = self._processor
            # cast {value}
            value = processor.type.pyre_cast(value)
            # convert it
            for converter in processor.converters:
                value = converter.pyre_cast(value)
            # validate it
            for validator in processor.validators:
                value = validator(value)
        # place it in the cache
        self._value = value
        # validate me
        self.validate()
        # and notify my observers
        self.notifyObservers()
        # and return
        return value

   
    # install value setter/getter as a property
    value = property(fget=getValue, fset=setValue, fdel=None, doc="Access to my value")


    # meta methods
    def __init__(self, processor, **kwds):
        super().__init__(**kwds)
        self._processor = processor
   

    # private data
    _processor = None


# end of file 
