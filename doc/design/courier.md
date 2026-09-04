<!-- -*- Markdown -*-
   -
   - michael a.g. aïvázis <michael.aivazis@para-sim.com>
   - (c) 1998-2026 all rights reserved
   -->

# journal delivery over ipc

A design for carrying journal entries out of the process that produced them, so that a
parent can collect the diagnostics of the workers it forked, a server can show them to a
remote client, and, later, a daemon can gather them from every participant of a
distributed application. The generic pieces are `journal` and `pyre.nexus` work; what a
particular application does with the collected entries is its own business. The first
consumer is `qed`, whose side of the design is in `qed/doc/console.md`.

Branches: `journal` in both `pyre` and `qed`.

Status: **the record, the courier, the entry constructor, the replay, the collection in
the nexus, and the opening payload on the event stream are built and tested** (2026-09-04,
branch `journal`); the C++ courier, the control records, and the daemon are not. Every fact
below about the code that preceded this work was read out of the source on 2026-09-04, with
the file cited; open questions are marked as such.

## Goal

An application built on `pyre.nexus` forks worker processes. Each worker inherits the
parent's journal configuration and device, so everything it says goes to the terminal
the parent was launched from, interleaved by descriptor rather than by entry, and
attributed to nobody. A device installed in the parent sees nothing a worker emits.
For a server whose interesting failures happen on its workers, and whose user is a
browser client that cannot see the terminal at all, this is the wrong shape.

The work is to make shipping an entry somewhere else a capability of the journal, and
collecting the entries of one's workers a capability of the nexus, with these
guarantees:

1. **Nothing changes at a call site.** Channels are opened and flushed exactly as
   today. Delivery is a device, installed the way devices are installed.
2. **A diagnostic facility may never block or kill the application it describes.**
   Sends are non-blocking, the queue is bounded, entries are dropped rather than
   stalled when the far end is slow, and a far end that is absent is a non-event.
3. **The record format is language neutral.** C++ and Python emit the same bytes, so
   a C++ device can be added without touching a consumer.
4. **The primitive is separate from the deployment.** A device that marshals entries
   onto a descriptor is the primitive; what sits at the far end (the parent's event
   loop, a server, a daemon) is policy. Building the device first is wasted under no
   deployment.

## What is already true

Read out of the source; these are the facts the design rests on.

- **A device is three methods.** `alert` for `info`/`warning`/`error`, `memo` for
  `debug`/`firewall`, `help` for help screens; each takes an entry. Identical in shape
  on both sides: `packages/journal/Device.py:13-42` and `lib/journal/Device.h:41-43`.
- **An entry is a page and notes.** `page` is a list of lines, `notes` a string-to-string
  map: `packages/journal/Entry.py:9-36`, `lib/journal/Entry.h:73-75`. The notes always
  carry `channel`, `severity` and `application`; `filename`, `line` and `function` when
  the entry was flushed with a location; and whatever the call site added. Nothing in
  either implementation records a timestamp, a process id, a host, or a thread.
- **One chronicler serves both languages.** With the bindings loaded, `journal.chronicler`
  is the pybind11 class whose `device` property reads and writes the static
  `pyre::journal::Chronicler::_device` in `libjournal` (`extensions/journal/chronicler.cc:54-69`,
  `lib/journal/Chronicler.cc:149`). The extension links against the shared library, so
  every C++ channel in the process resolves to the same default device as every Python
  channel.
- **A Python device captures C++ entries.** `journal.device` is the C++ `Device` exposed
  through a trampoline that forwards the three virtuals (`extensions/journal/devices.cc:19-43`).
  A Python subclass installed on the chronicler therefore receives entries flushed from
  C++, provided the flush happens on a thread that can take the interpreter lock. The
  entry arrives by reference, with `page` and `notes` as the opaque `Page` and `Notes`
  containers (`extensions/journal/entry.cc:19-21`); the callee must copy what it wants
  to keep. No code in the tree subclasses the trampolined device yet.
- **Device resolution cascades.** Per-channel device, then the severity-wide default,
  then the chronicler's device: `packages/journal/Channel.py:78-90`,
  `lib/journal/InventoryProxy.icc:41-73`. The bound channels expose `device` as a
  property (`extensions/journal/debug.cc:79` and siblings).
