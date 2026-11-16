#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# the framework
import pyre

# the drawing
from Sequence import Sequence


# the app
class LiaisonRace(pyre.application):
    """
    Draw the race between a synchronous recruitment and the liaison's report handler, as it was
    captured in a qed server, as a page with one sequence diagram; a historical record of a
    defect, not a description of how recruitment works
    """

    # user configurable state
    out = pyre.properties.ostream(default="liaison-race-historical.html")
    out.doc = "the page to write"

    # obligations
    @pyre.export
    def main(self, *args, **kwds) -> int:
        """
        Build the page and write it out
        """
        # make the diagram
        diagram = Sequence(cols=self.cols, dx=128)
        # relate the heads: a team owns its recruiter
        diagram.relate(src="Builders", dst="Forkserver", kind="owns")
        # go through the scenarios, in the order they happen
        for index, scenario in enumerate(self.scenarios):
            # set each one apart from the one before
            if index:
                # with a faint rule
                diagram.section()
            # and draw it
            scenario(self, diagram=diagram)
        # render the diagram in its page
        page = diagram.page(title=self.title, intro=self.intro, key=self.key, label=self.label)
        # and write it out
        self.out.write(page)
        # all done
        return 0

    # the scenarios
    def exit(self, diagram: Sequence) -> None:
        """
        A member leaves, and the agency reports it before the next pass of the event loop
        """
        # a member is gone
        diagram.trigger(label="SIGCHLD", col="StaffingAgency", sub="member 83245 is gone")
        # the agency collects it
        diagram.note(col="StaffingAgency", lines=["[harvest]: waitpid collects 83245"])
        # and reports it
        diagram.call(src="StaffingAgency", dst="Liaison", label="[Exited] 83245")
        # where it waits
        diagram.note(
            col="Liaison",
            lines=[
                "the report waits in the control channel, fd 8, until somebody reads it",
                "the server's event loop has not looked yet",
            ],
        )
        # all done
        return

    def race(self, diagram: Sequence) -> None:
        """
        One pass of the server's event loop: a recruitment drains the control channel ahead of
        the report handler, which then blocks
        """
        # the pass starts
        diagram.trigger(label="select", col="dispatcher", sub="pass 127, t = 0 ms")
        # with three channels ready
        diagram.note(
            col="dispatcher",
            lines=[
                "ready: fd 79 (an HTTP connection), fd 47 (a builder's journal), fd 8 (control)",
                "the pass serves them in this order, each on the readiness reported here",
            ],
        )
        # the first is a request
        diagram.call(src="dispatcher", dst="web", label="fd 79: request")
        # that needs builders
        diagram.call(src="web", dst="Builders", label="grow")
        # sixteen of them
        diagram.note(col="Builders", lines=["sixteen vacancies, filled one at a time"])
        # the first one
        diagram.call(src="Builders", dst="Forkserver", label="deploy")
        # through the liaison
        diagram.call(src="Forkserver", dst="Liaison", label="recruit", kind="bad")
        # which asks the agency
        diagram.call(src="Liaison", dst="StaffingAgency", label="[Recruit]")
        # and reads the control channel until the answer is in
        diagram.note(
            col="Liaison",
            lines=[
                "t = 14.6 ms: [hear] reads fd 8 and finds [Exited] 83245, not the answer",
                "delivers it: the exit is filed, its subscribers are told",
                "the message that made fd 8 ready in this pass is gone",
            ],
            kind="bad",
        )
        # the agency forks the member
        diagram.call(src="StaffingAgency", dst="member", label="enlist: fork")
        # and answers
        diagram.call(src="StaffingAgency", dst="Liaison", label="[Recruited] 83263")
        # the second hear gets it
        diagram.note(col="Liaison", lines=["t = 16.5 ms: [hear] reads the answer"])
        # back to the recruiter
        diagram.unwind("Liaison", "Forkserver", "Builders")
        # and fifteen more like it
        diagram.note(
            col="Builders",
            lines=[
                "fifteen more round trips, 83264 to 83278, about 1.3 ms each",
                "each [hear] finds only its own answer",
            ],
        )
        # back to the loop
        diagram.unwind("Builders", "web", "dispatcher")
        # the second channel
        diagram.call(src="dispatcher", dst="Builders", label="fd 47: Crew.overhear")
        # back
        diagram.ret(src="Builders", dst="dispatcher")
        # and the control channel, on the readiness reported 66 ms earlier
        diagram.call(src="dispatcher", dst="Liaison", label="fd 8: report", kind="bad")
        # which reads an empty channel
        diagram.note(
            col="Liaison",
            lines=[
                "t = 66.3 ms: nothing is pending on fd 8",
                "[hear] → Pickler.recv → recv_fds waits for a header that is not coming",
                "the event loop stops: no request is served, no journal replayed",
            ],
            kind="bad",
        )
        # all done
        return

    def stopgap(self, diagram: Sequence) -> None:
        """
        The same pass with the stopgap in place
        """
        # the same moment
        diagram.trigger(label="the same pass", col="dispatcher", sub="with Channel.pending")
        # the report handler
        diagram.call(src="dispatcher", dst="Liaison", label="fd 8: report", kind="good")
        # asks first
        diagram.note(
            col="Liaison",
            lines=[
                "[control.pending()] is false: return True, and keep listening",
                "the next message from the agency makes fd 8 ready again",
            ],
            kind="good",
        )
        # back to the loop
        diagram.ret(src="Liaison", dst="dispatcher")
        # all done
        return

    # the lifelines, left to right
    cols = [
        "dispatcher",
        "web",
        "Builders",
        "Forkserver",
        "Liaison",
        "StaffingAgency",
        "member",
    ]

    # the scenarios, in the order they happen
    scenarios = [
        exit,
        race,
        stopgap,
    ]

    # the page
    title = "the liaison race, before the fix"
    # its accessible description
    label = (
        "Sequence of calls in one pass of a qed server's event loop: a member's exit report"
        " waits on the control channel; an HTTP request recruits sixteen builders, and the first"
        " recruitment reads the exit report while waiting for its answer; the report handler then"
        " runs on the stale readiness of the control channel and blocks; with the stopgap, it"
        " finds nothing pending and keeps listening."
    )
    # the paragraphs above the diagram
    intro = """<p><b>A historical record, not current behavior:</b> the defect this page draws is the reason recruitment works the way <code>doc/design/recruitment.md</code> describes.</p>
<p>The wedge of the qed server under the firefox suite, as captured on 2026-11-16 by a ring-buffer trace (pass 127 of the server's event loop, times from the start of the pass). The liaison's control channel has two readers: <code>Liaison.report</code>, an event handler, and <code>Liaison.recruit</code>, which reads synchronously until its answer arrives and delivers everything it hears on the way. The condition exists on main since <code>c652dcb6a</code>. Generated by <code>etc/introspection/liaison-race-historical.py</code>.</p>
<p class="muted">Lifelines: <b>dispatcher</b> is the server's event loop; <b>web</b> is the handler of an HTTP request; <b>Builders</b> is the qed team that renders pyramid levels, and owns its recruiter, <b>Forkserver</b>; <b>Liaison</b> is the agency's handle in the server; <b>StaffingAgency</b> runs in a process of its own; <b>member</b> is a builder's process, forked by the agency. Messages in brackets travel on the control channel.</p>
"""
    # the key to its colors
    key = """<div class="key"><span class="d"><b>blue</b>: states, and data</span><span class="r"><b>red</b>: the race</span><span class="g"><b>green</b>: the stopgap</span><span class="t"><b>dashed</b>: what starts a scenario</span><span>× return</span></div>"""


# main
if __name__ == "__main__":
    # instantiate
    app = LiaisonRace(name="liaison-race-historical")
    # invoke
    status = app.run()
    # and share the status with the shell
    raise SystemExit(status)


# end of file
