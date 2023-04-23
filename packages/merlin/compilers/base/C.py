# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# support
import merlin


# mixin that adds some behavior that is specific to C compilers
class C(merlin.component):
    """
    Behavior specific to C compilers
    """

    def dialect(self, std):
        """
        Specify the language dialect
        """
        # recognize "ansi" as a special case
        if std == "ansi":
            # that has its own flag
            yield "-ansi"
            # all done
            return
        # otherwise, chain up
        yield from super().dialect(std)
        # all done
        return


# end of file