- **Workers are forked after the journal is configured, and never reconfigure it.**
  `pyre.nexus.Fork.deploy` opens one channel pair, calls `os.fork`, and in the child
  closes the parent's end, sheds the connections it inherited, builds the crew member
  and runs it (`packages/pyre/nexus/Fork.py:49-88`). Nothing in `pyre.nexus` touches the
  chronicler or the device, so the child keeps the parent's device object and its
  descriptor.
- **The crew channel is a blocking, single-purpose protocol.** One channel per member,
  `Pickler` framed, carrying a status word at birth, a task per assignment, a report per
  completion, and `None` at dismissal (`packages/pyre/nexus/Crew.py:106,275,354,232`).
  The team reads it only when it expects a report. `pyre.ipc` has no non-blocking send
  and no bounded buffer anywhere (`packages/pyre/ipc/Pipe.py:104-109`,
  `packages/pyre/ipc/Socket.py:106-113`).
- **The event loop already serves the parent.** `Fork` hands the team side of a crew
  member the shared dispatcher (`Fork.py:84`), and `whenReadReady` accepts several
  handlers per descriptor, each kept while it returns true
  (`packages/pyre/ipc/SelectorPSL.py:40-57,247-249`).
- **The journal package imports pyre.** `Device` derives from `pyre.patterns.named`, so a
  device that uses `os` and `json` adds no dependency the package does not already have.
  It must not import `pyre.ipc`; the transport is the caller's concern.
- **There has never been a network device.** No socket, daemon or remote device exists
  in the current tree or its history, and the `journal:` heading in `TODO` is empty.

## Architecture

Four pieces, in the order they should be built. The first two live in `journal`, the
third in `pyre.nexus`, the fourth is a later deployment.

### The record

One entry becomes one record: a JSON object on a single line, terminated by a newline.
JSON escapes the newlines inside strings, so line boundaries are record boundaries, and
a consumer in any language can split, parse and forward a record without understanding
it. The fields:

| field | type | meaning |
|---|---|---|
| `journal` | integer | the record format version, `1` |
| `seq` | integer | the sequence number of the record within its process, from 1 |
| `pid` | integer | the process that flushed the entry |
| `time` | float | seconds since the epoch at the flush |
| `sink` | string | which device method the entry was delivered to: `alert`, `memo`, or `help` |
| `page` | list of strings | the lines of the entry |
| `notes` | object of strings | the notes of the entry, as flushed |

Severity and channel are not repeated at the top level; they are in the notes, where
the journal put them. The envelope adds only what the journal does not know: the sink,
which the far end needs to route the entry to the same device method, and the three
origin fields, which the journal has no notion of and which are what make entries from
several processes orderable and attributable. Cross-process order is approximate and
`time` is the best available; `seq` is exact within a process and lets a consumer
detect drops.

The codec is a small module, `packages/journal/Record.py`, with `encode(entry, sink)`
returning bytes and `decode(line)` returning a plain record object, and a C++ twin
later. It copies `page` and `notes` out of the entry, so it works on both the pure
Python entry and the bound one.

### `Courier`, the device

`journal.Courier` is a device that writes records to a file descriptor it is given. It
takes the descriptor, not a `pyre.ipc` channel, so it lives in the journal package and
knows nothing about transports; the caller hands it the outbound descriptor of a pipe,
a socket pair, or a connected Unix socket. Its behavior:

- **It never blocks.** The descriptor is switched to non-blocking at construction. A
  write that cannot complete leaves the remainder in a pending buffer, which is flushed
  before the next record is attempted; a record that cannot be started because the
  buffer is still pending is dropped whole. Records are therefore never torn on the
  wire, only missing.
- **It never raises.** `EAGAIN` counts a drop. `EPIPE` and any other descriptor error
  mark the courier dead; from then on it delivers nothing and says nothing. A far end
  that closed is not an error in the process it was watching.
- **Drops are reported.** When a write succeeds after drops, the courier emits one
  synthetic record of its own, on the `journal.courier` channel at warning severity,
  saying how many records were lost. The count is in the notes so a consumer can
  show it without parsing prose.
- **It can mirror.** An optional second device receives every entry unchanged, before
  the courier ships it. This is how a process keeps its terminal output while also
  delivering elsewhere; a worker whose parent replays everything does not mirror, or
  every line would print twice.
