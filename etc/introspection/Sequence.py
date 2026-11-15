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
        # nothing else happens on these rows, so the lines may run across the diagram
        x, anchor = self.x[col] - 14, "start"
        # unless the widest of them would run past the right edge
        if x + max(self._span(text=line) for line in lines) > self.width - 8:
            # in which case they all end at the lifeline instead, so the note stays aligned
            x, anchor = self.x[col] + 14, "end"
        # go through the lines
        for line in lines:
            # make room
            self.gap(h=14)
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

    def page(self, title: str, intro: str, key: str, label: str) -> str:
        """
        Render the diagram, with {label} as its accessible description, in a page of its own
        under {title}, after the {intro} and the {key} to its colors
        """
        # the page says how its text is encoded, so the browser reads it right
        return (
            '<meta charset="utf-8">'
            + f"<title>{html.escape(title)}</title>"
            + self.style
            + f'<div class="wrap"><div class="prose"><h1>{html.escape(title)}</h1>'
            + intro
            + "</div>"
            + key
            + '<div class="fig">'
            + self.render(label=label)
            + "</div></div>"
        )

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


# end of file
