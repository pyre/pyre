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


def configure(component, *, traits=None):
    """
    Walk {component}'s properties and prompt the user to set each one, applying the answers to the
    component as we go; {traits} restricts the walk to a subset of the properties
    """
    # the properties to configure: the caller's subset, or all of them
    properties = traits if traits is not None else component.pyre_properties()
    # visit each one
    for trait in properties:
        # prompt for a value and apply it
        _configureTrait(component=component, trait=trait)
    # hand the configured component back
    return component


def _configureTrait(component, trait):
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


# end of file
