# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2025 all rights reserved


# support
import pyre


# build a progress bar
class ProgressBar(pyre.component, family="pyre.widgets.progress"):
    """
    Build and render a  progress bar
    """

    # user configurable state
    # set the glyph
    glyph = pyre.properties.str()
    glyph.default = "\u2500"
    glyph.doc = "the bar graphic"

    # and the display width
    width = pyre.properties.int()
    width.default = (2 * pyre.executive.terminal.width // 3) or 60
    width.doc = "the bar width, in characters"

    # pick some colors
    reset = pyre.properties.str()
    reset.default = pyre.executive.terminal.ansi["normal"]
    reset.doc = "the escape sequence that reset color to its normal value"

    color = pyre.properties.str()
    color.default = pyre.executive.terminal.misc["amber"]
    color.doc = "the color to use when rendering the completed work"

    background = pyre.properties.str()
    background.default = pyre.executive.terminal.gray["gray50"]
    background.doc = "the color to use when rendering the work that's not yet done"

    # rendering control
    throttle = pyre.properties.dimensional()
    throttle.default = "100 * ms"
    throttle.doc = "the bar refresh period"

    resolution = pyre.properties.float()
    resolution.default = 0.01
    resolution.doc = "minimum change before rerendering the bar"

    # interface
    def update(self, p):
        """
        Update the progress bar with a new value
        """
        # if this is the first update
        if p <= 0:
            # store the completed work fraction
            self.p = p
            # draw the bar
            bar = self.paint()
            # and render it
            print(bar, end="")
            # reset the timer
            self.timer.reset()
            # and start it
            self.timer.start()
            # all done
            return

        # if this is the final update
        if p >= 1:
            # store the completed work fraction
            self.p = 1.0
            # draw the bar
            bar = self.paint()
            # and render it
            print(bar)
            # stop the timer
            self.timer.stop()
            # and reset it
            self.timer.reset()
            # all done
            return

        # otherwise, compute the delta since the last rendering
        δ = p - self.p
        # if it's not enough
        if δ < self.resolution:
            # bail
            return
        # compute the amount of time since the last update
        δt = self.timer.read()
        # if it is less than the {throttle}
        if δt < self.throttle.value:
            # bail
            return
        # if we get this far, store the completed work fraction
        self.p = p
        # draw the bar
        bar = self.paint()
        # render it
        print(bar, end="")
        # reset the timer
        self.timer.reset()
        # and start it again
        self.timer.start()
        # all done
        return

    # metamethods
    def __init__(self, name: str, p: float = 0, **kwds):
        # chain up
        super().__init__(name, **kwds)
        # initialize the completion fraction
        self.p = 0
        # and make a timer
        self.timer = pyre.timers.wall(name=name)
        # all done
        return

    # implementation details
    def paint(self):
        """
        Paint a progress bar at
        """
        # unpack my state
        p = self.p
        color = self.color
        glyph = self.glyph
        reset = self.reset
        background = self.background

        # compute the bar size
        total = self.width
        # the portion that is done
        done = int(p * total)
        # the missing part
        todo = total - done
        # build the bar
        bar = f"{color}{glyph*done}{background}{glyph*todo}{reset}"
        # and the percentage
        mark = f"{color}{100*p:3.0f}{reset}%"
        # put it all together
        return f"\r{bar} {mark}"


# end of file
