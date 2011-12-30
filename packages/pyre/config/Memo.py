# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


# support
import weakref
# superclass
from ..algebraic.Memo import Memo as Base


# class declaration
class Memo(Base):
    """
    This mix-in builds upon its base class from {pyre.algebraic} in order to handle observers
    that are classes, not just instances. This is necessary for the proper maintenance of the
    class inventory.

    In particular, {Memo} makes room for three additional special observers: a {configurator},
    a {componentClass} and a {componentInstance}. The last two are typically mutually
    exclusive, although {Memo} does not enforce this constraint.
    """


    # public data
    @property
    def configurator(self):
        """
        Return the configuration store that is registered as a dependent
        """
        # check and dereference the weak reference
        return self._configurator and self._configurator()

    @configurator.setter
    def configurator(self, configurator):
        """
        Register {configurator} as a dependent configuration store
        """
        # build a weak reference to the store
        self._configurator = weakref.ref(configurator) if configurator else None
        # and return
        return


    @property
    def componentClass(self):
        """
        Return the component class that is registered as a dependent
        """
        # check and dereference the weak reference
        return self._componentClass and self._componentClass()

    @componentClass.setter
    def componentClass(self, componentClass):
        """
        Register {componentClass} as a dependent component class
        """
        # build a weak reference to the component class
        self._componentClass = weakref.ref(componentClass) if componentClass else None
        # and return
        return


    @property
    def componentInstance(self):
        """
        Return the component instance that is registered as a dependent
        """
        # check and dereference the weak reference
        return self._componentInstance and self._componentInstance()

    @componentInstance.setter
    def componentInstance(self, componentInstance):
        """
        Register {componentInstance} as a dependent component instance
        """
        # build a weak reference to the component instance
        self._componentInstance = weakref.ref(componentInstance) if componentInstance else None
        # and return
        return


    # observer management
    def notifyObservers(self):
        """
        Notify my registered observers that my value has changed
        """
        # print("Memo.notifyObservers: node:", self)
        # access my configurator
        configurator = self.configurator
        # if i have one
        if configurator:
            # notify
            # print("  notifying configuration store", configurator)
            configurator.updatedProperty(slot=self)

        # access my component class
        componentClass = self.componentClass
        # if i have one
        if componentClass:
            # notify
            # print("  notifying component class", componentClass)
            componentClass.pyre_updatedClassProperty(slot=self)

        # access my component instance
        componentInstance = self.componentInstance
        # if i have one
        if componentInstance: 
            # notify
            # print("  notifying component instance", componentInstance)
            componentInstance.pyre_updatedProperty(slot=self)

        # notify my peer nodes
        return super().notifyObservers()


    def subsume(self, obsolete):
        """
        Remove {obsolete} from its upstream graph and assume its responsibilities
        """
        # print("Memo.subsume: node:", self, ", obsolete:", obsolete)
        # access my configurator
        configurator = obsolete.configurator
        # if I have one
        if configurator: 
            # notify
            # print("  updating configuration store", configurator)
            configurator.replaceSlot(current=obsolete, replacement=self)
            # consistency check
            if self.configurator: assert self.configurator == configurator

        # access my component class
        componentClass = obsolete.componentClass
        # if I have one
        if componentClass:
            # notify
            # print("  updating component class", componentClass)
            componentClass.pyre_replaceClassSlot(current=obsolete, replacement=self)
            # consistency check
            if self.componentClass: assert self.componentClass == componentClass

        # access my component instance
        componentInstance = obsolete.componentInstance
        # if I have one
        if componentInstance:
            # notify
            # print("  updating component instance", componentInstance)
            componentInstance.pyre_replaceSlot(current=obsolete, replacement=self)
            # consistency check
            if self.componentInstance: assert self.componentInstance == componentInstance

        # notify my peer nodes
        return super().subsume(obsolete=obsolete)
        

    # private data
    _configurator = None
    _componentClass = None
    _componentInstance = None
        


# end of file 
