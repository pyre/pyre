# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
import re

# framework
import pyre


# the declarative description of a package category request
class Requirement:
    """
    A requirement on a package category: the category tag, the flavor selectors the
    selection must honor, and the version constraints it must satisfy

    Requirements are the vocabulary consumers use to ask for packages, and the vocabulary
    recipes use to constrain their dependencies. The text form reads like familiar package
    manager syntax: {hdf5}, {hdf5>=1.12,<2}, {hdf5[openmpi]}, {hdf5[parallel]>=1.14},
    {hdf5[!serial]}. Bracketed selectors name a flavor or a flavor class published by the
    category recipes; a leading {!} excludes instead. Version clauses are comparisons
    joined by commas, forming a conjunction
    """

    # exceptions
    from .exceptions import RequirementSyntaxError

    # constants
    # versions we cannot compare against anything
    unknown = "unknown"

    # the overall shape: a category tag, an optional bracketed selector list, and
    # whatever remains as the version clause section
    _grammar = re.compile(
        r"(?P<category>[A-Za-z][\w-]*)" r"(?:\[(?P<selectors>[^\]]*)\])?" r"(?P<clauses>.*)"
    )

    # a single version clause: a comparison operator followed by a version tag
    _clause = re.compile(r"(?P<operator>==|!=|>=|<=|>|<)\s*(?P<version>[\w.+-]+)")

    # a version component: an optional numeric part with whatever trails it
    _component = re.compile(r"(?P<number>\d+)?(?P<tail>.*)")

    # the map from comparison operators to constraint foundries
    _operators = {
        "==": lambda value: pyre.constraints.isEqual(value=value),
        "!=": lambda value: pyre.constraints.isNot(pyre.constraints.isEqual(value=value)),
        ">=": lambda value: pyre.constraints.isGreaterEqual(value=value),
        "<=": lambda value: pyre.constraints.isLessEqual(value=value),
        ">": lambda value: pyre.constraints.isGreater(value=value),
        "<": lambda value: pyre.constraints.isLess(value=value),
    }

    # factories
    @classmethod
    def parse(cls, spec):
        """
        Convert the text form in {spec} into a requirement
        """
        # requirements that are already structured pass through untouched
        if isinstance(spec, cls):
            # so callers can mix text and objects freely
            return spec
        # clean up the raw text
        text = spec.strip()
        # match the overall shape
        match = cls._grammar.fullmatch(text)
        # anything that doesn't even have a recognizable category tag
        if match is None:
            # is a syntax error
            raise cls.RequirementSyntaxError(spec=spec, problem="no recognizable category")
        # extract the category
        category = match.group("category")
        # the selector section, when present
        selectors = []
        # and the exclusions harvested from it
        exclusions = []
        # get the bracketed text
        bracketed = match.group("selectors")
        # if the brackets are there
        if bracketed is not None:
            # go through the comma separated entries
            for entry in bracketed.split(","):
                # clean it up
                entry = entry.strip()
                # blank entries indicate a typo
                if not entry:
                    # so complain
                    raise cls.RequirementSyntaxError(spec=spec, problem="empty selector")
                # a leading {!} flips the polarity
                if entry.startswith("!"):
                    # the rest of the token is the excluded name
                    name = entry[1:].strip()
                    # which must be non-trivial
                    if not name:
                        # or it's another typo
                        raise cls.RequirementSyntaxError(spec=spec, problem="empty exclusion")
                    # record the exclusion
                    exclusions.append(name)
                # plain tokens are selections
                else:
                    # record the selector
                    selectors.append(entry)
        # the version clause section
        clauses = []
        # get the remaining text
        trailing = match.group("clauses").strip()
        # if there is any
        if trailing:
            # go through the comma separated clauses
            for piece in trailing.split(","):
                # clean it up
                piece = piece.strip()
                # match the clause shape
                parsed = cls._clause.fullmatch(piece)
                # anything else is unrecognizable
                if parsed is None:
                    # so complain
                    raise cls.RequirementSyntaxError(
                        spec=spec, problem=f"bad version clause '{piece}'"
                    )
                # record the (operator, version) pair
                clauses.append((parsed.group("operator"), parsed.group("version")))
        # assemble the requirement
        return cls(
            category=category,
            selectors=tuple(selectors),
            exclusions=tuple(exclusions),
            clauses=tuple(clauses),
        )

    @classmethod
    def key(cls, version):
        """
        Convert a {version} tag into a componentwise comparison key

        Components are the dot separated pieces of the tag; each contributes its numeric
        part and whatever trails it, so that {1.9} sorts below {1.12}, and {1.14.6} sorts
        below {1.14.6b}. Purely alphabetic components sort below any numbered one, placing
        tags like {rc1} ahead of proper releases
        """
        # the components of the key
        components = []
        # go through the dot separated pieces
        for piece in version.split("."):
            # split off the numeric part
            match = cls._component.fullmatch(piece)
            # convert it, pushing alphabetic pieces below all numbered ones
            number = int(match.group("number")) if match.group("number") else -1
            # add the component
            components.append((number, match.group("tail")))
        # freeze the key
        return tuple(components)

    # meta-methods
    def __init__(self, *, category, selectors=(), exclusions=(), clauses=()):
        """
        Describe a requirement on the {category} selection
        """
        # the category this requirement constrains
        self.category = category
        # the flavor names or flavor classes the selection must answer to
        self.selectors = tuple(selectors)
        # the flavor names or flavor classes the selection must avoid
        self.exclusions = tuple(exclusions)
        # the (operator, version) pairs of the version conjunction
        self.clauses = tuple(clauses)
        # realize the version constraint by folding the clauses into a conjunction
        self.constraint = (
            pyre.constraints.isAll(
                # each clause contributes its operator applied to the parsed version
                *(self._operators[operator](self.key(version)) for operator, version in clauses)
            )
            # trivial requirements carry no constraint
            if clauses
            else None
        )
        # all done
        return

    # interface
    def admits(self, flavor, tags=()):
        """
        Check whether a selection with the given {flavor} and flavor class {tags} honors
        my selectors
        """
        # the pool of names the selection answers to
        names = {flavor, *tags}
        # every selector must be answered
        if not all(selector in names for selector in self.selectors):
            # otherwise the selection is inadmissible
            return False
        # and no exclusion may be
        if any(exclusion in names for exclusion in self.exclusions):
            # or the selection is explicitly ruled out
            return False
        # the selection passes
        return True

    def accepts(self, version):
        """
        Check whether the given {version} tag satisfies my version conjunction
        """
        # requirements without version clauses accept everything
        if self.constraint is None:
            # trivially
            return True
        # a version we can't compare cannot be proven to satisfy the clauses
        if not version or version == self.unknown:
            # so it is rejected
            return False
        # attempt to
        try:
            # push the comparison key through the conjunction
            self.constraint(self.key(version))
        # if it violates any clause
        except self.constraint.ConstraintViolationError:
            # the version is rejected
            return False
        # otherwise it is acceptable
        return True

    # debugging support
    def __str__(self):
        # rebuild the selector section, exclusions marked with their polarity
        selectors = ",".join((*self.selectors, *(f"!{name}" for name in self.exclusions)))
        # wrap it in brackets when non-trivial
        selectors = f"[{selectors}]" if selectors else ""
        # rebuild the version section
        clauses = ",".join(f"{operator}{version}" for operator, version in self.clauses)
        # and assemble the normalized form
        return f"{self.category}{selectors}{clauses}"

    # narrow the footprint
    __slots__ = (
        "category",
        "selectors",
        "exclusions",
        "clauses",
        "constraint",
    )


# end of file
