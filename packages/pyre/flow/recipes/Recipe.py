# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import pyre

# the exceptions i raise
from ..exceptions import (
    DuplicateNodeError,
    IncompatibleBindingError,
    IncompatiblePinError,
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
        # look for a specification of the product that is unrelated to it
        offered = self.clash(factory=factory, slot=slot, product=product, expected=expected)
        # if there is one
        if offered is not None:
            # the slot cannot share the product
            raise IncompatibleBindingError(
                node=factory, slot=slot, product=product, expected=expected, offered=offered
            )
        # what the slot was bound to, if anything
        previous = self.binding(factory=factory, slot=slot)
        # forget it
        self.bindings = [b for b in self.bindings if (b.factory, b.slot) != (factory, slot)]
        # make the binding
        binding = Binding(factory=factory, slot=slot, product=product)
        # add it
        self.bindings.append(binding)
        # an instance that writes the product
        if maker.level == "instance" and trait.output:
            # makes it an instance too
            self.realize(product=product)
        # when both ends are instances
        if maker.level == "instance" and stock.level == "instance":
            # the binding is a live one, so make it
            setattr(maker.pin, slot, stock.pin)
        # the product the slot was bound to before
        if previous is not None and previous.product != product:
            # may have lost the last instance that writes it
            self.demote(product=previous.product)
        # hand off the binding
        return binding

    def pin(self, name: str, pin=None) -> list:
        """
        Pin the node {name} to {pin}, a class or an instance that satisfies its protocol, or to
        nothing, so it stands for any implementation of it again; a factory takes the slots of
        its new pin, so the bindings of the slots it no longer has are undone and handed back,
        and a slot it keeps must still expect a specification related to the ones its product
        has; a refused pin leaves the node as it was
        """
        # find the node
        node = self.node(name=name)
        # a pin that does not satisfy its protocol
        if pin is not None and node.protocol is not None and not node.admits(pin=pin):
            # cannot stand here
            raise IncompatiblePinError(node=name, pin=pin, protocol=node.protocol)
        # remember what it was pinned to
        previous = node.pin
        # a binding is live while both of its ends are instances
        live = lambda binding: all(
            self.node(name=end).level == "instance" for end in (binding.factory, binding.product)
        )
        # my bindings, which are the ones that may need undoing
        mine = [b for b in self.bindings if name in (b.factory, b.product)]
        # the live ones, which come undone if the new pin stands
        undo = [b for b in mine if live(b)]
        # try the new pin
        node.pin = pin
        # the slots the node has with its new pin, if it is a factory
        slots = node.slots if isinstance(node, Factory) else {}
        # the bindings of the slots a factory no longer has
        gone = [b for b in mine if b.factory == name and b.slot not in slots]
        # go through the bindings that stay
        for binding in (b for b in mine if b not in gone):
            # a factory's slot must still get along with its product
            if binding.factory == name:
                # what the slot expects now
                expected = node.slots[binding.slot].protocol
                # what clashes with it
                offered = self.clash(
                    factory=name, slot=binding.slot, product=binding.product, expected=expected
                )
            # a product's pin must satisfy every slot bound to it
            else:
                # what the slot expects
                expected = self.factoryNode(name=binding.factory).slots[binding.slot].protocol
                # what clashes with it
                offered = None if pin is None or pin.pyre_isCompatible(spec=expected) else pin
            # if something clashes
            if offered is not None:
                # put the node back the way it was
                node.pin = previous
                # and complain
                raise IncompatibleBindingError(
                    node=binding.factory,
                    slot=binding.slot,
                    product=binding.product,
                    expected=expected,
                    offered=offered,
                )
        # the pin stands; undo the live bindings that were made through the old pin
        for binding in undo:
            # the instance that holds it: the old pin of the node, or the factory at its other end
            holder = (
                previous if binding.factory == name else self.factoryNode(name=binding.factory).pin
            )
            # a reader loses the product, but a writer keeps what it made, whether or not anyone
            # reads it
            if holder.pyre_trait(alias=binding.slot).input:
                # so clear the slot of a reader
                setattr(holder, binding.slot, None)
        # forget the bindings of the slots that are gone
        self.bindings = [b for b in self.bindings if b not in gone]
        # and make the ones that are live with the new pin
        for binding in (b for b in mine if b not in gone and live(b)):
            # by setting the slot of the factory's instance to the product's
            setattr(
                self.factoryNode(name=binding.factory).pin,
                binding.slot,
                self.productNode(name=binding.product).pin,
            )
        # a factory changes what its outputs are
        if isinstance(node, Factory):
            # go through the bindings of its slots that stay
            for binding in (b for b in mine if b.factory == name and b not in gone):
                # an instance that writes a product
                if node.level == "instance" and self.writes(binding=binding):
                    # makes it an instance too
                    self.realize(product=binding.product)
            # go through the products it was bound to
            for product in {b.product for b in mine if b.factory == name}:
                # each of which may have lost the last instance that writes it
                self.demote(product=product)
        # hand off the bindings that are gone
        return gone

    def realize(self, product: str) -> None:
        """
        Make {product} an instance, now that an instance writes it: the one that instance holds
        in the slot bound to it, when it satisfies everything the product must, or else a new
        instance of the class the product is pinned to or of the default of its most refined
        specification, which the writer then holds; a product that is an instance already is
        left alone
        """
        # find the product
        stock = self.productNode(name=product)
        # one that is an instance already
        if stock.level == "instance":
            # is left alone
            return
        # the most refined of what it must satisfy
        spec = self.specification(product=product)
        # the instances that write it, with the slots they write it through
        writers = [
            (self.factoryNode(name=b.factory).pin, b.slot)
            for b in self.writers(product=product)
            if self.factoryNode(name=b.factory).level == "instance"
        ]
        # with none
        if not writers:
            # it stays as it is
            return
        # the first one, and its slot
        holder, slot = writers[0]
        # the instance the first writer holds in its slot
        held = getattr(holder, slot)
        # it will do if it satisfies the specification and is of the class the product is
        # pinned to, if it is pinned to one
        fits = (
            held is not None
            and (spec is None or held.pyre_isCompatible(spec=spec))
            and (stock.level != "class" or isinstance(held, stock.pin))
        )
        # if it does not
        if not fits:
            # make one of the class the product is pinned to, or of the default of its
            # specification
            held = self.fresh(cls=stock.pin if stock.level == "class" else None, spec=spec)
        # a specification with no implementation to fall back on
        if held is None:
            # leaves the product as it is
            return
        # remember what the product was pinned to, so i can undo it
        self.realized[product] = stock.pin
        # pin the product to it, which makes every binding to it live
        self.pin(name=product, pin=held)
        # all done
        return

    def fresh(self, spec, cls=None):
        """
        Make a product that nobody has named, of {cls} or else of the default of {spec}, so it
        is a new one rather than the one the framework hands back for a name it has seen; a
        specification with no default makes nothing
        """
        # without a class
        if cls is None:
            # use the default of the specification
            cls = spec.pyre_default()
        # a foundry
        if isinstance(cls, pyre.foundry):
            # hands out the class it stands for
            cls = cls()
        # a specification with no default
        if cls is None:
            # makes nothing
            return None
        # make one and hand it off
        return cls()

    def demote(self, product: str) -> None:
        """
        Send {product} back to whatever it was pinned to before i made it an instance, when no
        instance writes it any more; a product someone else pinned is left alone
        """
        # one that i did not make an instance, or that is no longer mine
        if product not in self.realized or product not in self.nodes:
            # is left alone
            return
        # one that an instance still writes
        if any(
            self.factoryNode(name=b.factory).level == "instance"
            for b in self.writers(product=product)
        ):
            # stays an instance
            return
        # it goes back to what it was pinned to before, and is no longer mine
        self.pin(name=product, pin=self.realized.pop(product))
        # all done
        return

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
        # when both ends are instances, the binding was a live one; a reader loses the product,
        # but a writer keeps what it made, whether or not anyone reads it
        if maker.level == "instance" and stock.level == "instance" and self.reads(binding=binding):
            # so clear the slot of a reader
            setattr(maker.pin, slot, None)
        # the product may have lost the last instance that writes it
        self.demote(product=binding.product)
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

    def ordered(self) -> list:
        """
        My factories, each one after the factories that make its inputs, in the order they were
        added wherever the data does not decide
        """
        # the factories, in the order they were added
        pending = list(self.factories())
        # the factories each one waits for, by name: the makers of its inputs, other than itself
        upstream = {
            node.name: {
                writer.factory
                for reader in self.bindings
                if reader.factory == node.name and self.reads(binding=reader)
                for writer in self.writers(product=reader.product)
                if writer.factory != node.name
            }
            for node in pending
        }
        # the factories in flow order
        ordered = []
        # and the names of the ones that have their places
        placed = set()
        # until every factory has a place
        while pending:
            # the first one whose upstream factories all have their places goes next; a cycle
            # leaves none, and then the first one in line breaks it
            ready = next(
                (node for node in pending if upstream[node.name] <= placed),
                pending[0],
            )
            # place it
            ordered.append(ready)
            # remember that it has its place
            placed.add(ready.name)
            # and take it out of line
            pending.remove(ready)
        # hand off the order
        return ordered

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

    def clash(self, factory: str, slot: str, product: str, expected):
        """
        Find a specification of {product}, other than the one {slot} of {factory} contributes,
        that is no refinement of {expected}, either way, or nothing when they all get along
        """
        # go through what the product has, other than through this very slot
        for offered in self.specifications(product=product, skip=(factory, slot)):
            # a specification that is no refinement of the other, either way
            if not (issubclass(expected, offered) or issubclass(offered, expected)):
                # is the one
                return offered
        # they all get along
        return None

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

    def stage(self, *, catalog=None, products: dict | None = None):
        """
        Choose a c++ engine from {catalog} for every one of my factories, given the types of the
        {products} that are pinned, and hand back the plan that realizes graphs of them
        """
        # the plan knows how
        from .Plan import Plan

        # stage me
        return Plan.stage(recipe=self, catalog=catalog, products=products)

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
        # a node is named after its instance, but an instance that has no name of its own is
        # named after its role in the flow: the name of the trait of the flow that holds it, if
        # any, by identity
        roles = {
            id(flow.pyre_inventory[trait].value): trait.name for trait in flow.pyre_facilities()
        }
        # go through the factories of the flow
        for factory in flow.pyre_factories():
            # its name, or else its role
            name = factory.pyre_name or roles.get(id(factory))
            # add each one, pinned to itself
            node = recipe.factory(name=recipe.vacant(name=name), pin=factory)
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
                    # name it after itself, or its role in the flow, or else the way the framework
                    # names what a factory makes for itself, after the factory and the slot
                    name = product.pyre_name or roles.get(id(product)) or f"{node.name}.{slot}"
                    # add it, pinned to itself
                    name = recipe.product(name=recipe.vacant(name=name), pin=product).name
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
        # the products i made instances of because an instance writes them, with what each was
        # pinned to before
        self.realized = {}
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
