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
class RecruiterLifecycle(pyre.application):
    """
    Draw the life of a team whose members are recruited through the staffing agency, from the
    start of the agency to the shutdown of the application, as a page with one sequence diagram
    """

    # user configurable state
    out = pyre.properties.ostream(default="recruiter-lifecycle.html")
    out.doc = "the page to write"

    # obligations
    @pyre.export
    def main(self, *args, **kwds) -> int:
        """
        Build the page and write it out
        """
        # make the diagram
        diagram = Sequence(cols=self.cols, dx=150)
        # relate the heads: a staff owns its recruiter
        diagram.relate(src="Staff", dst="Forkserver", kind="owns")
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
    def start(self, diagram: Sequence) -> None:
        """
        The staffing agency is started, early by the application or by the first recruitment
        """
        # the application asks for the agency
        diagram.trigger(label="start the agency", col="application", sub="at activation, or lazily")
        # through the one liaison of the process
        diagram.note(
            col="application",
            lines=[
                "the [Liaison] is a component with a fixed name, so every recruiter",
                "gets the same one (T11)",
            ],
        )
        # which spawns the agency
        diagram.call(src="application", dst="Liaison", label="start", kind="good")
        # from the command line of the application
        diagram.note(
            col="Liaison",
            lines=[
                "opens the control channel, a [SocketPair]",
                "spawns the application's command line, script made absolute,",
                "in the shell [pyre.shells.forkserver], handing it the far end",
            ],
        )
        # the command line is captured before the working directory can change
        diagram.note(
            col="Liaison",
            lines=["when the command line is captured, and whether all of it is needed (open)"],
            kind="open",
        )
        # the new process builds the agency
        diagram.call(src="Liaison", dst="StaffingAgency", label="spawn", kind="good")
        # which serves on an event loop of its own
        diagram.note(
            col="StaffingAgency",
            lines=[
                "the shell builds the agency and runs its dispatcher (T4)",
                "requests: [whenReadReady] on the control channel",
                "exits: [whenSignal(SIGCHLD)], through [pyre.ipc.Signals]",
            ],
        )
        # and introduces itself
        diagram.call(src="StaffingAgency", dst="Liaison", label="[Greeting]", kind="good")
        # the liaison checks it
        diagram.note(
            col="Liaison",
            lines=[
                "the interpreter, the installation of pyre, the script",
                "a mismatch breaches a firewall",
            ],
        )
        # and listens for the agency's reports on the team's event loop
        diagram.call(src="Liaison", dst="dispatcher", label="whenReadReady", kind="good")
        # which watches the control channel from now on
        diagram.note(col="dispatcher", lines=["the control channel, and the agency's journal"])
        # back to the application
        diagram.unwind("dispatcher", "Liaison", "application")
        # all done
        return

    def recruit(self, diagram: Sequence) -> None:
        """
        A staff with work and vacancies recruits a member
        """
        # work arrives
        diagram.trigger(label="assign(task)", col="Staff", sub="vacancies: recruit")
        # the staff asks its recruiter
        diagram.call(src="Staff", dst="Forkserver", label="deploy")
        # which opens the channels the member will use
        diagram.note(
            col="Forkserver",
            lines=[
                "opens the crew channel, and the journal channel if wanted",
                "as [Fork.deploy] does",
            ],
        )
        # and asks the agency for a member
        diagram.call(src="Forkserver", dst="Liaison", label="recruit", kind="good")
        # with a request
        diagram.call(
            src="Liaison", dst="StaffingAgency", label="[Recruit] + descriptors", kind="good"
        )
        # what the request carries
        diagram.note(
            col="StaffingAgency",
            lines=[
                "the crew class, pickled, with the file its module came from",
                "the member's channel ends follow as a trailer",
            ],
        )
        # the agency forks
        diagram.call(src="StaffingAgency", dst="member", label="fork", kind="good")
        # the member makes itself
        diagram.note(
            col="member",
            lines=[
                "starts without the signal relay",
                "loads the crew class, refuses if it came from another file",
                "routes its journal, registers, runs",
            ],
        )
        # the agency answers with the pid
        diagram.call(src="StaffingAgency", dst="Liaison", label="[Recruited] pid", kind="good")
        # back to the recruiter and the staff
        diagram.unwind("Liaison", "Forkserver", "Staff")
        # the team side of the member joins the team
        diagram.note(
            col="Staff",
            lines=["closes its copies of the member's ends", "the member's proxy joins the team"],
        )
        # the member checks in over the crew channel
        diagram.call(src="member", dst="Staff", label="register")
        # and is put to work
        diagram.note(col="Staff", lines=["activate, then schedule"])
        # all done
        return

    def work(self, diagram: Sequence) -> None:
        """
        A member carries out tasks; the agency is not on the data path
        """
        # a task is scheduled
        diagram.trigger(label="schedule", col="Staff", sub="the crew channel")
        # the task goes to the member
        diagram.call(src="Staff", dst="member", label="task")
        # which carries it out
        diagram.note(col="member", lines=["executes it"])
        # and reports
        diagram.call(src="member", dst="Staff", label="report")
        # the staff collects
        diagram.note(
            col="Staff",
            lines=[
                "collect, requeue, or abandon",
                "the member is parked, or given the next task",
                "tasks, reports, descriptors and journal entries never pass through the agency",
            ],
        )
        # all done
        return

    def instruct(self, diagram: Sequence) -> None:
        """
        A journal control reaches the members, and the ones recruited from now on
        """
        # a control is applied
        diagram.trigger(label="instruct(control)", col="Staff", sub="a channel switched on")
        # the members already deployed are told directly
        diagram.call(src="Staff", dst="member", label="instruct")
        # and so is the recruiter
        diagram.call(src="Staff", dst="Forkserver", label="instruct")
        # which passes it on to the agency
        diagram.call(src="Forkserver", dst="Liaison", label="instruct", kind="good")
        # in a message
        diagram.call(src="Liaison", dst="StaffingAgency", label="[Instruct]", kind="good")
        # the agency applies it
        diagram.note(
            col="StaffingAgency", lines=["applies it, so members forked from now on start with it"]
        )
        # back to the staff
        diagram.unwind("StaffingAgency", "Liaison", "Forkserver", "Staff")
        # all done
        return

    def standDown(self, diagram: Sequence) -> None:
        """
        A staff stands down: its members are dismissed and nobody waits for them
        """
        # a staff with nothing to do
        diagram.trigger(label="standDown", col="Staff", sub="e.g. qed retires its builders")
        # for each parked member
        diagram.note(col="Staff", lines=["for each parked member: off the rosters"])
        # the member is told
        diagram.call(src="Staff", dst="member", label="dismissed")
        # what that means to the member
        diagram.note(col="member", lines=["no more tasks: retire, flush, and leave"])
        # the recruiter is told
        diagram.call(src="Staff", dst="Forkserver", label="dismiss(team, crew)", kind="good")
        # which arms the grace period and returns
        diagram.call(src="Forkserver", dst="dispatcher", label="alarm(grace)", kind="good")
        # back to the staff, at once
        diagram.unwind("dispatcher", "Forkserver", "Staff")
        # nothing waits
        diagram.note(
            col="Staff",
            lines=["returns at once: no waiting on the event loop (T3)"],
            kind="good",
        )
        # all done
        return

    def exit(self, diagram: Sequence) -> None:
        """
        A member leaves, and its exit reaches the recruiter and the team as events
        """
        # the agency hears the exit
        diagram.trigger(label="SIGCHLD", col="StaffingAgency", sub="through the signal relay")
        # it reaps every child that left
        diagram.note(col="StaffingAgency", lines=["[waitpid] without waiting, until none is left"])
        # and reports each one
        diagram.call(
            src="StaffingAgency", dst="dispatcher", label="[Exited] pid, status", kind="good"
        )
        # which wakes the liaison
        diagram.call(src="dispatcher", dst="Liaison", label="read ready", kind="good")
        # which tells the recruiter
        diagram.call(src="Liaison", dst="Forkserver", label="exited", kind="good")
        # the recruiter closes the books
        diagram.note(
            col="Forkserver", lines=["cancels the alarms it armed for the member, and forgets it"]
        )
        # and tells the team
        diagram.call(src="Forkserver", dst="Staff", label="departed(crew, status)", kind="good")
        # a hook the team may override
        diagram.note(col="Staff", lines=["a hook that does nothing by default (T10)"])
        # back along the chain
        diagram.unwind("Staff", "Forkserver", "Liaison", "dispatcher")
        # under Fork, the same ending
        diagram.note(
            col="dispatcher",
            lines=[
                "under [Fork], the member is the team's child: [whenSignal(SIGCHLD)]",
                "here, then the recruiter reaps it without waiting",
            ],
        )
        # all done
        return

    def grace(self, diagram: Sequence) -> None:
        """
        A dismissed member that does not leave within the grace period is made to
        """
        # the alarm fires
        diagram.trigger(label="grace expired", col="dispatcher", sub="the alarm of dismiss")
        # the recruiter insists
        diagram.call(src="dispatcher", dst="Forkserver", label="alarm", kind="good")
        # politely first
        diagram.call(src="Forkserver", dst="member", label="SIGTERM", kind="good")
        # and gives it another period
        diagram.call(src="Forkserver", dst="dispatcher", label="alarm(grace)", kind="good")
        # then for good
        diagram.note(
            col="Forkserver",
            lines=[
                "at the next alarm: [SIGKILL]",
                "the exit arrives as in the scenario above, and cancels what is armed",
            ],
        )
        # back to the loop
        diagram.unwind("dispatcher", "Forkserver", "dispatcher")
        # all done
        return

    def death(self, diagram: Sequence) -> None:
        """
        A member dies without being dismissed
        """
        # the team hears it first
        diagram.trigger(label="end of the crew channel", col="Staff", sub="a member died")
        # what the team does
        diagram.note(
            col="Staff",
            lines=[
                "off the rosters, its channel closed",
                "no [waitpid]: the member may not be the team's child",
            ],
        )
        # it hands the member to its recruiter
        diagram.call(src="Staff", dst="Forkserver", label="bury(team, crew)", kind="good")
        # which knows whose child it is
        diagram.note(
            col="Forkserver",
            lines=[
                "the agency's [Exited] report closes it, as above (T8, T12)",
                "under [Fork], [SIGCHLD] and a reap without waiting",
            ],
        )
        # back to the team
        diagram.ret(src="Forkserver", dst="Staff")
        # which may replace it
        diagram.note(col="Staff", lines=["a standing staff recruits a replacement"])
        # all done
        return

    def agencyDeath(self, diagram: Sequence) -> None:
        """
        The agency dies; the members already running are unaffected
        """
        # the liaison hears it
        diagram.trigger(label="end of the control channel", col="Liaison", sub="the agency died")
        # what happens to whom
        diagram.note(
            col="Liaison",
            lines=[
                "the members never talk to the agency, so they keep working",
                "its children are reparented to [init], which reaps them",
            ],
        )
        # a new agency, the way the first one started
        diagram.call(src="Liaison", dst="StaffingAgency", label="spawn", kind="good")
        # with the same greeting and checks
        diagram.note(col="StaffingAgency", lines=["as at the start"])
        # back to the liaison
        diagram.ret(src="StaffingAgency", dst="Liaison")
        # what happens when it cannot be started
        diagram.note(
            col="Liaison",
            lines=["an agency that cannot be started: refuse to recruit, or fork in place (open)"],
            kind="open",
        )
        # all done
        return

    def shutdown(self, diagram: Sequence) -> None:
        """
        The application ends: every member goes home, then the agency
        """
        # the staffs are disbanded
        diagram.trigger(label="disband", col="Staff", sub="at exit")
        # every member is dismissed
        diagram.call(src="Staff", dst="Forkserver", label="dismiss(team, crew)", kind="good")
        # back at once
        diagram.ret(src="Forkserver", dst="Staff")
        # and the team turns the loop until they are gone
        diagram.call(src="Staff", dst="dispatcher", label="watch, until all departed", kind="good")
        # nothing else runs now
        diagram.note(
            col="dispatcher",
            lines=[
                "nothing else runs at exit, so waiting is fine here,",
                "and it happens on the loop, as exits and alarms arrive",
            ],
        )
        # back to the staff
        diagram.ret(src="dispatcher", dst="Staff")
        # the staff is done
        diagram.end(col="Staff")
        # then the agency goes home
        diagram.gap(h=18)
        # when the application lets go of it
        diagram.trigger(label="stop the agency", col="application", sub="at exit")
        # through its liaison
        diagram.call(src="application", dst="Liaison", label="stop", kind="good")
        # closing the control channel is how it is told
        diagram.call(
            src="Liaison", dst="StaffingAgency", label="end of the control channel", kind="good"
        )
        # the agency's loop ends
        diagram.note(
            col="StaffingAgency", lines=["its dispatcher reads the end, the loop ends, it exits"]
        )
        # back to the application
        diagram.unwind("StaffingAgency", "Liaison", "application")
        # all done
        return

    # the lifelines, left to right
    cols = [
        "application",
        "Staff",
        "Forkserver",
        "Liaison",
        "dispatcher",
        "StaffingAgency",
        "member",
    ]

    # the scenarios, in the order they happen
    scenarios = [
        start,
        recruit,
        work,
        instruct,
        standDown,
        exit,
        grace,
        death,
        agencyDeath,
        shutdown,
    ]

    # the page
    title = "recruiter lifecycle"
    label = (
        "Sequence of calls in the life of a team whose members are recruited through the"
        " staffing agency: starting the agency, recruiting a member, work, a journal control,"
        " standing down, a member exiting, a grace period running out, a member dying, the"
        " agency dying, and shutdown."
    )
    intro = """<p>The life of a <code>pyre.nexus</code> team whose members come from the staffing agency, as settled for branch <code>teardown</code> on 2026-11-15 and written up in <code>doc/design/forkserver.md</code>. One lifeline per collaborator; time runs down. Each scenario starts at the margin with what sets it off, and ends when control returns there. Generated by <code>etc/introspection/recruiter-lifecycle.py</code>.</p>
<p class="muted">Lifelines: <b>application</b> is the process that runs the teams; <b>Staff</b> is the team, which owns its recruiter, <b>Forkserver</b>; <b>Liaison</b> is the agency's handle in the team's process; <b>dispatcher</b> is the team's event loop; <b>StaffingAgency</b> runs in a process of its own, spawned from the application's command line; <b>member</b> is a crew member, forked by the agency. Messages in brackets travel on the control channel. T-numbers are topics on the <a href="https://claude.ai/artifact/J1J6jqStmMkBmEqef2BnEd" target="_blank" rel="noopener">tracker</a>.</p>
"""
    key = """<div class="key"><span class="g"><b>green</b>: what the design changes</span><span class="o"><b>amber</b>: open question</span><span class="t"><b>dashed</b>: what starts a scenario</span><span class="d"><b>blue</b>: data</span><span>× return</span></div>"""


# main
if __name__ == "__main__":
    # instantiate
    app = RecruiterLifecycle(name="recruiter-lifecycle")
    # invoke
    status = app.run()
    # and share the status with the shell
    raise SystemExit(status)


# end of file
