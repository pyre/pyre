<!--
-*- markdown -*-
-*- coding: utf-8 -*-

michael a.g. aïvázis <michael.aivazis@para-sim.com>
(c) 1998-2026 all rights reserved
-->

# Report payloads

Status: **agreed** on 2026-11-17, from the choices made in a tracker, topics P1–P12; being built
on branch `payloads`.

A crew member's report is a tuple `(crewstatus, taskstatus, result)` that `Crew.report` sends to
its team with the marshaler. When the result holds an open file, the file travels inside the
report as a channel, the same way channels already travel between processes (`ipc.md`). Nothing
outside the marshaler handles a raw descriptor.

## The file channel

1. `pyre.ipc.File` is a channel over an open file. Its inbound and outbound ends are the same
   descriptor, it travels like every other channel, and it arrives as a copy (`ipc.md`,
   decision 4).
2. The channel owns the descriptor. A client that holds a file, such as qed's `Spool`, moves its
   descriptor into a `File` and reaches the file only through the channel: sharing it (a
   duplicate), mapping it, and closing it. The duplicate is a python file object, so the http
   server's `transmit` takes it as it takes any file today.

## Sending a report

3. `Crew.report` sends the report as is. The manifest finds the channels inside the result and
   carries their descriptors with the message; qed's `Crew.report` and `Crew.harvest` overrides
   are no longer needed.
4. A channel that travels arrives as a copy, so the sender's own copy is still open after the
   send. `Crew.report` closes every channel its report carried: the marshaler's `send` returns the
   manifest of the message, which records the channels it declared.

## A descriptor that cannot arrive

5. A process whose descriptor table is full cannot receive a descriptor. The kernels report this
   differently (measured 2026-11-17):
   - macOS: the receive raises `EMSGSIZE`, every byte of the message stays in the socket, and
     the descriptor is lost;
   - linux: the receive returns the bytes with `MSG_CTRUNC` set and no descriptors.
6. `SocketPair.receive` delivers the bytes in both cases, reading them again on macOS, so the
   stream stays framed; it records nothing about the loss. `write` refuses to carry more
   descriptors than `capacity`, so a truncation on arrival means a full table, not an oversized
   message; the capacity firewall goes away.
7. `Pickler.recv` reads the whole message, header and body, before it claims the descriptors.
   The header says how many to expect: when fewer arrived, `claim` closes the ones that did and
   raises `ArrivalError`, a `CarriageError`, naming the channel and both counts. The next message
   on the channel is intact.
8. `Crew.assess` treats an `ArrivalError` from `harvest` as a failed task, which takes the
   existing path for recoverable failures: a `Pool` puts the task back in its workplan, a `Staff`
   hands the failure to its client. The member stays at work. qed's drain of the trailer byte
   goes away.
9. A `Pool` gives up on a task that keeps failing: its `retries` trait, 3 by default, bounds the
   recoverable failures of each task, and once a task exceeds it the pool abandons it with its
   last error. The count is forgotten when the task completes or is abandoned. A `Staff` keeps
   handing every failure to its client.

## Tests

- `File`: travels over a socket pair and arrives as a working copy; the sender's copy is
  independent of it.
- `SocketPair.receive` and `Pickler.recv` with a full table, on the platform at hand: the
  message is consumed, `ArrivalError` is raised, and the next message arrives whole.
- `Crew.report` closes what it carried; `Crew.assess` keeps a member whose report could not
  arrive.
- A `Pool` abandons a task after `retries` recoverable failures, and its batch completes.

## Later

- P7: the crew protocol as message classes, on a branch of its own.


<!-- end of file -->
