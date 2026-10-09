# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# the exceptions i raise
from ..exceptions import (
    DuplicateNodeError,
    IncompatibleBindingError,
    UnknownNodeError,
    UnknownSlotError,
)

# my parts
from .Binding import Binding
from .Factory import Factory
from .Product import Product


# a graph of protocols, some of them pinned
class Recipe:
    """
    A flow graph described by what each node must be rather than what it is: every factory and
    product is a protocol, optionally pinned to a class or an instance, and the bindings join the
    slots of the factories to the products by name; staging makes whatever is not an instance
    """

    # interface
    def factories(self):
        """
        Iterate over my factories, in the order they were added
        """
        # filter my nodes
        yield from (node for node in self.nodes.values() if isinstance(node, Factory))
        # all done
        return

    def products(self):
        """
        Iterate over my products, in the order they were added
        """
        # filter my nodes
        yield from (node for node in self.nodes.values() if isinstance(node, Product))
        # all done
        return

    def factory(self, name: str, protocol=None, pin=None, settings: dict | None = None) -> Factory:
        """
        Add a factory {name} that satisfies {protocol}, optionally pinned to a class or an
        instance, along with the {settings} to apply once it is made
        """
        # make the node
        node = Factory(name=name, protocol=protocol, pin=pin, settings=settings)
        # add it
        return self.adopt(node=node)

    def product(self, name: str, specification=None, pin=None) -> Product:
        """
        Add a product {name} that satisfies {specification}, optionally pinned to a class or an
        instance; a product with no specification takes what its bindings say
        """
        # make the node
        node = Product(name=name, protocol=specification, pin=pin)
        # add it
        return self.adopt(node=node)

    def node(self, name: str):
        """
        Look up the node {name}
        """
        # look it up
        node = self.nodes.get(name)
        # if it is not there
        if node is None:
            # complain
            raise UnknownNodeError(node=name)
        # otherwise, hand it off
        return node

    def remove(self, name: str) -> None:
        """
        Remove the node {name}, along with its bindings
        """
        # find the node, which also makes sure it is there
        self.node(name=name)
        # go through the bindings that involve it
        for binding in [b for b in self.bindings if name in (b.factory, b.product)]:
            # and undo each one
            self.unbind(factory=binding.factory, slot=binding.slot)
        # and forget the node
        del self.nodes[name]
        # all done
        return

    def bind(self, factory: str, slot: str, product: str) -> Binding:
        """
        Bind {slot} of {factory} to {product}, replacing whatever it was bound to; the slot must
        expect a specification related to the ones the product already has, one way or the other
        """
        # find the factory
        maker = self.factoryNode(name=factory)
        # and the product
        stock = self.productNode(name=product)
        # look up the slot
        trait = maker.slots.get(slot)
        # if it is not there
        if trait is None:
            # complain
            raise UnknownSlotError(node=factory, slot=slot)
        # what the slot expects
        expected = trait.protocol
        # go through what the product already has, other than through this very slot
        for offered in self.specifications(product=product, skip=(factory, slot)):
            # a specification that is no refinement of the other, either way
            if not (issubclass(expected, offered) or issubclass(offered, expected)):
                # cannot share a product
                raise IncompatibleBindingError(
                    node=factory, slot=slot, product=product, expected=expected, offered=offered
                )
        # forget whatever the slot was bound to
        self.bindings = [b for b in self.bindings if (b.factory, b.slot) != (factory, slot)]
        # make the binding
        binding = Binding(factory=factory, slot=slot, product=product)
        # add it
        self.bindings.append(binding)
        # when both ends are instances
        if maker.level == "instance" and stock.level == "instance":
            # the binding is a live one, so make it
            setattr(maker.pin, slot, stock.pin)
        # hand off the binding
        return binding

    def unbind(self, factory: str, slot: str) -> Binding | None:
        """
        Undo the binding of {slot} of {factory}, and hand it back, or nothing if it was unbound
        """
        # find the binding
        binding = self.binding(factory=factory, slot=slot)
        # if there is none
        if binding is None:
            # there is nothing to undo
            return None
        # forget it
        self.bindings.remove(binding)
        # find the factory
        maker = self.factoryNode(name=factory)
        # and the product
        stock = self.productNode(name=binding.product)
        # when both ends are instances
        if maker.level == "instance" and stock.level == "instance":
            # the binding was a live one, so undo it
            setattr(maker.pin, slot, None)
        # hand off the binding
        return binding

    def binding(self, factory: str, slot: str) -> Binding | None:
        """
        Find the binding of {slot} of {factory}, if any
        """
        # look through my bindings
        return next(
            (b for b in self.bindings if b.factory == factory and b.slot == slot),
            None,
        )

    def readers(self, product: str) -> list:
        """
        The bindings through which factories read {product}
        """
        # filter my bindings
        return [b for b in self.bindings if b.product == product and self.reads(binding=b)]

    def writers(self, product: str) -> list:
        """
        The bindings through which factories write {product}
        """
        # filter my bindings
        return [b for b in self.bindings if b.product == product and self.writes(binding=b)]

    def reads(self, binding: Binding) -> bool:
        """
        Check whether the factory of {binding} reads its product
        """
        # ask the slot
        return bool(self.factoryNode(name=binding.factory).slots[binding.slot].input)

    def writes(self, binding: Binding) -> bool:
        """
        Check whether the factory of {binding} writes its product
        """
        # ask the slot
        return bool(self.factoryNode(name=binding.factory).slots[binding.slot].output)

    def specifications(self, product: str, skip: tuple | None = None):
        """
        Iterate over what {product} must satisfy: the specification it was declared with, and the
        ones the slots bound to it expect, except the slot named by {skip}
        """
        # find the product
        stock = self.productNode(name=product)
        # if it was declared with a specification
        if stock.specification is not None:
            # that is the first one
            yield stock.specification
        # go through its bindings
        for binding in self.bindings:
            # skipping the ones to other products
            if binding.product != product:
                # on to the next
                continue
            # and the one to skip
            if (binding.factory, binding.slot) == skip:
                # on to the next
                continue
            # what the slot expects
            yield self.factoryNode(name=binding.factory).slots[binding.slot].protocol
        # all done
        return

    def specification(self, product: str):
        """
        The most refined of the specifications {product} must satisfy, or nothing when there are
        none
        """
        # the most refined so far
        refined = None
        # go through the specifications
        for spec in self.specifications(product=product):
            # one that refines the best so far
            if refined is None or issubclass(spec, refined):
                # takes over
                refined = spec
        # hand it off
        return refined

    # factories of recipes
    @classmethod
    def harvest(cls, flow):
        """
        Describe the factories of {flow} and the products they are bound to as a recipe, with
        every node pinned to its instance
        """
        # make a recipe
        recipe = cls()
        # the names of the nodes of the products, by product identity
        products = {}
        # go through the factories of the flow
        for factory in flow.pyre_factories():
            # add each one, pinned to itself
            node = recipe.factory(name=recipe.vacant(name=factory.pyre_name), pin=factory)
            # go through its slots
            for slot, trait in node.slots.items():
                # find the product bound to it
                product = factory.pyre_inventory[trait].value
                # a slot that is not bound
                if product is None:
                    # has nothing to record
                    continue
                # look up the node of the product
                name = products.get(id(product))
                # if it does not have one yet
                if name is None:
                    # add it, pinned to itself
                    name = recipe.product(
                        name=recipe.vacant(name=product.pyre_name), pin=product
                    ).name
                    # and remember it
                    products[id(product)] = name
                # record the binding, which the flow already has
                recipe.bindings.append(Binding(factory=node.name, slot=slot, product=name))
        # hand off the recipe
        return recipe

    # metamethods
    def __init__(self, **kwds):
        # chain up
        super().__init__(**kwds)
        # my nodes, by name, in the order they were added
        self.nodes = {}
        # and my bindings, in the order they were made
        self.bindings = []
        # all done
        return

    # implementation details
    def adopt(self, node):
        """
        Add {node} under its name, which must not be taken
        """
        # get its name
        name = node.name
        # if it is taken
        if name in self.nodes:
            # complain
            raise DuplicateNodeError(node=name)
        # otherwise, file the node
        self.nodes[name] = node
        # and hand it off
        return node

    def vacant(self, name: str) -> str:
        """
        The first of {name}, {name}.1, {name}.2, ... that is not the name of one of my nodes
        """
        # start with the name itself
        candidate = name
        # and a counter
        count = 0
        # while the candidate is taken
        while candidate in self.nodes:
            # try the next one
            count += 1
            # by numbering it
            candidate = f"{name}.{count}"
        # hand it off
        return candidate

    def factoryNode(self, name: str) -> Factory:
        """
        Look up the factory {name}
        """
        # look it up
        node = self.nodes.get(name)
        # if it is not a factory
        if not isinstance(node, Factory):
            # complain
            raise UnknownNodeError(node=name)
        # otherwise, hand it off
        return node

    def productNode(self, name: str) -> Product:
        """
        Look up the product {name}
        """
        # look it up
        node = self.nodes.get(name)
        # if it is not a product
        if not isinstance(node, Product):
            # complain
            raise UnknownNodeError(node=name)
        # otherwise, hand it off
        return node


# end of file
