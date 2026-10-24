# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
import html


# a sequence diagram, in the notation of doc/diagrams/design/component-construction.graffle
class Sequence:
    """
    A sequence diagram drawn as inline SVG: one lifeline per collaborator, time running down,
    scenarios started from the margin, calls landing on named entry points, returns as crosses
    """

    # interface
    def trigger(self, label: str, col: str, sub: str | None = None) -> None:
        """
        Start a scenario: a dashed arrow from the margin, named {label}, lands on {col}
        """
        # remember where the scenario enters, so it can be closed there
        self._entry = col
        # find the lifeline
        x = self.x[col]
        # name what starts the scenario
        self._text(x=14, y=self.y - 4, text=label, cls="trig")
        # if there is more to say about it
        if sub:
            # say it underneath
            self._text(x=14, y=self.y + 12, text=sub, cls="trigsub")
        # draw the arrow from the margin
        self.marks.append(
            f'<line class="tline" x1="12" y1="{self.y}" x2="{x - 7}" y2="{self.y}"'
            f' marker-end="url(#ta)"/>'
        )
        # and the entry point it lands on
        self.marks.append(f'<circle class="dot entry" cx="{x}" cy="{self.y}" r="5"/>')
        # all done
        return

    def call(self, src: str, dst: str, label: str, kind: str = "") -> None:
        """
        Draw a message from {src} to {dst}, landing on the entry point {label}; {kind} is
        empty, "bad" for a defect, or "good" for the path to keep
        """
        # make room
        self.gap(h=26)
        # find the two lifelines
        xs, xd = self.x[src], self.x[dst]
        # figure out which way the message goes
        direction = 1 if xd > xs else -1
        # pick the arrowhead that matches the kind
        head = {"bad": "mb", "good": "mg"}.get(kind, "ma")
        # mark where the message leaves
        self.marks.append(f'<circle class="dot" cx="{xs}" cy="{self.y}" r="2.4"/>')
        # draw the message
        self.marks.append(
            f'<line class="msg {kind}" x1="{xs}" y1="{self.y}" x2="{xd - direction * 7}"'
            f' y2="{self.y}" marker-end="url(#{head})"/>'
        )
        # name the entry point above the callee
        self._text(x=xd, y=self.y - 9, text=label, cls=f"call {kind}", anchor="middle")
        # and mark it
        self.marks.append(
            f'<circle class="dot {"bad" if kind == "bad" else "entry"}" cx="{xd}" cy="{self.y}"'
            f' r="4.5"/>'
        )
        # all done
        return

    def note(self, col: str, lines: list[str], kind: str = "") -> None:
        """
        Write the steps {col} takes under its entry point; words in [brackets] are data
        """
        # a note that follows another one on the same lifeline
        if self._lastNote == (col, self.y):
            # gets set apart from it
            self.gap(h=5)
        # go through the lines
        for line in lines:
            # make room
            self.gap(h=14)
            # nothing else happens on this row, so the line may run across the diagram
            x, anchor = self.x[col] - 14, "start"
            # unless it would run past the right edge
            if x + self._span(text=line) > self.width - 8:
                # in which case it ends at the lifeline instead
                x, anchor = self.x[col] + 14, "end"
            # write it
            self._rich(x=x, y=self.y, text=line, cls=f"note {kind}", anchor=anchor)
        # remember where this note ended
        self._lastNote = (col, self.y)
        # all done
        return

    def ret(self, src: str, dst: str) -> None:
        """
        Return from {src} to {dst}: a cross on the callee, a faint arrow back to the caller
        """
        # make room
        self.gap(h=16)
        # find the two lifelines
        xs, xd = self.x[src], self.x[dst]
        # figure out which way the return goes
        direction = 1 if xd > xs else -1
        # cross out the callee
        self._cross(x=xs)
        # and point back to the caller
        self.marks.append(
            f'<line class="back" x1="{xs - direction * 5}" y1="{self.y}"'
            f' x2="{xd - direction * 6}" y2="{self.y}" marker-end="url(#rb)"/>'
        )
        # all done
        return

    def unwind(self, *cols: str) -> None:
        """
        Return along a chain of calls, from the innermost callee in {cols} outwards
        """
        # go through consecutive pairs
        for src, dst in zip(cols, cols[1:]):
            # and return from each callee to its caller
            self.ret(src=src, dst=dst)
        # all done
        return

    def end(self, col: str) -> None:
        """
        Mark the end of the activity of {col} with nobody to return to
        """
        # make room
        self.gap(h=14)
        # and cross it out
        self._cross(x=self.x[col])
        # if this is where the scenario entered
        if col == self._entry:
            # it is done
            self._entry = None
        # all done
        return

    def section(self) -> None:
        """
        Separate one scenario from the next
        """
        # finish the one before
        self._close()
        # make room
        self.gap(h=18)
        # draw a faint rule across the diagram
        self.marks.append(
            f'<line class="sep" x1="8" y1="{self.y}" x2="{self.width - 8}" y2="{self.y}"/>'
        )
        # and leave room under it
        self.gap(h=22)
        # all done
        return

    def relate(self, src: str, dst: str, kind: str) -> None:
        """
        Draw a relation between the heads of {src} and {dst}: "derives", with an open triangle
        at {dst}, or "owns", with a diamond at {src}
        """
        # the heads sit on this line
        y = self.top - 22
        # find the two lifelines
        xs, xd = self.x[src], self.x[dst]
        # figure out which way the relation goes
        direction = 1 if xd > xs else -1
        # leave room for the names of the two heads
        x1, x2 = xs + direction * self._half(src), xd - direction * self._half(dst)
        # draw the line
        self.heads.append(f'<line class="rel" x1="{x1}" y1="{y}" x2="{x2}" y2="{y}"/>')
        # a derivation points to the base with an open triangle
        if kind == "derives":
            # at the end of the line
            self.heads.append(f'<path class="relopen" d="M{x2},{y} l{-direction * 9},-5 v10 z"/>')
        # ownership puts a diamond at the owner
        else:
            # at the start of the line
            self.heads.append(
                f'<path class="relhead" d="M{x1},{y} l{direction * 6},-4 l{direction * 6},4'
                f' l{-direction * 6},4 z"/>'
            )
        # all done
        return

    def gap(self, h: int) -> None:
        """
        Move down by {h}
        """
        # easy enough
        self.y += h
        # all done
        return

    def render(self, label: str) -> str:
        """
        Build the SVG, with {label} as its accessible description
        """
        # finish the last scenario
        self._close()
        # leave room at the bottom
        self.gap(h=30)
        # the height is where the cursor stopped
        height = self.y
        # draw the lifelines and their names
        lifelines = []
        # go through the collaborators
        for name, x in self.x.items():
            # draw the lifeline
            lifelines.append(
                f'<line class="life" x1="{x}" y1="{self.top - 8}" x2="{x}" y2="{height - 10}"/>'
            )
            # and name it
            lifelines.append(
                f'<text class="ent" x="{x}" y="{self.top - 18}" text-anchor="middle">'
                f"{html.escape(name)}</text>"
            )
        # put it all together
        return (
            f'<svg class="seq" viewBox="0 0 {self.width} {height}" role="img"'
            f' aria-label="{html.escape(label, quote=True)}">'
            + self._defs
            + "".join(lifelines)
            + "".join(self.heads)
            + "".join(self.marks)
            + "</svg>"
        )

    # metamethods
    def __init__(self, cols: list[str], x0: int = 190, dx: int = 112, top: int = 70, **kwds):
        # chain up
        super().__init__(**kwds)
        # place the lifelines
        self.x = {name: x0 + i * dx for i, name in enumerate(cols)}
        # leave room to the right of the last one for its notes
        self.width = x0 + (len(cols) - 1) * dx + 140
        # remember where the heads sit
        self.top = top
        # start the cursor under the heads
        self.y = top + 40
        # make a pile for the marks in the diagram body
        self.marks = []
        # and one for the relations among the heads
        self.heads = []
        # nothing has been noted yet
        self._lastNote = None
        # and no scenario has started
        self._entry = None
        # all done
        return

    # implementation details
    def _close(self) -> None:
        """
        Mark the return of the lifeline where the current scenario entered, unless it is marked
        already
        """
        # if a scenario is still open
        if self._entry is not None:
            # its entry point returns to whoever started it
            self.end(col=self._entry)
        # all done
        return

    def _text(self, x: float, y: float, text: str, cls: str, anchor: str = "start") -> None:
        """
        Write {text} at ({x}, {y})
        """
        # escape and place it
        self.marks.append(
            f'<text class="{cls}" x="{x}" y="{y}" text-anchor="{anchor}">'
            f"{html.escape(text)}</text>"
        )
        # all done
        return

    def _rich(self, x: float, y: float, text: str, cls: str, anchor: str = "start") -> None:
        """
        Write {text} at ({x}, {y}), drawing the words in [brackets] as data
        """
        # make a pile for the pieces
        spans = []
        # split at the brackets; the odd pieces are data
        for i, chunk in enumerate(text.replace("]", "[").split("[")):
            # skip the empty pieces left by adjacent brackets
            if not chunk:
                # on to the next
                continue
            # style each piece by what it is
            spans.append(f'<tspan class="{"data" if i % 2 else cls}">{html.escape(chunk)}</tspan>')
        # place the line
        self.marks.append(f'<text x="{x}" y="{y}" text-anchor="{anchor}">{"".join(spans)}</text>')
        # all done
        return

    def _cross(self, x: float) -> None:
        """
        Draw a cross at {x} on the current line
        """
        # two short strokes
        self.marks.append(
            f'<path class="x" d="M{x - 4},{self.y - 4} L{x + 4},{self.y + 4}'
            f' M{x - 4},{self.y + 4} L{x + 4},{self.y - 4}"/>'
        )
        # all done
        return

    def _span(self, text: str) -> float:
        """
        Estimate the width of a line of {text} at the size of the notes
        """
        # about five and a half pixels per character, ignoring the brackets that mark data
        return 5.5 * len(text.replace("[", "").replace("]", ""))

    def _half(self, name: str) -> float:
        """
        Estimate half the width of the head named {name}, plus a margin
        """
        # about four pixels per character at the size of the heads, and room to breathe
        return 4.0 * len(name) + 8

    # the arrowheads
    _defs = (
        "<defs>"
        + "".join(
            f'<marker id="{key}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6"'
            f' markerHeight="6" orient="auto-start-reverse">'
            f'<path d="M0,0 L10,5 L0,10 z" class="hd {cls}"/></marker>'
            for key, cls in (
                ("ma", ""),
                ("mb", "bad"),
                ("mg", "good"),
                ("rb", "back"),
                ("ta", "trig"),
            )
        )
        + "</defs>"
    )


# end of file
