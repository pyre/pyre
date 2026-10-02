# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
import os
import re

# for my metaclass
import pyre


# the singleton that owns the global state
class Chronicler(metaclass=pyre.patterns.singleton):
    """
    The manager of the journal global state
    """

    # public data
    notes = None
    device = None
    decor = 1
    detail = 1
    margin = " " * 2

    # interface
    @staticmethod
    def level(variable: str) -> int | None:
        """
        Read a decoration or detail level from the environment {variable}

        As in the c++ journal, the setting is the integer the value starts with, and a value that
        is missing, does not start with an integer, or is zero leaves the level unset
        """
        # read the setting
        setting = os.environ.get(variable)
        # if it's not there
        if setting is None:
            # there is no level
            return None
        # look for the integer the setting starts with
        match = re.match(r"\s*[+-]?\d+", setting)
        # if there isn't one
        if match is None:
            # there is no level
            return None
        # convert it
        level = int(match.group())
        # and hand it off, unless it is zero, which the environment cannot request
        return level if level != 0 else None

    @staticmethod
    def nameset(text: str) -> set:
        """
        Split the comma separated channel names in {text} into a set, skipping the empty ones
        """
        # split, and keep the non empty names
        return {name for name in text.split(",") if name}

    def quiet(self):
        """
        Suppress all output
        """
        # get the trash can
        from .Trash import Trash

        # make one and install it as the default device
        self.device = Trash()
        # all done
        return

    # metamethods
    def __init__(
        self,
        decor=None,
        detail=None,
        device=device,
        margin=margin,
        notes=notes,
        **kwds,
    ):
        """
        Set up the global state, taking the levels the caller leaves out from the environment
        """
        # chain up
        super().__init__(**kwds)
        # the default decor: what the caller asked for, or what the environment says
        decor = decor if decor is not None else self.level(variable="JOURNAL_DECOR")
        # and if neither expressed an opinion, the class default
        self.decor = decor if decor is not None else type(self).decor
        # the default detail: what the caller asked for, or what the environment says
        detail = detail if detail is not None else self.level(variable="JOURNAL_DETAIL")
        # and if neither expressed an opinion, the class default
        self.detail = detail if detail is not None else type(self).detail
        # the default margin
        self.margin = margin

        # the global metadata; can't be empty
        self.notes = (
            notes
            if notes is not None
            else {
                "application": "journal",  # this key is required; applications should override
            }
        )

        # if whoever initialized the journal did not express an opinion regarding the device
        if device is None:
            # the two devices we might install
            from .Console import Console
            from .BootDevice import BootDevice

            # once the framework is up, {pyre.executive} is set and a real console is safe to
            # build; while pyre is still booting it is None, and a console would reach for
            # framework facilities (the terminal) that don't exist yet, so pick a boot device
            # that merely collects entries until pyre hands us a real one
            deviceFactory = Console if pyre.executive else BootDevice
            # build the chosen device
            device = deviceFactory()
        # attach it
        self.device = device

        # all done
        return


# end of file
