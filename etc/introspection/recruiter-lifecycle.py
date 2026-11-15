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
    start of the agency to the shutdown of the application, with the states of each party and
    the transitions between them, as a page with one sequence diagram
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
        diagram = Sequence(cols=self.cols, dx=128)
        # relate the heads: a staff owns its recruiter
        diagram.relate(src="Staff", dst="Forkserver", kind="owns")
        # and the recruiter owns the departures on its ledger
        diagram.relate(src="Forkserver", dst="Departure", kind="owns")
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
        diagram.trigger(label="Forkserver.start", col="application", sub="at activation, or lazily")
        # through the one liaison of the process
        diagram.call(src="application", dst="Liaison", label="Liaison.instance().start")
        # which has nothing running
        diagram.note(
            col="Liaison",
            lines=[
                "the component named [pyre.nexus.liaison]: every recruiter gets the same one",
                "liaison: [idle] → [spawning]",
            ],
        )
        # so it spawns the agency
        diagram.call(src="Liaison", dst="StaffingAgency", label="spawn")
        # from the command line of the application
        diagram.note(
            col="StaffingAgency",
            lines=[
                "[StaffingAgency.command] + --shell=forkserver, control and journal ends",
                "the shell builds the agency, which serves on its own dispatcher:",
                "requests by [whenReadReady], exits by [whenSignal(SIGCHLD)]",
                "agency: [serving]",
            ],
        )
        # and introduces itself
        diagram.call(src="StaffingAgency", dst="Liaison", label="[Greeting]")
        # the liaison checks it
        diagram.note(
            col="Liaison",
            lines=[
                "[greeted]: interpreter, pyre, script must match; a firewall if not",
                "liaison: [spawning] → [running]",
            ],
        )
        # and is heard on the team's event loop
        diagram.call(src="Liaison", dst="dispatcher", label="whenReadReady")
        # what it listens to
        diagram.note(
            col="dispatcher", lines=["[report] on the control channel, [overhear] on the journal"]
        )
        # back to the application
        diagram.unwind("dispatcher", "Liaison", "application")
        # all done
        return

    def recruit(self, diagram: Sequence) -> None:
        """
        A staff with work and vacancies recruits a member
        """
        # work arrives
        diagram.trigger(label="Staff.assign", col="Staff", sub="vacancies: recruit")
        # the staff asks its recruiter
        diagram.call(src="Staff", dst="Forkserver", label="deploy")
        # which opens the channels
        diagram.note(col="Forkserver", lines=["opens the crew channel and the journal channel"])
        # and asks the liaison for a member
        diagram.call(src="Forkserver", dst="Liaison", label="recruit")
        # which sends the request
        diagram.call(src="Liaison", dst="StaffingAgency", label="[Recruit] + descriptors")
        # what it carries
        diagram.note(
            col="StaffingAgency",
            lines=["the crew class, pickled, with the file of its module; the member's ends"],
        )
        # the agency forks
        diagram.call(src="StaffingAgency", dst="member", label="enlist: fork")
        # the member makes itself
        diagram.note(
            col="member",
            lines=[
                "member: [forked]",
                "[Crew.route]: its journal goes to the team first",
                "[Recruit.load]: a class from another file breaches a firewall, and it leaves",
                "builds itself, [register]s, [work]s",
                "member: [forked] → [working]",
            ],
        )
        # the agency answers with the pid
        diagram.call(src="StaffingAgency", dst="Liaison", label="[Recruited] pid")
        # back to the recruiter
        diagram.ret(src="Liaison", dst="Forkserver")
        # which makes the team side of the member
        diagram.call(src="Forkserver", dst="Crew", label="team.crew + join")
        # its first state
        diagram.note(col="Crew", lines=["crew: [registered]"])
        # back to the staff
        diagram.unwind("Crew", "Forkserver", "Staff")
        # the staff files it
        diagram.note(col="Staff", lines=["on the roster [registered]"])
        # all done
        return

    def checkin(self, diagram: Sequence) -> None:
        """
        The member checks in and takes tasks; the agency is not on the data path
        """
        # the member checks in
        diagram.trigger(label="checkin", col="member", sub="the crew channel")
        # its status
        diagram.call(src="member", dst="Crew", label="[crewcodes.healthy]")
        # the team side tells the staff
        diagram.call(src="Crew", dst="Staff", label="activate")
        # which moves it
        diagram.note(col="Staff", lines=["crew: [registered] → [active]", "then [schedule]"])
        # back
        diagram.ret(src="Staff", dst="Crew")
        # a task goes out
        diagram.call(src="Crew", dst="member", label="execute: the task")
        # the member does it
        diagram.note(col="member", lines=["[perform]s it, then [report]s"])
        # and reports
        diagram.call(src="member", dst="Crew", label="(crewstatus, taskstatus, result)")
        # the team side settles the task and the member
        diagram.note(
            col="Crew",
            lines=["[assess]: collect, requeue, or abandon; a healthy member is [schedule]d again"],
        )
        # with nothing to do, the staff parks it
        diagram.call(src="Crew", dst="Staff", label="submit, nothing to do")
        # how
        diagram.note(
            col="Staff",
            lines=["crew: [active] → [idle], with a [vigil] on its channel"],
        )
        # back
        diagram.ret(src="Staff", dst="Crew")
        # all done
        return

    def instruct(self, diagram: Sequence) -> None:
        """
        A journal control reaches the members, and the ones recruited from now on
        """
        # a control is applied
        diagram.trigger(label="Staff.instruct", col="Staff", sub="a channel switched on")
        # the members already deployed are told directly
        diagram.call(src="Staff", dst="Crew", label="instruct")
        # over the journal channel
        diagram.call(src="Crew", dst="member", label="the encoded control")
        # back
        diagram.unwind("member", "Crew", "Staff")
        # and so is the recruiter
        diagram.call(src="Staff", dst="Forkserver", label="instruct")
        # which passes it on
        diagram.call(src="Forkserver", dst="Liaison", label="instruct")
        # to the agency
        diagram.call(src="Liaison", dst="StaffingAgency", label="[Instruct]")
        # which applies it
        diagram.note(
            col="StaffingAgency", lines=["applies it: members forked from now on start with it"]
        )
        # back to the staff
        diagram.unwind("StaffingAgency", "Liaison", "Forkserver", "Staff")
        # all done
        return

    def standDown(self, diagram: Sequence) -> None:
        """
        A staff stands down: its parked members are dismissed, and nobody waits for them
        """
        # a staff with nothing to do
        diagram.trigger(label="Staff.standDown", col="Staff", sub="e.g. qed retires its builders")
        # it rests
        diagram.note(
            col="Staff",
            lines=["staff: [serving] → [resting]", "for each [idle] member: [_release]"],
        )
        # the member is told
        diagram.call(src="Staff", dst="Crew", label="dismissed")
        # with the end of tasks marker
        diagram.call(src="Crew", dst="member", label="None")
        # what the member does
        diagram.note(
            col="member",
            lines=[
                "no more tasks: [leave]: [retire], flush, [os._exit]",
                "member: [working] → [exited]",
            ],
        )
        # back
        diagram.ret(src="Crew", dst="Staff")
        # the team side is off the rosters
        diagram.note(col="Staff", lines=["crew: [idle] → [dismissed]"])
        # the recruiter is told
        diagram.call(src="Staff", dst="Forkserver", label="dismiss(team, crew)")
        # which puts it on the ledger
        diagram.call(src="Forkserver", dst="Departure", label="depart")
        # its state
        diagram.note(
            col="Departure",
            lines=[
                "deadline: now + grace; reminders: [SIGTERM], [SIGKILL]",
                "departure: [leaving]",
            ],
        )
        # back
        diagram.ret(src="Departure", dst="Forkserver")
        # the recruiter collects anybody already gone, then watches
        diagram.note(
            col="Forkserver",
            lines=[
                "[collect]: a member already gone is collected now",
                "[watch]: [listen] (the liaison's exits) and one [alarm] per event loop",
                "recruiter: [quiet] → [watching]",
            ],
        )
        # it subscribes once
        diagram.call(src="Forkserver", dst="Liaison", label="subscribe(exited)")
        # and arms the alarm once
        diagram.call(src="Forkserver", dst="dispatcher", label="alarm(grace, remind)")
        # back to the staff at once
        diagram.unwind("dispatcher", "Forkserver", "Staff")
        # nobody waits
        diagram.note(
            col="Staff", lines=["returns at once: no waiting on the event loop"], kind="good"
        )
        # all done
        return

    def exit(self, diagram: Sequence) -> None:
        """
        A member leaves, and its exit reaches the recruiter and the team as events
        """
        # the agency hears the exit
        diagram.trigger(label="SIGCHLD", col="StaffingAgency", sub="through pyre.ipc.Signals")
        # it reaps every child that left
        diagram.note(
            col="StaffingAgency", lines=["[harvest]: [waitpid(-1, WNOHANG)] until none is left"]
        )
        # and reports each one
        diagram.call(src="StaffingAgency", dst="dispatcher", label="[Exited] pid, status")
        # which wakes the liaison
        diagram.call(src="dispatcher", dst="Liaison", label="report")
        # which files it and tells its subscribers
        diagram.note(col="Liaison", lines=["[hear] → [exited]: the report goes on its pile"])
        # the recruiter
        diagram.call(src="Liaison", dst="Forkserver", label="exited")
        # collects
        diagram.note(col="Forkserver", lines=["[collect]: [reap] each pid on the ledger"])
        # by asking the liaison
        diagram.call(src="Forkserver", dst="Liaison", label="collect(pid)")
        # back
        diagram.ret(src="Liaison", dst="Forkserver")
        # takes it off the ledger
        diagram.call(src="Forkserver", dst="Departure", label="pop")
        # its last state
        diagram.note(col="Departure", lines=["departure: [leaving] → [collected]"])
        # back
        diagram.ret(src="Departure", dst="Forkserver")
        # and tells the team
        diagram.call(src="Forkserver", dst="Staff", label="departed(crew, status)")
        # what the team does
        diagram.note(
            col="Staff", lines=["crew: [dismissed] → [gone]; a hook that does nothing by default"]
        )
        # back along the chain
        diagram.unwind("Staff", "Forkserver", "Liaison", "dispatcher")
        # the recruiter may go quiet
        diagram.note(
            col="dispatcher",
            lines=[
                "an empty ledger: [exited] returns false, the subscription ends",
                "recruiter: [watching] → [quiet]",
                "under [Fork], the same through [whenSignal(SIGCHLD)] and [waitpid(pid, WNOHANG)]",
            ],
        )
        # all done
        return

    def grace(self, diagram: Sequence) -> None:
        """
        A dismissed member that does not leave within the grace period is made to
        """
        # the alarm fires
        diagram.trigger(label="alarm", col="dispatcher", sub="the next deadline")
        # the recruiter's handler
        diagram.call(src="dispatcher", dst="Forkserver", label="remind")
        # collects first
        diagram.note(col="Forkserver", lines=["[collect] whoever left"])
        # then reminds the late
        diagram.call(src="Forkserver", dst="Departure", label="remind")
        # politely first
        diagram.call(src="Departure", dst="member", label="SIGTERM")
        # the departure's state
        diagram.note(
            col="Departure",
            lines=[
                "departure: [leaving] → [reminded]",
                "at the next deadline, [SIGKILL]: departure: [reminded] → [killed]",
                "then only its exit is left to collect",
            ],
        )
        # back
        diagram.ret(src="Departure", dst="Forkserver")
        # the alarm comes back at the next deadline
        diagram.note(
            col="Forkserver",
            lines=["returns the time to the next deadline, or [None] once the ledger is empty"],
        )
        # back to the loop
        diagram.ret(src="Forkserver", dst="dispatcher")
        # all done
        return

    def death(self, diagram: Sequence) -> None:
        """
        A member dies without being dismissed
        """
        # the team hears it first
        diagram.trigger(
            label="end of the crew channel", col="Crew", sub="a vigil, or an assessment"
        )
        # the team side tells the staff
        diagram.call(src="Crew", dst="Staff", label="bury")
        # what the team does
        diagram.note(
            col="Staff",
            lines=["crew: [idle] or [active] → [buried]", "off the rosters, its channel closed"],
        )
        # it hands the member to its recruiter
        diagram.call(src="Staff", dst="Forkserver", label="bury(team, crew)")
        # which treats it as a departure
        diagram.call(src="Forkserver", dst="Departure", label="depart")
        # same as a dismissal
        diagram.note(col="Departure", lines=["departure: [leaving]; its exit arrives as above"])
        # back
        diagram.unwind("Departure", "Forkserver", "Staff")
        # the staff may replace it
        diagram.note(col="Staff", lines=["a [serving] staff recruits a replacement"])
        # back
        diagram.ret(src="Staff", dst="Crew")
        # all done
        return

    def agencyDeath(self, diagram: Sequence) -> None:
        """
        The agency dies; the members already running are unaffected
        """
        # the liaison hears it
        diagram.trigger(label="end of the control channel", col="dispatcher", sub="the agency died")
        # through its handler
        diagram.call(src="dispatcher", dst="Liaison", label="report")
        # which stops listening
        diagram.note(
            col="Liaison",
            lines=[
                "[EndOfStream]: the handler returns false",
                "liaison: [running] → [lost]; the members keep working, reparented to [init]",
            ],
        )
        # back
        diagram.ret(src="Liaison", dst="dispatcher")
        # the next start spawns a new one
        diagram.note(
            col="dispatcher",
            lines=[
                "the next [start]: every listening loop [forget]s the old channels,",
                "they are closed, and a new agency is spawned, as at the start",
            ],
        )
        # what is open
        diagram.note(
            col="dispatcher",
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
        diagram.trigger(label="Staff.disband", col="Staff", sub="at exit")
        # for good
        diagram.note(
            col="Staff",
            lines=[
                "staff: [disbanded]",
                "the [idle] and [registered] are told to leave, the [active] get [SIGKILL]",
            ],
        )
        # every member is handed over
        diagram.call(src="Staff", dst="Forkserver", label="dismiss(team, crew)")
        # back at once
        diagram.ret(src="Forkserver", dst="Staff")
        # then the staff waits for all of them at once
        diagram.call(src="Staff", dst="Forkserver", label="settle")
        # on a loop of its own
        diagram.note(
            col="Forkserver",
            lines=[
                "a fresh loop like the team's, which may be the caller or not running",
                "[watch] on it; [collect] stops it once the ledger is empty",
                "recruiter: [watching] → [settling] → [quiet]",
            ],
        )
        # back
        diagram.ret(src="Forkserver", dst="Staff")
        # the staff is done
        diagram.end(col="Staff")
        # then the agency goes home
        diagram.gap(h=18)
        # when the application lets go of it
        diagram.trigger(label="Forkserver.stop", col="application", sub="at exit")
        # through its liaison
        diagram.call(src="application", dst="Liaison", label="stop")
        # closing the control channel is how it is told
        diagram.call(src="Liaison", dst="StaffingAgency", label="end of the control channel")
        # the agency's loop ends
        diagram.note(
            col="StaffingAgency",
            lines=["[request] reads the end, stops its loop", "agency: [serving] → [gone]"],
        )
        # back to the application
        diagram.unwind("StaffingAgency", "Liaison", "application")
        # the liaison's last state
        diagram.note(col="application", lines=["liaison: [running] → [idle]"])
        # all done
        return

    # the lifelines, left to right
    cols = [
        "application",
        "Staff",
        "Crew",
        "Forkserver",
        "Departure",
        "Liaison",
        "dispatcher",
        "StaffingAgency",
        "member",
    ]

    # the scenarios, in the order they happen
    scenarios = [
        start,
        recruit,
        checkin,
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
        " staffing agency, with the states of each party: starting the agency, recruiting a"
        " member, its check-in and work, a journal control, standing down, a member exiting, a"
        " grace period running out, a member dying, the agency dying, and shutdown."
    )
    intro = """<p>The life of a <code>pyre.nexus</code> team whose members come from the staffing agency, as built on branch <code>teardown</code>, with the state of every party and each transition, written <span style="color:var(--data)">state → state</span> where it happens. One lifeline per collaborator; time runs down. Each scenario starts at the margin with what sets it off, and ends when control returns there. Generated by <code>etc/introspection/recruiter-lifecycle.py</code>; the states are tabulated in <code>doc/design/forkserver.md</code>.</p>
<p class="muted">Lifelines: <b>application</b> is the process that runs the teams; <b>Staff</b> is the team, which owns its recruiter, <b>Forkserver</b>; <b>Crew</b> is the team side of a member; <b>Departure</b> is a member on the recruiter's ledger of departures; <b>Liaison</b> is the agency's handle in the team's process; <b>dispatcher</b> is the team's event loop; <b>StaffingAgency</b> runs in a process of its own, spawned from the application's command line; <b>member</b> is a crew member's process, forked by the agency. Messages in brackets travel on the control channel.</p>
"""
    key = """<div class="key"><span class="d"><b>blue</b>: states, and data</span><span class="g"><b>green</b>: nobody waits</span><span class="o"><b>amber</b>: open question</span><span class="t"><b>dashed</b>: what starts a scenario</span><span>× return</span></div>"""


# main
if __name__ == "__main__":
    # instantiate
    app = RecruiterLifecycle(name="recruiter-lifecycle")
    # invoke
    status = app.run()
    # and share the status with the shell
    raise SystemExit(status)


# end of file
