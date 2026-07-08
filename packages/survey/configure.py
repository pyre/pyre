# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# the framework, for its trait introspection
import pyre

# the prompts we drive
from .Input import Input
from .Confirm import Confirm
from .Select import Select


def configure(component, *, traits=None, _seen=None):
    """
    Walk {component}'s properties and facilities, prompting the user to set each one and applying
    the answers as we go, recursing into the component chosen for each facility; {traits} restricts
    the walk to a subset of the properties and suppresses the facilities
    """
    # the component families already on this configuration path, so we can break protocol cycles
    seen = (_seen or frozenset()) | {component.pyre_family()}
    # the properties to configure: the caller's subset, or all of them
    properties = traits if traits is not None else component.pyre_properties()
    # visit each property
    for trait in properties:
        # prompt for a value and apply it
        _configureProperty(component=component, trait=trait)
    # a restricted walk stops at the named properties; otherwise carry on to the facilities
    if traits is None:
        # visit each facility
        for facility in component.pyre_facilities():
            # choose an implementation and recurse into it
            _configureFacility(component=component, facility=facility, seen=seen)
    # hand the configured component back
    return component


def _configureProperty(component, trait):
    """
    Prompt for a single {trait}, coerce and validate the answer, and apply it to {component},
    re-prompting until the value is acceptable
    """
    # the errors {process} raises: a coercion failure, or a constraint violation
    from pyre.schemata.exceptions import SchemaError
    from pyre.constraints.exceptions import ConstraintViolationError

    # seed the prompt from the trait's declared default; we deliberately do not read the live
    # value off the component, since a read triggers validation and, for some trait types, side
    # effects such as opening a file
    prompt = _promptFor(trait=trait, default=trait.default)
    # keep asking until the answer is acceptable
    while True:
        # put the question to the user
        answer = prompt.ask()
        # try to
        try:
            # run the answer through the trait's own coerce-and-validate pipeline — exactly what a
            # later read would do, but against our candidate rather than the live slot
            value = trait.process(value=answer)
        # a value that will not coerce, or that a validator rejects
        except (SchemaError, ConstraintViolationError) as error:
            # report what was wrong and loop to ask again
            print(f"  {error}")
            # back to the top
            continue
        # the value is good, so store it on the component
        setattr(component, trait.name, value)
        # this trait is done
        return


def _promptFor(trait, default):
    """
    Choose and build the prompt best suited to {trait}, seeded with its declared {default}
    """
    # the question to put to the user is the trait's documentation, or its name as a fallback
    message = trait.doc or trait.name
    # a boolean is a yes/no confirmation
    if trait.typename == "bool":
        # seeded with the default truth value
        return Confirm(message=message, default=bool(default))
    # a rendering of the default as text, for the prompts that show one; {None} means no default
    hint = None if default is None else str(default)
    # a trait limited to a set of choices is a menu
    choices = _choices(trait=trait)
    # when there is such a set
    if choices is not None:
        # offer it as a selection, seeded with the default choice
        return Select(message=message, options=choices, default=hint)
    # everything else is free text that {process} will coerce and validate
    return Input(message=message, default=hint)


def _choices(trait):
    """
    The sorted choices a {trait} is limited to by an {isMember}/{Set} validator, or {None} when it
    is not so constrained
    """
    # examine each validator attached to the trait
    for validator in trait.validators:
        # a set constraint carries the allowed values
        choices = getattr(validator, "choices", None)
        # when we find one
        if choices is not None:
            # hand back a stable, ordered list of them
            return sorted(str(choice) for choice in choices)
    # no membership constraint, so no fixed menu
    return None


def _configureFacility(component, facility, seen):
    """
    Prompt the user to choose an implementation for {facility}, apply it, and recurse into the
    chosen component's own traits; {seen} carries the families already on the path, to stop cycles
    """
    # discover the visible implementations of the facility's protocol, each a (uri, name, class)
    implementers = facility.protocol.pyre_locateAllImplementers(namespace=pyre.executive.nameserver)
    # index them by their short name, which is how the user picks and how pyre resolves them
    byName = {name: cls for uri, name, cls in implementers}
    # with nothing to choose from, leave the facility at its default
    if not byName:
        # nothing to do
        return
    # the question is the facility's documentation, or its name as a fallback
    message = facility.doc or facility.name
    # the protocol's preferred implementation names the default choice
    default = facility.protocol.pyre_default()
    # its short name, when there is one
    preferred = default.pyre_familyFragments()[-1] if default is not None else None
    # offer the choice as a menu over the implementation names
    choice = Select(message=message, options=sorted(byName), default=preferred).ask()
    # apply it; pyre coerces the name into an instance attached to the component
    setattr(component, facility.name, choice)
    # reach the freshly built child component
    child = getattr(component, facility.name)
    # recurse into it, unless a component of its family is already on the path
    if child.pyre_family() not in seen:
        # walk the child's own properties and facilities
        configure(child, _seen=seen)
    # all done
    return


# end of file
