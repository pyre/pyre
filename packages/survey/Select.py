# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# the base prompt and the key names
from .Prompt import Prompt
from . import keys


class Select(Prompt):
    """
    Offer a list of options and let the user settle on exactly one; arrow keys on a real
    terminal, a numbered fallback when the input is redirected
    """

    def __init__(self, *, options, default=None, pagesize=7, **kwds):
        # chain up
        super().__init__(**kwds)
        # the choices, kept in the order the caller gave them
        self.options = list(options)
        # the choice to start on, given as one of the option values
        self.default = default
        # the most options to show at once before the list scrolls
        self.pagesize = pagesize
        # how many terminal rows the last drawn frame occupied
        self._drawn = 0

    def ask(self) -> str:
        """
        Return the option the user settles on
        """
        # an empty list has nothing to choose from
        if not self.options:
            # so refuse rather than draw an empty menu
            raise ValueError("cannot select from an empty list of options")
        # a real terminal gets the live arrow-key experience
        if self.console.interactive():
            # so drive the interactive loop
            return self._askInteractive()
        # anything else falls back to a numbered prompt
        return self._askNumbered()

    def _askInteractive(self) -> str:
        """
        Drive the arrow-key selection loop against a raw terminal
        """
        # start on the default, or the top of the list
        index = self._defaultIndex()
        # take the terminal into raw mode for the duration of the loop
        with self.console as console:
            # keep the cursor out of the way while frames are redrawn
            console.hideCursor()
            # make sure the menu is torn down and the cursor restored no matter how we leave
            try:
                # draw the first frame
                self._render(index=index)
                # then react to each keypress until the user commits
                while True:
                    # read the next keypress
                    key = console.readkey()
                    # enter accepts the highlighted option
                    if key.name == keys.ENTER:
                        # so leave the loop with the current highlight
                        break
                    # up moves the highlight toward the top, wrapping around
                    if key.name == keys.UP:
                        # step back one, rolling past the top to the bottom
                        index = (index - 1) % len(self.options)
                    # down and tab move it toward the bottom, wrapping around
                    elif key.name in (keys.DOWN, keys.TAB):
                        # step forward one, rolling past the bottom to the top
                        index = (index + 1) % len(self.options)
                    # ctrl-c and a dead input both abandon the selection
                    elif key.name in (keys.INTERRUPT, keys.EOF):
                        # so bail out the way the shell expects
                        raise KeyboardInterrupt
                    # anything else leaves the highlight where it is
                    else:
                        # so wait for the next key without redrawing
                        continue
                    # redraw to reflect the moved highlight
                    self._render(index=index)
            finally:
                # collapse the menu to a single summary line
                self._summarize(index=index)
                # and give the cursor back
                console.showCursor()
        # hand back the chosen option
        return self.options[index]

    def _askNumbered(self) -> str:
        """
        Offer a numbered list and read a choice, for when there is no live terminal
        """
        # settle the default up front so it can be shown and returned on a blank reply
        fallback = self.options[self._defaultIndex()]
        # lay out the choices with one-based numbers
        for number, option in enumerate(self.options, start=1):
            # one line per choice
            print(f"  {number}) {option}")
        # keep asking until the reply names a real option
        while True:
            # read a line naming a choice
            reply = input(f"{self.message} [{fallback}]: ").strip()
            # a blank reply takes the default
            if not reply:
                # so hand back the fallback
                return fallback
            # a number in range selects by position
            if reply.isdigit() and 1 <= int(reply) <= len(self.options):
                # so return the option at that one-based position
                return self.options[int(reply) - 1]
            # the exact text of an option selects it too
            if reply in self.options:
                # so return it directly
                return reply
            # otherwise explain the accepted answers and ask again
            print(f"  please pick 1-{len(self.options)} or type an option")

    def _render(self, *, index: int) -> None:
        """
        Draw the message and the visible slice of options, highlighting {index}
        """
        # the terminal we draw on
        console = self.console
        # rewind over whatever frame is currently on screen
        console.rewind(lines=self._drawn)
        # the slice of options to show around the highlight
        start, end = self._window(index=index)
        # open the frame with the colored message
        rows = [f"{self.paint(self.message, self.theme.message)}:"]
        # add each visible option
        for position in range(start, end):
            # the highlighted one is marked and painted with the selection color
            if position == index:
                # a pointer plus the option, in the selection color
                rows.append(
                    self.paint(f"❯ {self.options[position]}", self.theme.selected)
                )
            # the rest sit quietly, indented to line up
            else:
                # two spaces where the pointer would be
                rows.append(f"  {self.options[position]}")
        # commit the frame
        console.write("\n".join(rows) + "\n")
        # make it visible at once
        console.flush()
        # remember how tall it was so the next redraw can rewind it
        self._drawn = len(rows)

    def _summarize(self, *, index: int) -> None:
        """
        Replace the whole menu with a single line naming the chosen option
        """
        # the terminal we draw on
        console = self.console
        # clear the live frame
        console.rewind(lines=self._drawn)
        # the colored message
        label = self.paint(self.message, self.theme.message)
        # and the chosen option, painted like a selection
        value = self.paint(self.options[index], self.theme.selected)
        # leave the decision on the record
        console.write(f"{label}: {value}\n")
        # make it visible at once
        console.flush()
        # there is no live frame left to rewind
        self._drawn = 0

    def _window(self, *, index: int):
        """
        Compute the slice of options to show so that {index} stays visible, roughly centered
        """
        # how many options there are in all
        total = len(self.options)
        # never try to show more rows than there are options
        size = min(self.pagesize, total)
        # center the window on the highlight
        start = index - size // 2
        # but do not run off the top
        if start < 0:
            # pin the window to the first option
            start = 0
        # nor off the bottom
        if start + size > total:
            # pin the window to the last full page
            start = total - size
        # hand back the visible half-open range
        return start, start + size

    def _defaultIndex(self) -> int:
        """
        Locate the starting highlight from the default value, or the top of the list
        """
        # honor the default only when it is actually one of the options
        if self.default is not None and self.default in self.options:
            # so start on the default's position
            return self.options.index(self.default)
        # otherwise start at the top
        return 0


# end of file
