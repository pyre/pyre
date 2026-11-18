<!--
-*- markdown -*-
-*- coding: utf-8 -*-

michael a.g. aïvázis <michael.aivazis@para-sim.com>
(c) 1998-2026 all rights reserved
-->

# channels that travel

A design for sending a `pyre.ipc` channel to another process whole, so that no client takes a
channel apart into descriptors and puts it back together on the other side. A channel travels in
a message, over a channel that can carry descriptors, or across an `exec`, on a command line; in
both cases the channel says how it is encoded and rebuilds itself on arrival.

Branch: `ipc` in `pyre`.

Status: **merged** as pyre#411 on 2026-11-16, as the design below describes; agreed on
2026-11-15, from the choices made in a tracker that day. The facts below were read out of the
source on 2026-11-15, at `bba28dae0`, with the file cited.

## What is already true

- **A channel's ends are of two kinds.** `Pipe.inbound` and `outbound` are descriptors;
  `Socket.inbound` and `outbound` are the socket itself (`pyre/ipc/Pipe.py`, `Socket.py`).
  `Channel` does not say which. Clients compensate: `Crew._descriptor` probes with `hasattr`,
  and `tests/pyre.pkg/ipc/selector_close_reuse.py` and `psl_close_reuse.py` test with
  `isinstance`.
- **Channels are taken apart to travel.** `Recruit` collects the descriptors of the member's
  channels, names their kind with `isinstance(channel, socket.socket)`, and records how many
  belong to each; the agency rebuilds them from the numbers (`nexus/messages/Recruit.py`:
  `kind`, `unpack`, `wrap`, `dress`). `Message.send` ships the descriptors after the marshaled
  message, as a second message of one byte (`nexus/messages/Message.py`).
- **Only a unix domain socket carries descriptors.** `SocketPair.sendDescriptors` and
  `recvDescriptors` wrap `SCM_RIGHTS` (`pyre/ipc/SocketPair.py`). The descriptors ride on the
  first byte of the data they are sent with; a read that is not a `recvmsg` drops them.
- **`Pickler` is the only marshaler**, but four components declare a `marshaler` facility
  (`Liaison`, `StaffingAgency`, `Peer`, `Asynchronous`), so others can be configured in.
- **Channels cross an `exec` as numbers.** `Liaison.spawn` puts `control.child.fileno()` and
  `journal.child.fileno()` on the agency's command line and in `pass_fds`; `shells/Forkserver`
  reads them as `int` traits, and `StaffingAgency.serve` assumes they are a `SocketPair`.
- **The standard streams of `shells/Fork` share a descriptor.** `parentChannels` builds
  `stdout` and `stderr` as pipe channels with the same write end (`outfd=stdin[1]`), and
  `childChannels` with the same read end; closing both channels closes it twice. `shells/Daemon`
  installs the child's ends with `os.dup2` on the raw ends.
- **The journal courier writes to a descriptor** (`journal/Courier.py`, and its C++ twin in
  `lib/journal`); `Crew.route` and `StaffingAgency.ship` hand it a channel's writable end.
- **A trait can hold an open resource.** `pyre.properties.istream` coerces a string into an open
  stream and renders it back with `string()` (`pyre/schemata/InputStream.py`).

## The design

**1. A channel's ends are descriptors** (T1). `Socket.inbound` and `outbound` return
`self.fileno()`, and `Channel` says so. The selectors key their tables by the ends; where a
selector picked out the channel of the signal relay among those keys, it now asks the relay for
its descriptor (`Signals.descriptor`).

**2. A channel says how it travels** (T2). Two methods on `Channel`, overridden by each kind:

- `depart()` returns the channel's hints, plain data that name its class by import path and
  carry whatever else it needs, and the descriptors it is made of: one for a `SocketPair`, two
  for a `Pipe`;
- the class method `arrive(hints, descriptors)` rebuilds a channel from them.

The hints name the class by its import path, so the channel kinds of clients travel as well as
the ones in `pyre.ipc`.

A `Manifest` (`pyre/ipc/Manifest.py`) is where a message and its channels meet. A marshaler that
meets a channel while encoding a message declares it to the message's manifest, which keeps its
descriptors and hands back a token, the hints plus the positions of its descriptors, to encode in
the channel's place. On arrival, the marshaler hands each token back, and the manifest rebuilds
the channel from the descriptors that came with the message. A marshaler connects the manifest to
the hook its serializer offers for this (pickle's `persistent_id` and `persistent_load`; json's
`default` and `object_hook`), so no marshaler speaks another's language, and channels know nothing
about marshalers.

