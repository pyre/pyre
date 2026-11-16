<!--
-*- markdown -*-
-*- coding: utf-8 -*-

michael a.g. aïvázis <michael.aivazis@para-sim.com>
(c) 1998-2026 all rights reserved
-->

# Recruitment through the staffing agency: one reader per channel

Status: agreed 2026-11-16 (michael), as B with D, keeping the guard in `Liaison.report`. The
questions were R1-R4 on the `ipc` tracker.

## The defect

The liaison's control channel had two readers. `Liaison.report`, an event handler, heard the
agency's messages as they arrived; `Liaison.recruit` sent a `Recruit` and then read the same
channel synchronously until its `Recruited` answer was in, delivering everything it heard on the
way. When a handler that recruits ran earlier in the same pass of the event loop as `report`, the
recruitment took delivery of the message whose readiness the dispatcher had recorded for the
control channel, and `report` then read an empty channel and blocked the event loop for good.

A ring-buffer trace of a qed server captured it: in one pass, the selector reported an HTTP
connection, a builder's journal and the control channel ready; the HTTP handler recruited sixteen
builders over 50 ms, and the first recruitment delivered the agency's report of an exit that was
waiting; 66 ms into the pass the dispatcher called `report`, which found nothing pending and
blocked in `recv_fds`. The condition existed on main since the agency took over the forkserver
(`c652dcb6a`). The race is drawn, as a historical record, in
`etc/introspection/liaison-race-historical.py`.

## What stays

The agency's reports of exits stay. The members are the agency's children, so only the agency can
collect them and their exit status. The recruiter's ledger of departures, which dismissal and
`settle` wait on, empties only through those reports (`Forkserver.reap` reads them through
`Liaison.collect`). That a member's crew channel has ended does not mean its process is gone: it
may still be leaving, or stuck, and the grace period and the kill that follows it depend on knowing
which.

## The alternatives

| | the race | stale readiness from any other reader | a partly arrived report | round trips | size |
|---|---|---|---|---|---|
| **A.** recruitment that does not wait: tickets, the pid as a message, incremental framing | removed | removed | removed | none waited on | large |
| **B.** two channels: requests and their answers on one, the agency's reports on the other | removed | not covered | blocks, bounded | one per member | small |
| **B** with the guard in `report` kept | removed | removed | blocks, bounded | one per member | small |
| **C.** no exit reports: a death is learned when the crew channel ends | removed | n/a | n/a | one per member | undoes what stays, above |
| **D.** batch recruitment: one request for all the vacancies of a team | narrowed | not covered | blocks, bounded | one per team | small; combines with B |

## The design: B with D, and the guard

**B. One reader per channel.** The agency talks to its liaison over two channels, beside the one
its journal travels over. The control channel carries the conversation the liaison starts:
`Greeting` once, then each `Recruit` and its `Recruited`, and `Instruct`, which has no answer; only
`spawn` and `recruit` read it, synchronously, and nothing listens to it on an event loop. The
report channel carries what the agency says on its own, its reports of exits; only `report` reads
it, from the event loop. A recruitment cannot deliver a report, and the readiness of the report
channel is consumed only by the handler it wakes. The end of the agency shows on both: `report`
sees the end of the report channel and stops listening, and a recruitment in progress sees the end
of the control channel.

**The guard.** `report` still checks `Channel.pending()` before it reads, and keeps listening when
nothing is waiting, so a reader the design does not foresee, e.g. an event loop of `settle` nested
in a handler of another loop that listens to the same channel, cannot turn stale readiness into a
hang. What remains is a report caught half-written: the agency writes each report whole to a local
socket, so the wait for the rest is bounded by a local write.

**D. One request per team.** `Forkserver.recruit` fills all the vacancies of a team with one
`Recruit`, which carries the class of the members and the member's ends of the channels of each of
them; the agency forks them one after the other and answers with all their pids in one
`Recruited`. Sixteen builders cost one round trip instead of sixteen. A message carries at most
`SocketPair.capacity` descriptors, so a team with more members than fit is recruited in as many
requests as it takes. `Forkserver.deploy`, the recruitment of a single member, is a request for
one. Each member the agency forks inherits the ends of the members forked after it, and closes
them; the ends of the members forked before it are already closed.

## What changes

- `Liaison.spawn` opens a third socket pair, the report channel, and hands the agency its end on
  the command line, as the channel trait `reports` of `shells/Forkserver`; `Liaison.listen`
  watches the report channel instead of the control channel; `report` reads the report channel.
- `StaffingAgency.serve` takes the report channel; `harvest` writes `Exited` to it; the members
  close it, with the control channel, as they start.
- `Recruit` carries the class of the members and lists of their channels and journals; `Recruited`
  carries the list of their pids; `Liaison.recruit` returns the list.
- `Forkserver` overrides `recruit` to fill the vacancies in batches, and `deploy` recruits a batch
  of one.
- The drivers that talk to the agency directly follow suit: the `forkserver_*` drivers, and
  `liaison_report_drained`, which keeps checking the guard. A new driver checks that a recruitment
  leaves the agency's reports alone, and another checks `Channel.pending()`.
- `doc/design/forkserver.md` and `etc/introspection/recruiter-lifecycle.py` show the report
  channel and the batched request.

## What it leaves alone

T13 of the `pyre.nexus` Recruiters tracker, the crew protocol as messages, changes the conversation
between a team and its members over the crew channel; this design changes only the conversation
between the liaison and the agency, so neither disturbs the other. A, recruitment that does not
wait, remains a possible step of its own; incremental framing, if it is built, serves the crew
channel too.


<!-- end of file -->
