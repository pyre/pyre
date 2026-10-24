#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# the framework
import pyre

# the drawing
from Sequence import Sequence


# the app
class TraitValueSequence(pyre.application):
    """
    Draw the sequence of calls that carries a trait value from each of its sources to the
    trait, as a page with one sequence diagram
    """

    # user configurable state
    out = pyre.properties.ostream(default="trait-value-sequence.html")
    out.doc = "the page to write"

    # the design to draw
    design = pyre.properties.str(default="today")
    design.validators = pyre.constraints.isMember("today", "proposed")
    design.doc = "the design to draw: the path as it is [today], or the [proposed] one"

    # obligations
    @pyre.export
    def main(self, *args, **kwds) -> int:
        """
        Build the page and write it out
        """
        # look up the design to draw
        design = self.designs[self.design]
        # make the diagram
        diagram = Sequence(cols=design["cols"])
        # relate the heads: a slot is a node of the calc algebra
        diagram.relate(src="slot", dst="calc", kind="derives")
        # and the trait type derives from its schema
        diagram.relate(src="Trait", dst="Schema", kind="derives")
        # go through the scenarios, in the order they happen
        for index, scenario in enumerate(design["scenarios"]):
            # set each one apart from the one before
            if index:
                # with a faint rule
                diagram.section()
            # and draw it
            scenario(self, diagram=diagram)
        # render the diagram
        svg = diagram.render(label=design["label"])
        # put it in its page
        page = (
            f"<title>{design['title']}</title>"
            + self.style
            + f'<div class="wrap"><div class="prose"><h1>{design["title"]}</h1>'
            + design["intro"]
            + "</div>"
            + design["key"]
            + '<div class="fig">'
            + svg
            + "</div></div>"
        )
        # and write it out
        self.out.write(page)
        # all done
        return 0

    # the scenarios
    def boot(self, diagram: Sequence) -> None:
        """
        The command line, and the environment, deposited at boot
        """
        # the parser turns the command line into assignments
        diagram.trigger(label="boot", col="codec", sub="argv, at import")
        # say how
        diagram.note(
            col="codec", lines=["CommandLineParser turns --a.b=text into [Assignment] events"]
        )
        # the configurator processes them
        diagram.call(src="codec", dst="Configurator", label="processEvents")
        # one by one
        diagram.note(col="Configurator", lines=["for each assignment, at the [command] rank"])
        # each one goes into the store
        diagram.call(src="Configurator", dst="NameServer", label="insert")
        # before any trait has claimed its key
        diagram.note(
            col="NameServer",
            lines=[
                "the key is unknown, and so is its trait",
                "so the factory is the slot of [identity]",
            ],
        )
        # so the generic factory builds the slot
        diagram.call(src="NameServer", dst="SlotFactory", label="__call__")
        # and treats the text as the generic trait would
        diagram.note(
            col="SlotFactory", lines=["text goes through the macro of [identity]: an interpolation"]
        )
        # the interpolation compiles the text
        diagram.call(src="SlotFactory", dst="calc", label="interpolation")
        # resolving references as it goes
        diagram.note(
            col="calc",
            lines=[
                "compile the text",
                "each {name} is retrieved",
                "an unknown one becomes a [placeholder]",
            ],
        )
        # the result is the slot node
        diagram.call(src="calc", dst="slot", label="node")
        # which holds the source but no value yet
        diagram.note(col="slot", lines=["keeps the source text", "no value yet"])
        # back to the parser
        diagram.unwind("slot", "calc", "SlotFactory", "NameServer", "Configurator", "codec")
        # the environment takes the same path
        diagram.note(
            col="codec", lines=["Environ deposits [pyre.environ.*] the same way, at [boot] rank"]
        )
        # all done
        return

    def load(self, diagram: Sequence) -> None:
        """
        A configuration document, deposited when it is loaded
        """
        # the codec decodes the document into events
        diagram.trigger(label="loadConfiguration", col="codec", sub="pfg, yaml, cfg, pml")
        # whose values are text or objects, depending on the codec
        diagram.note(col="codec", lines=["decode: pfg gives text, yaml gives objects"])
        # the configurator processes them
        diagram.call(src="codec", dst="Configurator", label="processEvents")
        # plain assignments go into the store as at boot
        diagram.note(
            col="Configurator",
            lines=[
                "[Assignment]: as at boot, at [user] rank",
                "yaml objects take the [native] branch",
            ],
        )
        # leave a little room
        diagram.gap(h=4)
        # conditional assignments wait for their instance
        diagram.note(
            col="Configurator",
            lines=["[ConditionalAssignment], [family#name]:", "held in [deferred], not inserted"],
            kind="good",
        )
        # back to the codec
        diagram.ret(src="Configurator", dst="codec")
        # all done
        return

    def declare(self, diagram: Sequence) -> None:
        """
        A component class registers the defaults of its traits
        """
        # the class record builds its inventory
        diagram.trigger(label="class declared", col="Component", sub="Actor.__init__")
        # trait by trait
        diagram.note(col="Component", lines=["pyre_buildInventory, for every trait"])
        # each default goes into the store
        diagram.call(src="Component", dst="NameServer", label="insert")
        # at the lowest rank, with the trait's own factory
        diagram.note(
            col="NameServer", lines=["at [defaults] rank, with the [classSlot] of the trait"]
        )
        # a key that was only referred to gives way to the default
        diagram.note(col="NameServer", lines=["key holds a [placeholder]: build from the default"])
        # but a key that was deposited earlier is rebuilt from its value
        diagram.note(col="NameServer", lines=["key holds a value: rebuild it from [old.value]"])
        # by the trait's factory
        diagram.call(src="NameServer", dst="SlotFactory", label="__call__")
        # which gets the expanded text escaped, so it is not expanded again
        diagram.note(
            col="SlotFactory",
            lines=["text that was expanded already is escaped (pyre#40)"],
            kind="good",
        )
        # through the trait's macro
        diagram.call(src="SlotFactory", dst="calc", label="macro")
        # into a new slot node
        diagram.call(src="calc", dst="slot", label="node")
        # back to the class
        diagram.unwind("slot", "calc", "SlotFactory", "NameServer", "Component")
        # all done
        return

    def instantiate(self, diagram: Sequence) -> None:
        """
        A component instance registers its traits, then receives its deferred assignments
        """
        # the class makes an instance
        diagram.trigger(label="C(name=…)", col="Component", sub="Actor.__call__")
        # which first claims the global settings under its name
        diagram.note(col="Component", lines=["pull the global settings into its scope"])
        # by aliasing the short names
        diagram.call(src="Component", dst="NameServer", label="alias")
        # which keeps the setting with the higher rank
        diagram.note(
            col="NameServer",
            lines=[
                "merge [a] into [name.a], by rank",
                "a [placeholder] there has no processors to carry",
            ],
        )
        # back to the instance
        diagram.ret(src="NameServer", dst="Component")
        # then registers its traits
        diagram.note(col="Component", lines=["registerSlots, for every trait"])
        # each one goes into the store
        diagram.call(src="Component", dst="NameServer", label="insert")
        # at the lowest rank, following the class
        diagram.note(
            col="NameServer",
            lines=[
                "at [defaults] rank, a reference to the class slot",
                "followed until the instance first reads the trait",
            ],
            kind="good",
        )
        # a key that was only referred to gives way to the default
        diagram.note(col="NameServer", lines=["key holds a [placeholder]: build from the default"])
        # but an existing setting is rebuilt from its value
        diagram.note(col="NameServer", lines=["key holds a value: rebuild it from [old.value]"])
        # by the trait's factory
        diagram.call(src="NameServer", dst="SlotFactory", label="__call__", kind="bad")
        # which gets the expanded text escaped, so it is not expanded again
        diagram.note(
            col="SlotFactory",
            lines=["text that was expanded already is escaped (pyre#40)"],
            kind="good",
        )
        # but where a reference to a component that does not exist yet is evaluated too early
        diagram.note(
            col="SlotFactory",
            lines=["a forward reference raises [UnresolvedNodeError] (s43)"],
            kind="bad",
        )
        # through the trait's macro
        diagram.call(src="SlotFactory", dst="calc", label="macro")
        # into a new slot node
        diagram.call(src="calc", dst="slot", label="node")
        # back to the instance
        diagram.unwind("slot", "calc", "SlotFactory", "NameServer", "Component")
        # the configurator applies what it held for this instance
        diagram.call(src="Component", dst="Configurator", label="configureComponentInstance")
        # from its pile
        diagram.note(col="Configurator", lines=["the [deferred] pile for this instance"])
        # each held assignment goes into the store
        diagram.call(src="Configurator", dst="NameServer", label="insert", kind="good")
        # once the trait is known and with the source untouched
        diagram.note(
            col="NameServer",
            lines=["via [pyre_setTrait]", "the trait is known, and the source is intact"],
            kind="good",
        )
        # so the right factory builds the slot
        diagram.call(src="NameServer", dst="SlotFactory", label="__call__", kind="good")
        # in one pass
        diagram.note(col="SlotFactory", lines=["built once, by the right factory"], kind="good")
        # through the trait's macro
        diagram.call(src="SlotFactory", dst="calc", label="macro")
        # into the slot node
        diagram.call(src="calc", dst="slot", label="node")
        # back to the instance
        diagram.unwind("slot", "calc", "SlotFactory", "NameServer", "Configurator", "Component")
        # all done
        return

    def assign(self, diagram: Sequence) -> None:
        """
        Code assigns to a trait of a named component
        """
        # the assignment reaches the inventory
        diagram.trigger(label="c.t = value", col="Component", sub="explicit rank")
        # which sets the value of the trait
        diagram.note(col="Component", lines=["setTraitValue"])
        # in the store
        diagram.call(src="Component", dst="NameServer", label="insert")
        # with the trait known
        diagram.note(col="NameServer", lines=["at [explicit] rank, with the factory of the trait"])
        # whose factory builds the slot
        diagram.call(src="NameServer", dst="SlotFactory", label="__call__")
        # choosing by the python type of the value
        diagram.note(
            col="SlotFactory", lines=["text goes through the macro, anything else is [native]"]
        )
        # through a macro or a native node
        diagram.call(src="SlotFactory", dst="calc", label="macro · native")
        # into the slot node
        diagram.call(src="calc", dst="slot", label="node")
        # which takes the place of the old one
        diagram.note(
            col="slot",
            lines=["on a class: the instances that follow it see the change"],
            kind="good",
        )
        # back to the inventory
        diagram.unwind("slot", "calc", "SlotFactory", "NameServer", "Component")
        # all done
        return

    def delete(self, diagram: Sequence) -> None:
        """
        Code deletes a trait of a named component
        """
        # the deletion reaches the component
        diagram.trigger(label="del c.t", col="Component", sub="pyre_deleteTrait")
        # which can only give up a value it has
        diagram.note(
            col="Component",
            lines=[
                "still following its class: [TraitUnsetError]",
                "read or set: give the value up",
            ],
        )
        # by putting back what the trait started with
        diagram.call(src="Component", dst="NameServer", label="insert", kind="good")
        # whatever the rank of the value it replaces
        diagram.note(
            col="NameServer",
            lines=[
                "at [defaults] rank, claiming the node",
                "a reference to the class slot, followed again",
            ],
            kind="good",
        )
        # the factory takes the reference as it is
        diagram.call(src="NameServer", dst="SlotFactory", label="__call__")
        # which becomes the slot
        diagram.call(src="SlotFactory", dst="slot", label="replace")
        # back to the component
        diagram.unwind("slot", "SlotFactory", "NameServer", "Component")
        # all done
        return

    def read(self, diagram: Sequence) -> None:
        """
        The first read of a trait computes its value
        """
        # reading the trait asks the slot for its value
        diagram.trigger(label="c.t", col="slot", sub="first read only")
        # which is computed once
        diagram.note(col="slot", lines=["computed once, then kept"])
        # from the values of its operands
        diagram.call(src="slot", dst="calc", label="operands")
        # references contribute their text
        diagram.note(
            col="calc", lines=["the values of the referents are spliced as [str] (s25)"], kind="bad"
        )
        # except the unset ones
        diagram.note(
            col="calc", lines=["a [None] referent makes the value [None] (s45)"], kind="good"
        )
        # back to the slot
        diagram.ret(src="calc", dst="slot")
        # whose postprocessor is the trait
        diagram.call(src="slot", dst="Trait", label="process")
        # say so
        diagram.note(col="Trait", lines=["the postprocessor of the slot"])
        # unset stays unset
        diagram.note(
            col="Trait",
            lines=["[None], or text [none] in any case: the value is [None] (s44)"],
            kind="good",
        )
        # which first runs its converters
        diagram.note(col="Trait", lines=["converters, before the schema"])
        # then asks its schema to convert
        diagram.call(src="Trait", dst="Schema", label="coerce")
        # parsing the text a second time
        diagram.note(col="Schema", lines=["a second parse: eval, units, split, strptime"])
        # back to the trait
        diagram.ret(src="Schema", dst="Trait")
        # then applies its own rules
        diagram.note(col="Trait", lines=["normalizers, then validators"])
        # back to the slot
        diagram.ret(src="Trait", dst="slot")
        # which hands out the value
        diagram.note(col="slot", lines=["the trait's value"])
        # and, in an instance that follows its class, stops following
        diagram.note(
            col="slot",
            lines=[
                "an instance keeps what it read, like a cached property",
                "and remembers where it came from",
            ],
            kind="good",
        )
        # and is done
        diagram.end(col="slot")
        # all done
        return

    # the proposed scenarios
    def depositProposed(self, diagram: Sequence) -> None:
        """
        The command line, the environment, and documents deposit their values without a trait
        """
        # the codecs turn their sources into assignments
        diagram.trigger(label="boot, load", col="codec", sub="argv, environ, documents")
        # the same way for every source
        diagram.note(col="codec", lines=["every source makes [Assignment] events"])
        # with text or objects inside
        diagram.note(col="codec", lines=["yaml carries objects, the rest carry text"])
        # the configurator processes them
        diagram.call(src="codec", dst="Configurator", label="processEvents")
        # conditional assignments still wait for their instance
        diagram.note(
            col="Configurator",
            lines=["[family#name] waits in [deferred], as it does today"],
            kind="good",
        )
        # the rest go into the store, each at the rank of its source
        diagram.call(src="Configurator", dst="NameServer", label="insert", kind="good")
        # without asking which trait will claim the key
        diagram.note(
            col="NameServer",
            lines=[
                "no trait is involved, so there is no slot factory",
                "the source alone decides the kind of node",
            ],
            kind="good",
        )
        # the algebra builds the node from the source
        diagram.call(src="NameServer", dst="calc", label="template", kind="good")
        # one template mechanism for every trait
        diagram.note(
            col="calc",
            lines=[
                "text with a {name} becomes an [interpolation]",
                "anything else becomes a [variable]",
            ],
        )
        # whether a template may compute is undecided
        diagram.note(
            col="calc",
            lines=[
                "open: may a template do arithmetic? (Q2)",
                "open: what is the escape rule? (Q3)",
            ],
            kind="open",
        )
        # an unknown reference makes a placeholder, ranked below every source, as it is today
        diagram.note(
            col="calc",
            lines=[
                "an unknown {name} becomes a [placeholder]",
                "ranked [uninitialized], below [defaults], as today",
            ],
        )
        # the result is the slot
        diagram.call(src="calc", dst="slot", label="node")
        # which keeps everything needed to explain it later
        diagram.note(col="slot", lines=["keeps its [source], [rank] and [locator]"])
        # but has no type yet
        diagram.note(col="slot", lines=["no postprocessor yet"])
        # back to the codec
        diagram.unwind("slot", "calc", "NameServer", "Configurator", "codec")
        # all done
        return

    def declareProposed(self, diagram: Sequence) -> None:
        """
        A component class claims the keys of its traits, attaching itself to existing slots
        """
        # the class record builds its inventory
        diagram.trigger(label="class declared", col="Component", sub="Actor.__init__")
        # trait by trait
        diagram.note(col="Component", lines=["pyre_buildInventory, for every trait"])
        # each trait claims its key
        diagram.call(src="Component", dst="NameServer", label="claim", kind="good")
        # keeping a value that is already there
        diagram.note(col="NameServer", lines=["key holds a value: keep its slot"], kind="good")
        # and filling in the rest, without asking a placeholder for its value
        diagram.note(
            col="NameServer",
            lines=["key holds a placeholder, or nothing:", "insert the default at [defaults] rank"],
            kind="good",
        )
        # the trait becomes the postprocessor of the slot
        diagram.call(src="NameServer", dst="slot", label="postprocessor = trait", kind="good")
        # which invalidates the slot
        diagram.note(col="slot", lines=["flush the cache"], kind="good")
        # and everything that depends on it
        diagram.note(col="slot", lines=["dependents follow"], kind="good")
        # which the algebra already supports
        diagram.note(col="slot", lines=["tested by calc/postprocessor_late*"])
        # back to the class
        diagram.unwind("slot", "NameServer", "Component")
        # nothing has been checked yet
        diagram.note(
            col="Component",
            lines=["cost: a bad default surfaces at its first read, or at the check"],
            kind="bad",
        )
        # all done
        return

    def instantiateProposed(self, diagram: Sequence) -> None:
        """
        A component instance claims its keys, then receives its deferred assignments
        """
        # the class makes an instance
        diagram.trigger(label="C(name=…)", col="Component", sub="Actor.__call__")
        # which first claims the global settings under its name
        diagram.note(col="Component", lines=["pull the global settings into its scope"])
        # by aliasing the short names
        diagram.call(src="Component", dst="NameServer", label="alias")
        # which compares ranks and nothing else
        diagram.note(
            col="NameServer",
            lines=["merge by rank, without asking a node for its trait"],
            kind="good",
        )
        # so a placeholder, which has none, cannot crash it
        diagram.note(
            col="NameServer",
            lines=["a placeholder has no trait to carry, as today since s32 was fixed"],
            kind="good",
        )
        # back to the instance
        diagram.ret(src="NameServer", dst="Component")
        # then claims the keys of its traits
        diagram.note(col="Component", lines=["registerSlots, for every trait"])
        # each one
        diagram.call(src="Component", dst="NameServer", label="claim", kind="good")
        # keeping a value that is already there
        diagram.note(col="NameServer", lines=["key holds a value: keep its slot"], kind="good")
        # and filling in the rest from the class, without asking a placeholder for its value
        diagram.note(
            col="NameServer",
            lines=["key holds a placeholder, or nothing:", "refer to the class slot"],
            kind="good",
        )
        # a reference to a name nobody has set yet stays unevaluated
        diagram.note(
            col="NameServer",
            lines=["a forward reference is left pending, not evaluated (s43)"],
            kind="good",
        )
        # so the instance sees its class the way the instance of a python class does
        diagram.note(
            col="NameServer",
            lines=[
                "like a python instance: the class value until it has its own",
                "a class change reaches it; del gives the trait back (s51, done)",
            ],
            kind="good",
        )
        # the trait becomes the postprocessor of the slot
        diagram.call(src="NameServer", dst="slot", label="postprocessor = trait", kind="good")
        # back to the instance
        diagram.unwind("slot", "NameServer", "Component")
        # the configurator applies what it held for this instance
        diagram.call(src="Component", dst="Configurator", label="configureComponentInstance")
        # from its pile
        diagram.note(col="Configurator", lines=["the [deferred] pile for this instance"])
        # each held assignment goes into the store, outranking the default
        diagram.call(src="Configurator", dst="NameServer", label="insert", kind="good")
        # the algebra builds the node from the source
        diagram.call(src="NameServer", dst="calc", label="template", kind="good")
        # with the trait already attached
        diagram.call(src="calc", dst="slot", label="node")
        # say so
        diagram.note(col="slot", lines=["the trait is already its postprocessor"])
        # and the owner hears about the replacement
        diagram.call(src="slot", dst="Component", label="pyre_traitModified", kind="good")
        # which today happens only through pyre_setTrait
        diagram.note(
            col="Component",
            lines=["every replacement notifies the owner (s38)"],
            kind="good",
        )
        # back to the configurator
        diagram.ret(src="Component", dst="Configurator")
        # and to the instance
        diagram.ret(src="Configurator", dst="Component")
        # all done
        return

    def assignProposed(self, diagram: Sequence) -> None:
        """
        Code assigns to a trait of a named component
        """
        # the assignment reaches the inventory
        diagram.trigger(label="c.t = value", col="Component", sub="explicit rank")
        # which sets the value of the trait
        diagram.note(col="Component", lines=["setTraitValue"])
        # in the store
        diagram.call(src="Component", dst="NameServer", label="insert", kind="good")
        # the same path as every other source
        diagram.note(col="NameServer", lines=["at [explicit] rank, like any other source"])
        # the algebra builds the node from the source
        diagram.call(src="NameServer", dst="calc", label="template", kind="good")
        # text goes through the template, objects do not
        diagram.note(col="calc", lines=["text becomes a template, objects a [variable]"])
        # into the slot, with the trait attached
        diagram.call(src="calc", dst="slot", label="node")
        # and the owner hears about it
        diagram.call(src="slot", dst="Component", label="pyre_traitModified", kind="good")
        # back to the inventory
        diagram.end(col="Component")
        # all done
        return

    def readProposed(self, diagram: Sequence) -> None:
        """
        The first read of a trait computes its value, with one parse
        """
        # reading the trait asks the slot for its value
        diagram.trigger(label="c.t", col="slot", sub="first read only")
        # which is computed once
        diagram.note(col="slot", lines=["computed once, then kept"])
        # from the values of its operands
        diagram.call(src="slot", dst="calc", label="operands")
        # how a referent enters a template is undecided
        diagram.note(
            col="calc",
            lines=["open: does a reference splice its value or its text? (Q1)"],
            kind="open",
        )
        # an unset referent must not turn into text
        diagram.note(
            col="calc",
            lines=["a [None] operand makes the template [None] (s45)"],
            kind="open",
        )
        # back to the slot
        diagram.ret(src="calc", dst="slot")
        # whose postprocessor is the trait
        diagram.call(src="slot", dst="Trait", label="process")
        # unset stays unset, whatever the source
        diagram.note(
            col="Trait",
            lines=["text [none] in any case is [None]; nothing replaces it (s44)"],
            kind="good",
        )
        # which first runs its converters
        diagram.note(col="Trait", lines=["converters, before the schema"])
        # then asks its schema to convert
        diagram.call(src="Trait", dst="Schema", label="coerce")
        # parsing the text once
        diagram.note(col="Schema", lines=["the only parse"], kind="good")
        # without evaluating it
        diagram.note(col="Schema", lines=["no eval (s15, s23)"], kind="good")
        # back to the trait
        diagram.ret(src="Schema", dst="Trait")
        # then applies its own rules
        diagram.note(col="Trait", lines=["normalizers, then validators"])
        # a failure names everything needed to fix it
        diagram.note(
            col="Trait",
            lines=["an error names the [trait], the [source] and the [locator]"],
            kind="good",
        )
        # back to the slot
        diagram.ret(src="Trait", dst="slot")
        # which hands out the value
        diagram.note(col="slot", lines=["the trait's value"])
        # and is done
        diagram.end(col="slot")
        # all done
        return

    def checkProposed(self, diagram: Sequence) -> None:
        """
        The application author asks for every configuration error at once, when ready
        """
        # the author decides when the configuration is complete
        diagram.trigger(
            label="app.pyre_validateConfiguration()", col="Component", sub="when ready (s39)"
        )
        # of the class defaults and of the instance, skipping what the developer marked lazy
        diagram.note(
            col="Component",
            lines=["every slot of the class, then of the instance", "except the [lazy] ones"],
        )
        # every slot is checked
        diagram.call(src="Component", dst="slot", label="check", kind="good")
        # which may need a lazy trait
        diagram.note(col="slot", lines=["a lazy referent is checked if an eager trait needs it"])
        # or may reach a name nobody has set, which goes in the report like any other failure
        diagram.note(
            col="slot",
            lines=["pending: it reaches a [placeholder]", "its [UnresolvedNodeError] is reported"],
            kind="good",
        )
        # through the chain, without keeping what it computes
        diagram.call(src="slot", dst="Trait", label="check")
        # nothing is materialized
        diagram.note(col="Trait", lines=["nothing is materialized or cached"], kind="good")
        # the schema predicts its coercion instead of performing it
        diagram.call(src="Trait", dst="Schema", label="check", kind="good")
        # streams and facilities say whether they would succeed
        diagram.note(
            col="Schema",
            lines=[
                "would coerce succeed? (s39)",
                "streams: readable or writable, not opened",
                "facilities: resolvable, not instantiated",
            ],
            kind="good",
        )
        # what the later steps see is undecided
        diagram.note(
            col="Schema",
            lines=["open: what do normalizers and validators see then?"],
            kind="open",
        )
        # back to the trait
        diagram.ret(src="Schema", dst="Trait")
        # a value is invalid when one of the trait's own steps rejects it
        diagram.note(
            col="Trait",
            lines=["invalid: a converter, coerce, a normalizer or a validator raised"],
        )
        # whose failures are collected rather than raised
        diagram.note(col="Trait", lines=["failures are kept, not raised"], kind="good")
        # back to the slot
        diagram.ret(src="Trait", dst="slot")
        # and to the component
        diagram.ret(src="slot", dst="Component")
        # then the checks the author wrote run too
        diagram.note(col="Component", lines=["then pyre_configured"], kind="good")
        # and everything comes back at once, without raising
        diagram.note(
            col="Component",
            lines=["returns a report of the exceptions, raises nothing"],
            kind="good",
        )
        # what to do about them is the author's call
        diagram.note(
            col="Component",
            lines=["the author decides: stop, log, or ask the user for what is missing"],
            kind="good",
        )
        # side effects wait for the first read
        diagram.note(
            col="Component",
            lines=["cost: streams open and facilities are built at their first read"],
            kind="bad",
        )
        # and is done
        diagram.end(col="Component")
        # all done
        return

    def saveProposed(self, diagram: Sequence) -> None:
        """
        A configuration is written out, and can be read back
        """
        # the writer asks each slot what to record
        diagram.trigger(label="save", col="codec", sub="pfg, yaml writers")
        # what it records is undecided
        diagram.note(col="codec", lines=["open: record the source or the value? (Q4)"], kind="open")
        # the writer asks the slot
        diagram.call(src="codec", dst="slot", label="source · value")
        # back to the writer
        diagram.ret(src="slot", dst="codec")
        # a value is rendered by its schema
        diagram.call(src="codec", dst="Schema", label="string", kind="good")
        # so that it reads back the same
        diagram.note(
            col="Schema",
            lines=["text that coerce reads back (s10-s14, s18-s21)"],
            kind="good",
        )
        # back to the writer
        diagram.ret(src="Schema", dst="codec")
        # which escapes what the template would expand
        diagram.note(col="codec", lines=["escape the braces (s24)"], kind="good")
        # and what the format itself would misread
        diagram.note(
            col="codec", lines=["escape the syntax of the format itself (s22)"], kind="good"
        )
        # and is done
        diagram.end(col="codec")
        # all done
        return

    # the designs: lifelines left to right, scenarios in the order they happen, and the page
    designs = {
        "today": {
            "title": "trait value sequence",
            "cols": [
                "codec",
                "Configurator",
                "Component",
                "NameServer",
                "SlotFactory",
                "calc",
                "slot",
                "Trait",
                "Schema",
            ],
            "scenarios": [boot, load, declare, instantiate, assign, delete, read],
            "label": (
                "Sequence of calls that carry a trait value from each source to the trait: boot,"
                " loading a document, declaring a class, making an instance, assigning from code,"
                " deleting from code, and reading the trait."
            ),
            "intro": """<p>Who calls whom, and when, as a value travels from its source to a trait. One lifeline per collaborator; time runs down. Each scenario starts at the margin with what sets it off, and ends when control returns there. Drawn in the notation of <code>doc/diagrams/design/component-construction.graffle</code>, as a candidate to replace the flow diagram in the <a href="https://claude.ai/artifact/NUhiziGjjNuNxGxZNhPTSJ" target="_blank" rel="noopener">guide</a>. Generated by <code>etc/introspection/trait-value-sequence.py</code>.</p>
    <p class="muted">Lifelines: <b>codec</b> is the command line parser or a document reader; <b>calc</b> is the node algebra the name server is built on (interpolations, expressions, variables, placeholders); <b>slot</b> is the node that ends up holding the value, a calc node itself; <b>Trait</b> owns its <b>SlotFactory</b> and derives from its <b>Schema</b>.</p>
""",
            "key": """<div class="key"><span class="g"><b>green</b>: entry points; the one path that builds a slot once</span><span class="r"><b>red</b>: defects</span><span class="t"><b>dashed</b>: what starts a scenario</span><span class="d"><b>blue</b>: data</span><span>× return</span></div>""",
        },
        "proposed": {
            "title": "trait value strawman",
            "cols": [
                "codec",
                "Configurator",
                "Component",
                "NameServer",
                "calc",
                "slot",
                "Trait",
                "Schema",
            ],
            "scenarios": [
                depositProposed,
                declareProposed,
                instantiateProposed,
                assignProposed,
                readProposed,
                checkProposed,
                saveProposed,
            ],
            "label": (
                "Proposed sequence of calls that carry a trait value from each source to the trait:"
                " depositing, declaring a class, making an instance, assigning from code, reading"
                " the trait, checking the configuration, and saving it."
            ),
            "intro": """<p>The strawman: the same sources and the same lifelines as <a href="https://claude.ai/artifact/7hTb8C5yHnG918GSFJECkb" target="_blank" rel="noopener">the path today</a>, minus <b>SlotFactory</b>. A value is deposited as a node built from its source alone; a trait that arrives later attaches itself to that node as its postprocessor instead of rebuilding it from its value. Nothing is expanded twice, a placeholder is replaced rather than rebuilt from, the text is parsed once, by the schema, and a single check reports every error on demand. Generated by <code>etc/introspection/trait-value-sequence.py --design=proposed</code>.</p>
<p class="muted"><b>Possibly stale:</b> this design was drawn against the code before instances started to follow their classes until they read a trait, and before <code>del</code> and the provenance of following instances were settled; it is kept as it was until the design is revisited.</p>
<p class="muted">Q1-Q4 are open questions in the guide, and Q8 is settled by s51; s-numbers are entries in the ledger. The two calc tests named in the declaration scenario show that the algebra already supports attaching a postprocessor late.</p>
""",
            "key": """<div class="key"><span class="g"><b>green</b>: what changes, or stays because it works</span><span class="o"><b>amber</b>: open question</span><span class="r"><b>red</b>: cost of the design</span><span class="d"><b>blue</b>: data</span><span>× return</span></div>""",
        },
    }

    # the style of the page around the diagram
    style = """<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Source+Sans+3:wght@400;600;700&family=Source+Serif+4:ital,opsz,wght@1,8..60,400;1,8..60,600&display=swap">
<style>
  /* layout: a short reading column, then one tall sequence diagram */
  :root {
    --bg: #fbfbf8; --fg: #23281f; --muted: #6e7466; --life: #cfcfae; --entity: #3c7db5;
    --call: #5f9442; --trigger: #b38b52; --data: #2f5f8f; --defect: #b4442e;
    --font-body: "Source Sans 3", "Segoe UI", system-ui, sans-serif;
    --font-note: "Source Serif 4", Georgia, serif;
  }
  @media (prefers-color-scheme: dark) {
    :root:not([data-theme="light"]) {
      --bg: #161814; --fg: #e4e6de; --muted: #a2a898; --life: #4a4a38; --entity: #7fb3e0;
      --call: #94c776; --trigger: #d7b07a; --data: #8fbbe6; --defect: #ef8a72; color-scheme: dark;
    }
  }
  :root[data-theme="dark"] {
    --bg: #161814; --fg: #e4e6de; --muted: #a2a898; --life: #4a4a38; --entity: #7fb3e0;
    --call: #94c776; --trigger: #d7b07a; --data: #8fbbe6; --defect: #ef8a72; color-scheme: dark;
  }
  body { background: var(--bg); color: var(--fg); font-family: var(--font-body); font-size: 16px; line-height: 1.55; }
  .wrap { max-width: 1260px; margin: 0 auto; padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px)); padding-block: 28px 64px; }
  .prose { max-width: 70ch; }
  h1 { font-family: var(--font-note); font-style: italic; font-weight: 600; font-size: 1.8rem; margin: 0 0 8px; }
  p { margin: 0 0 10px; }
  .muted { color: var(--muted); }
  a { color: var(--entity); }
  .key { display: flex; flex-wrap: wrap; gap: 6px 22px; font-size: 0.88rem; color: var(--muted); margin: 14px 0 10px; }
  .key b { font-weight: 600; }
  .key .g { color: var(--call); } .key .r { color: var(--defect); } .key .t { color: var(--trigger); } .key .d { color: var(--data); }
  .key .o { color: var(--trigger); }
  .fig { overflow-x: auto; }
  svg.seq { display: block; width: 100%; min-width: 1000px; max-width: 1240px; height: auto; }
  svg .life { stroke: var(--life); stroke-width: 1; }
  svg .ent { fill: var(--entity); font-family: var(--font-body); font-size: 14px; }
  svg .rel { stroke: var(--trigger); stroke-width: 1; }
  svg .relhead { fill: var(--trigger); }
  svg .relopen { fill: var(--bg); stroke: var(--trigger); stroke-width: 1; }
  svg .sep { stroke: var(--life); stroke-width: 1; stroke-dasharray: 2 4; }
  svg .trig { fill: var(--call); font-family: var(--font-note); font-style: italic; font-size: 13px; }
  svg .trigsub { fill: var(--muted); font-family: var(--font-note); font-style: italic; font-size: 10.5px; }
  svg .tline { stroke: var(--trigger); stroke-width: 1; stroke-dasharray: 5 3; }
  svg .msg { stroke: var(--muted); stroke-width: 1; }
  svg .msg.bad { stroke: var(--defect); stroke-width: 1.4; }
  svg .msg.good { stroke: var(--call); stroke-width: 1.4; }
  svg .back { stroke: var(--life); stroke-width: 1; }
  svg .hd { fill: var(--muted); } svg .hd.bad { fill: var(--defect); } svg .hd.good { fill: var(--call); }
  svg .hd.back { fill: var(--life); } svg .hd.trig { fill: var(--trigger); }
  svg .call { fill: var(--call); font-family: var(--font-note); font-style: italic; font-size: 12px; }
  svg .call.bad { fill: var(--defect); }
  svg .dot { fill: var(--muted); } svg .dot.entry { fill: var(--call); } svg .dot.bad { fill: var(--defect); }
  svg .note { fill: var(--muted); font-family: var(--font-note); font-style: italic; font-size: 10.5px; }
  svg .note.bad { fill: var(--defect); } svg .note.good { fill: var(--call); }
  svg .note.open { fill: var(--trigger); }
  svg .data { fill: var(--data); font-family: var(--font-body); font-style: normal; font-size: 10.5px; }
  svg .x { stroke: var(--muted); stroke-width: 1.1; fill: none; }
</style>

"""


# main
if __name__ == "__main__":
    # instantiate
    app = TraitValueSequence(name="trait-value-sequence")
    # invoke
    status = app.run()
    # and share the status with the shell
    raise SystemExit(status)


# end of file
