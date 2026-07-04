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
            raise ValueError("cannot select from an empty list of options")
        # a real terminal gets the live arrow-key experience; anything else the numbered fallback
        if self.console.interactive():
            return self._askInteractive()
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
            try:
                # draw the first frame, then react to each keypress
                self._render(index=index)
                while True:
                    key = console.readkey()
                    # enter accepts the highlighted option
                    if key.name == keys.ENTER:
                        break
                    # up moves the highlight toward the top, wrapping around
                    if key.name == keys.UP:
                        index = (index - 1) % len(self.options)
                    # down and tab move it toward the bottom, wrapping around
                    elif key.name in (keys.DOWN, keys.TAB):
                        index = (index + 1) % len(self.options)
                    # ctrl-c and a dead input both abandon the selection
                    elif key.name in (keys.INTERRUPT, keys.EOF):
                        raise KeyboardInterrupt
                    # anything else leaves the highlight where it is
                    else:
                        continue
                    # redraw to reflect the moved highlight
                    self._render(index=index)
            finally:
                # collapse the menu to a single summary line and restore the cursor
                self._summarize(index=index)
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
            print(f"  {number}) {option}")
        # keep asking until the reply names a real option
        while True:
            reply = input(f"{self.message} [{fallback}]: ").strip()
            # a blank reply takes the default
            if not reply:
                return fallback
            # a number in range selects by position
            if reply.isdigit() and 1 <= int(reply) <= len(self.options):
                return self.options[int(reply) - 1]
            # the exact text of an option selects it too
            if reply in self.options:
                return reply
            # otherwise explain the accepted answers and ask again
            print(f"  please pick 1-{len(self.options)} or type an option")

    def _render(self, *, index: int) -> None:
        """
        Draw the message and the visible slice of options, highlighting {index}
        """
        console = self.console
        # rewind over whatever frame is currently on screen
        console.rewind(lines=self._drawn)
        # the slice of options to show, and the header above them
        start, end = self._window(index=index)
        rows = [f"{self.paint(self.message, self.theme.message)}:"]
        # each visible option, the highlighted one marked and painted with the selection color
        for position in range(start, end):
            if position == index:
                rows.append(
                    self.paint(f"❯ {self.options[position]}", self.theme.selected)
                )
            else:
                rows.append(f"  {self.options[position]}")
        # commit the frame and remember how tall it was
        console.write("\n".join(rows) + "\n")
        console.flush()
        self._drawn = len(rows)

    def _summarize(self, *, index: int) -> None:
        """
        Replace the whole menu with a single line naming the chosen option
        """
        console = self.console
        # clear the live frame, then leave the decision on the record, the choice in color
        console.rewind(lines=self._drawn)
        label = self.paint(self.message, self.theme.message)
        value = self.paint(self.options[index], self.theme.selected)
        console.write(f"{label}: {value}\n")
        console.flush()
        self._drawn = 0

    def _window(self, *, index: int):
        """
        Compute the slice of options to show so that {index} stays visible, roughly centered
        """
        total = len(self.options)
        # never try to show more rows than there are options
        size = min(self.pagesize, total)
        # center the window on the highlight, then slide it back inside the list
        start = index - size // 2
        if start < 0:
            start = 0
        if start + size > total:
            start = total - size
        return start, start + size

    def _defaultIndex(self) -> int:
        """
        Locate the starting highlight from the default value, or the top of the list
        """
        # honor the default only when it is actually one of the options
        if self.default is not None and self.default in self.options:
            return self.options.index(self.default)
        return 0


# end of file