- **It closes what it owns.** `close()` releases the descriptor; the courier is dead
  afterwards.

It is a subclass of `journal.device`, whichever implementation that is, so that the
chronicler accepts it in both the bound and the pure Python configurations. This
makes it the first Python device that exercises the trampoline, and the first that
must cope with `Page` and `Notes` rather than a list and a dict; the record codec
absorbs that difference.

**The C++ twin**, `pyre::journal::Courier`, writes the same bytes and follows the same
rules. It is not needed by an application whose C++ runs inside Python processes, since
the Python courier already sees those entries through the trampoline. It is needed by a
pure C++ participant and by the daemon deployment, and it is the reason the record
format is JSON rather than a pickle. It is scheduled after the Python pieces are proven.

### Collection in `pyre.nexus`

The fan-in lives with the recruiter, because the recruiter is the only code that
exists on both sides of the fork.

**Deployment.** `Fork.deploy` opens a second channel pair through the same transport
it uses for the crew channel, before the fork. In the child it closes the parent's end
of both pairs, sheds the inherited connections as today, and then, before the crew
member is built, installs a courier on the chronicler with the child's outbound
descriptor. Everything the worker says from that point, from either language, goes to
the parent. In the parent it closes the child's end of both pairs, hands the crew
proxy the journal channel alongside the crew channel, and registers the proxy's
`overhear` handler for read readiness on it. A recruiter trait, `journal`, defaulting
to true, turns the whole arrangement off for a team that does not want it.

**Shedding.** `Fork.shed` closes every channel the shared loop watches and every
deployed member's crew channel (`Fork.py:101-126`). The parent's ends of the journal
channels of earlier members are registered with the loop, so the new child sheds them
with everything else; the crew proxy must also list its journal channel so `shed` sees
it explicitly rather than by accident of registration. The new child's own end is not
registered anywhere and survives.

**Overhearing.** `Crew.overhear` reads what is available, appends it to a per-member
buffer, splits off complete lines, decodes each record, and hands it to the team's
`overhear(crew, record)`. A partial tail waits for the next read. A line that does not
decode is dropped and counted; the count is reported through the parent's own journal
once, not per line. End of stream means the worker is gone, which the crew channel
already reports; the handler returns false and the channel is closed in `bury` and
`dismiss` along with the crew channel. The descriptor cost is one more per member on
each side over sockets, two over pipes.

**Replay.** The default `Team.overhear` replays the record into the parent's own
journal: it resolves the device through a channel of the record's severity and name,
so per-channel and per-severity device installations in the parent are honored, and
calls the record's sink on it with an entry rebuilt from the page and notes. The
parent's `active` and `fatal` flags do not apply: the worker's channel was active, or
the entry would not exist, and a fatal severity has already done its work in the
worker. The three origin fields are written into the notes as `pid`, `seq` and `time`
before replay, so a device downstream can tell a worker's entry from the parent's and
keep its provenance. With a plain console this gives every application built on the
nexus a single, in-order, attributed log on the terminal, with no other change.

Replay needs `journal.entry(page, notes)`, a factory that exists in the pure Python
package but not in the bindings, where `Entry` has no constructor and read-only parts
(`extensions/journal/entry.cc:24-40`). A constructor taking the page and the notes is a
small binding addition and the only one this work requires.

A team that wants the record itself, rather than a replayed entry, overrides
`overhear`; that is the hook a server uses to forward records to its clients.

### Control, later

The journal channel is a socket pair or a pipe pair, so it carries bytes in both
directions, and the worker runs the same selector loop as the parent
(`packages/pyre/nexus/Peer.py:30-60`). A control record sent by the parent, read by a
handler the child registers on its end of the journal channel, can activate or
deactivate a channel in the worker after launch. That is the capability the framework's
`TODO` asks about, and it is the point at which a server-side control surface stops
being limited to the server's own channels. It is a later phase; the design only
requires that nothing in the earlier phases assume the journal channel is one-way.

### The daemon, later still

A daemon is the courier pointed at a Unix domain socket, and a collector that accepts
connections instead of forking them. It earns its cost when participants are not
children of one parent: a hosted deployment with several servers, or command line
tools that should report into a running server. It is not part of this plan beyond the
requirement above that the record be self-describing enough to arrive from a stranger:
the version field, the pid, and the application note in every record.