**3. The channel a message goes over carries its descriptors** (T3). `Channel.write` takes the
descriptors of the manifest along with the bytes. `SocketPair` sends both with one `sendmsg`,
reads with `recvmsg`, and keeps the descriptors that arrive until the marshaler claims them; the
framing of `Pickler` carries the number of descriptors next to the length, so the marshaler
claims exactly the ones that came with the message. Every other channel refuses to write
descriptors, with an exception raised when a channel is asked to carry descriptors it cannot.

**4. A channel that travels arrives as a copy** (T4). The sender keeps its channel and closes it
when it is done with it, as with any other copy of a descriptor.

**5. A channel crosses an `exec` as a trait** (T5). A new schema, `pyre.schemata.channel`, with
the property `pyre.properties.channel()`, renders a channel as a string of its class, its hints
and its descriptor numbers, `pyre.ipc.SocketPair:SocketPair?family=1&type=1&proto=0#7`, and
coerces such a string back into the channel; the form keeps clear of the braces that
configuration values expand. `pass_fds` keeps the
numbers, so the string that leaves on the command line is the string that arrives.
`Channel.descriptors()` names the descriptors to pass. The `control` and `journal` traits of
`shells/Forkserver` become channels.

**6. Each standard stream is a channel of its own** (T6). `shells/Fork` builds one pipe channel
per stream, each owning its descriptors, and `Channel.install(stream)` makes the right end of a
channel the process's standard `stream`, so `shells/Daemon` stops reaching for numbers. Each
process closes the ends that belong to the other, so a reader sees the end of what the other
side writes, and the application's `main` and `launched` get the three channels by name.

**7. The operations clients now do on raw ends become `Channel` methods** (T7), each returning
the channel: `setBlocking(flag)`, `descriptors()`, `install(stream)`, beside `depart` and `arrive`.
The query `pending()` reports, without waiting, whether a read would find something, bytes or the
end of the stream; an event handler that reads in blocking mode checks it, since the readiness
that woke the handler was recorded at the start of the pass and another reader, e.g. a handler on
an event loop nested in an earlier one, may have taken delivery since (see
`doc/design/recruitment.md`).

**8. The courier comes in two layers** (T8). `journal.Courier` stays the device that writes
records to a descriptor; `journal` sits below pyre and learns nothing about channels.
`pyre.ipc.Courier` is built from a channel and hands the journal device a copy of its writable
end, so the channel and the courier each close their own descriptor, and neither depends on the
other staying alive; `Crew.route` and `StaffingAgency.ship` use it. It is built on demand
(`pyre.ipc.courier(channel=...)`), since `journal` may still be booting when `pyre.ipc` is first
imported.

**9. What goes away** (T9): `Recruit.kind`, `unpack`, `wrap`, `dress`, its `split` and
`transport` fields and its table of transports, since `Recruit` carries the two channels;
`Message.descriptors` and the trailer in `Message.send` and `receive`; `Crew._descriptor`; the
loop of `os.close` in `StaffingAgency.enlist`, which closes the request's channels instead.

**10. A dispatcher says whether a channel is being watched.** `reading(channel)` and
`writing(channel)` report whether a handler is waiting to read from or write to the channel, or
is doing so right now; a running handler counts unless its channel was forgotten, since it would
not be put back. Clients ask the dispatcher about a channel instead of looking its ends up in the
dispatcher's tables.

## Tests

One behavior per driver, under `tests/pyre.pkg/ipc` unless named otherwise:

- the ends of every kind of channel are descriptors (`socketpair.py` and the `close_reuse`
  drivers change to say so);
- a manifest declares and rebuilds a pipe channel and a socket pair, with no transport involved;
- a socket pair carries a message that holds a pipe channel and a socket pair, and both work in
  the receiving process, which holds copies;
- a pipe refuses a message that holds a channel;
- the channel property renders a channel and coerces the string back;
- a channel crosses an `exec` on the command line and works on the other side;
- the standard stream channels of `shells/Fork` own their descriptors;
- the channel courier ships records down a channel;
- each selector says a channel is read or written while a handler waits on it or runs, and not
  once the handler declines or the channel is forgotten (`selector_` and `psl_` `reading`,
  `writing`, `reading_forgotten`);
- the nexus drivers pass unchanged.

## Blind alleys

None yet.


<!-- end of file -->