## Tests

Following the four journal suites and their naming (`tests/journal.pkg`,
`tests/journal.ext`, `tests/journal.api`, `tests/journal.lib`) and the nexus suite
(`tests/pyre.pkg/nexus`):

- `record_encode`, `record_decode`, `record_roundtrip`: the codec, including notes with
  newlines and non-ASCII, and a page that is empty.
- `courier_sanity`, `courier_ship`: install a courier on a pipe, flush entries of every
  severity, read the records back, check the sink, the sequence and the origin fields.
- `courier_mirror`: the mirror sees every entry in order.
- `courier_full`: a pipe nobody drains; the courier must return promptly from every
  flush, count the drops, and report them once the reader catches up.
- `courier_closed`: the far end closes; the courier goes quiet without raising.
- `courier_cxx` in `journal.ext`: a C++ channel, flushed through the bindings, reaches
  the Python courier with its page and notes intact. The first test of the trampoline.
- `staff_overhear`: a two-member team whose task logs on a debug channel; the parent
  replays both members' entries, attributed by pid, in the order they were flushed
  within each member.
- `staff_last_words`: a task that fires a firewall; the parent sees the entry before it
  learns of the casualty.
- `fork_journal_off`: the recruiter trait disabled; no second pair, no handler.

## Change map

`pyre`, package root `packages/`:

- `journal/Record.py` *(new)*: the codec.
- `journal/Courier.py` *(new)*: the device. Imported at the end of `journal/__init__.py`,
  in both branches, after `device` is bound.
- `journal/__init__.py`: export `courier`, `record`, and `entry`; in the bound branch,
  `entry` is `libjournal.Entry`.
- `extensions/journal/entry.cc`: a constructor taking the page and the notes.
- `pyre/nexus/Fork.py`: the `journal` trait; the second pair; the courier installed in
  the child; the journal channel handed to both crew proxies; `shed` lists it.
- `pyre/nexus/Crew.py`: `journal` channel attribute; `overhear`; close in `resign`.
- `pyre/nexus/Pool.py` and `Staff.py`: `overhear(crew, record)` with the replay default;
  the journal channel closed in `bury` and `dismiss`.
- `pyre/http/EventStream.py` and `pyre/http/Server.py`: an optional opening payload that
  the streaming path queues right after the preamble, so a newcomer can be sent history.
- `lib/journal/Courier.h`, `.icc`, `.cc` *(later)*: the C++ twin, registered in
  `extensions/journal/devices.cc` when it exists.
- `doc/design/journal.md`: a section on delivery, once built.

## Sequencing

1. The record and the Python courier, with their tests. No consumer yet; the terminal
   still shows everything.
2. The entry constructor in the bindings and the trampoline test.
3. Collection in the nexus with the replay default. At this point every nexus
   application has an attributed worker log for free, and `qed`'s server device sees
   worker entries with no `qed` change.
4. `qed` builds its far end on top of this; see `qed/doc/console.md`.
5. The C++ courier.
6. Control records to workers, driven by the console's needs.
7. The daemon, when a deployment needs it.

Commit `pyre` and `qed` separately; the `qed` work depends on step 3 being installed.

## Open questions

1. **Does the trampoline hold under a released interpreter lock?** The render pipelines
   flush firewalls from C++ while Python holds the lock today. If the bindings ever
   release it around rendering, a flush from a thread the interpreter does not know
   will fail inside the trampoline. Worth a test in step 2, and a note in the bindings.
2. **Should the parent's replay carry the origin in the notes, or as a channel prefix?**
   The notes keep the channel name intact for filtering, and they are invisible on a
   console at the default decor. A parent that wants to see the pid on its terminal
   raises its decor. The design chooses the notes.
3. **How large is the socket buffer a worker gets?** The default is what the platform
   gives a socket pair; a busy debug channel fills it in a burst. Raising `SO_SNDBUF` on
   the child's end is a one-line policy in `Fork.deploy` once there is a measurement.
4. **What does the courier do with `help`?** Ship it like the rest. Help screens are
   entries too, and a consumer can ignore the sink.


<!-- end of file -->
