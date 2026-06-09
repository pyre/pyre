# server-sent events over pyre.http

A design for pushing server-originated events to connected HTTP clients, built as
a general `pyre.http` capability (usable by any tool, not just `qed`) with a clear
path toward GraphQL subscriptions.

Branches: `sse` in both `pyre` and `qed`.

Status: **implemented and verified end to end** (2026-06-08). The notes below describe the design
as built; where the build diverged from the original plan, the divergence is called out inline.

## Goal

Let a `pyre.http` server push messages to clients over a long-lived connection,
so that a state change made by one client (or by automation) is reflected in every
other connected client without polling. The motivating case: drive `qed`'s
`window.qed` automation surface and have a second browser, connected to the same
server, update on its own.

Two standing constraints:

1. **The primitive is general.** It lives in `pyre.http` and knows nothing about
   `qed`. Every tool built on `pyre.http` gets it for free.
2. **Client-library assumptions are isolated.** `qed` is migrating off Relay onto
   Houdini. The browser-side wiring must keep the GraphQL-client-specific atom down
   to a single, clearly marked swap point.

Transport decision: **Server-Sent Events (SSE)**, not WebSockets. The push is
strictly server→client; the client→server direction is already served by GraphQL
mutation POSTs. SSE rides plain HTTP, needs no handshake, and the browser
`EventSource` gives reconnection for free. The same `Hub`/`EventStream` pair is the
transport `graphql-sse` needs later (see "Toward GraphQL subscriptions").

## The core insight

For our use case the push needs **no threads, no async, and no out-of-band wakeup**
of the selector loop.

Trace the flow: automation drives `window.qed` → that client POSTs a mutation → the
POST arrives as a read-ready event on *its* channel → `http/Server.py:process`
handles it → the server-side state mutates. Right there, **synchronously inside that
same handler**, we enqueue SSE frames onto the *other* clients' held-open channels.
The broadcast is just more work performed while servicing an event we are already
inside. The single-threaded `SelectorPSL` loop never has to be woken from outside,
because every state change is itself triggered by an incoming request.

This is why the change is a few hundred lines and not a reactor rewrite.

Out-of-band pushes — a timer, a filesystem watcher, a background process reporting
progress — would need a dispatcher alarm or a self-pipe to wake `select()`. That is
a documented extension point (see "Extension points"), not part of this work.

## Architecture

Three additive pieces in `pyre.http`, plus a one-line correctness fix in the `pyre.ipc`
dispatcher (`SelectorPSL`). No change to the socket channel was needed.

### `EventStream(Response)` — the SSE response

A new response type alongside the others in `pyre/http/`. It carries the SSE
headers and owns the wire framing; it has zero application awareness.

- Headers: `Content-Type: text/event-stream`, `Cache-Control: no-cache`,
  `Connection: keep-alive`, and **no `Content-Length`**.
- `alive = True` (the connection is held open).
- `streaming = True` — a new flag on `Response` (default `False`) that the server
  checks to route this response down the streaming path instead of the normal
  render-and-write-once path.
- An optional `topic` (default a single global topic) used by the `Hub` to scope
  delivery. Topics exist from day one because `graphql-sse` maps one subscription
  operation to one topic; a flat global broadcast would have to be refit later.
- `event(data, *, name=None, id=None, retry=None) -> bytes` — formats one SSE
  frame: `id: …\nevent: …\ndata: …\n\n`. Pure transport.

### Protocol version — HTTP/1.1

The `weaver/HTTP.py` renderer negotiates `min(renderer.version, response.version)` for the status
line, and the renderer was capped at `1.0` — so every response went out as `HTTP/1.0` even though
`Response` already declares `1.1`. That cap is wrong for the streaming path: an event stream carries
**no `Content-Length`** and never self-closes, and under HTTP/1.0 `Connection: keep-alive` without a
length is self-contradictory — the only body delimiter 1.0 offers is connection close. HTTP/1.1
makes persistent connections the default and cleanly frames an open-ended stream, so the renderer
now prefers **`1.1`**. The render-once path is unaffected: it always sets `Content-Length`.

`render` and `preamble` share this status-line + negotiation logic, so `render` delegates to
`preamble` for the status line and headers, then appends the blank-line separator and body — the
body is assembled *first* so `Content-Length` is set before the headers go out, leaving the wire
bytes byte-identical to the original render-once output.

### `Hub` — the subscriber registry and outbound pump

Owned by the server (`self.hub`), constructed with the dispatcher reference (the
server already holds `self.dispatcher`, set in `nexus.Server.activate`). The `Hub`
holds subscriber channels keyed by topic and pumps bytes to them without blocking
the loop.

State:

- `_subscribers: dict[topic, set[channel]]`
- `_queues: dict[channel, deque[bytes]]` — per-channel outbound byte queue
- `_armed: set[channel]` — channels currently registered for write-readiness

Interface:

- `subscribe(channel, topic)` — record the channel under the topic, create its
  queue.
- `unsubscribe(channel)` — drop the channel from every topic, its queue, and its
  armed flag. Called on disconnect.
- `publish(event, topic)` — append `event` bytes to every subscribed channel's
  queue and **arm each channel once** (see below).
- `flush(channel)` — the `whenWriteReady` handler. Drains as much of the channel's
  queue as the socket will take, returns `True` while bytes remain (so the
  dispatcher reschedules it), `False` when the queue empties.

### Write-buffered delivery (the "two functions")

Splitting the synchronous write into *assemble + queue* and *flush when writable*
is exactly the `whenWriteReady` split. The mechanics fall out of what
`SelectorPSL` already does:

- `whenWriteReady(channel, call)` (`ipc/SelectorPSL.py:65`) turns on `EVENT_WRITE`
  for the channel's `outbound` fd and registers the handler.
- The watch loop (`ipc/SelectorPSL.py:176-188`) invokes write handlers when the fd
  is writable; a handler that returns truthy is rescheduled, a falsy one is removed
  and the `EVENT_WRITE` bit is cleared — while `EVENT_READ` stays on for disconnect
  detection.
- `dispatch()` (`ipc/SelectorPSL.py:243-249`) already catches `BlockingIOError`
  /`InterruptedError` (reschedule) and `OSError` (drop). So `flush` may attempt a
  partial send naively: a full socket buffer raises `BlockingIOError` and the
  dispatcher simply tries again next time the fd is writable; a broken connection
  raises `OSError` and the handler is dropped.

`flush(channel)`:

1. Peek the head of the queue; attempt a **partial** send.
2. Remove fully-sent bytes; if a frame was partially sent, put the remainder back
   at the head.
3. Return `True` if the queue still has bytes, else remove the channel from
   `_armed` and return `False`.

**Arm once.** `whenWriteReady` appends a *new* handler to the fd's write pile on
every call (`SelectorPSL.py:93`). `publish` must therefore arm a channel only if it
is not already in `_armed`, or duplicate `flush` handlers pile up on one queue. Add
to `_armed` on arm; remove when `flush` drains to empty.

### Partial write on the channel

The original plan called for a new partial-send method on `SocketTCP`. **It turned out to be
unnecessary:** `SocketTCP` derives from `socket.socket`, whose inherited `send(bytes) -> int`
*already is* the non-blocking partial send we want — it writes what it can, returns the count,
and raises `BlockingIOError`/`OSError` exactly as the dispatcher expects. (Contrast `read`/`write`,
which earn their wrappers by transforming behavior — looping `recv`, wrapping `sendall`. `send`
would add nothing.) So `SocketTCP` is untouched. The only requirement is that the connection be
non-blocking on the streaming path, which `Server.stream` arranges with a single
`channel.setblocking(False)`; the normal request path keeps using the blocking `write`.

### Dispatcher fix — arming write from within read

The core insight depends on a read handler (`process`) registering *write* interest on the **same**
fd, synchronously, while it runs. This surfaced a latent bug in `ipc/SelectorPSL.py:watch()` that no
prior client had hit, because none armed a new event on a live fd mid-dispatch.

`watch()` snapshotted the fd's event mask into a local *before* dispatching its handlers, cleared
bits for handler piles that drained, then wrote the local back with `selector.modify`. But when
`process` called `whenWriteReady` during the read dispatch, it set `EVENT_WRITE` in the live mask
table — and the stale local snapshot (read-only) then overwrote the registration, **wiping the
WRITE bit just added**. The flush handler never fired, so the preamble (and every event) sat in the
queue forever. The connection opened and then went silent.

The fix recomputes the mask from the **live** table after dispatch rather than from a pre-dispatch
snapshot: track the bits whose piles drained (`cleared`), then set
`event = masks[fd] & ~cleared`, so interest a handler *added* during dispatch survives. The
registration update is also wrapped to tolerate an fd a handler closed mid-dispatch (the
streaming-channel disconnect path). All `pyre.pkg/ipc` tests still pass. This fix is general — any
handler that arms new interest on its own fd now behaves correctly — not SSE-specific.

### Server wiring

Two touches in `pyre/http/Server.py`, plus an `activate` override:

- `respond()` (line 166) gains a streaming branch: if `response.streaming`, render
  **status line + headers only** (no body, no `Content-Length`), enqueue that
  preamble via `self.hub` for the channel, `self.hub.subscribe(channel, topic)`,
  arm the channel, and return `response.alive`. The preamble and every later event
  go through the same queue+flush path, so nothing on a streaming channel is ever
  written with the blocking `sendall`. This needs a body-less variant of
  `weaver/HTTP.py:render` (its lines 57-59 compute the body and set
  `Content-Length` — exactly what we skip).
- The 0-byte disconnect branch (lines 78-92) gains one line:
  `self.hub.unsubscribe(channel)`. Because an `EventSource` never sends more bytes,
  `process()` fires on a streaming channel **only** at disconnect, so cleanup falls
  out naturally with no extra bookkeeping. The streaming channel is never placed in
  `self.requests` (its GET completed), so the existing `del self.requests[channel]`
  harmlessly hits its `KeyError` guard.

`self.hub` is constructed in an `activate` override: the base `nexus.Server.activate` is where the
dispatcher first becomes available (`self.dispatcher`), so the override chains up and then builds
`self.hub = self.Hub(dispatcher=self.dispatcher)`. `EventStream` and `Hub` are exposed as the class
types `server.eventStream` and `server.Hub` (alongside the existing `server.request`/`server.response`),
and the live instance as `server.hub`.

## qed integration contract

The only place that knows about `qed`. All of it on the `sse` branch of `qed`.

- **`/events` route** in `pkg/ux/Dispatcher.py` → handler returns an `EventStream`,
  which subscribes that browser.
- **One broadcast choke point — `GraphQL.respond` (`pkg/ux/GraphQL.py`), not the Store.** The
  original plan put `hub.publish(...)` at the `Store` mutators. In the code that turned out to be
  the *scattered* option: the `Store` has ~30 mutators with no shared funnel and no hub reference,
  so "publish at the Store mutators" would mean a `publish` call added to every one of them plus
  threading the hub in. The genuinely single seam is `GraphQL.respond`: every state change arrives
  as a GraphQL mutation POST, and they all funnel through that one method, which already holds
  `server` (hence `server.hub`) in its execution context. So publish once there, right after
  `schema.execute`, when the operation is a mutation (`graphql.parse` + `OperationType.MUTATION`)
  and `not result.errors` — queries and failed mutations notify nothing. The payload is minimal —
  a single `{"type": "change"}` frame on the global topic ("something changed, refetch"). Per-topic
  scoping (e.g. one topic per viewport) is deferred to the graphql-sse layer below.
- **Client `liveSync`** — split in two so the GraphQL-client coupling stays isolated:
  `ux/client/automation/eventStream.js` is the portable DOM half (`subscribe(onChange)` opens
  `new EventSource('events')`, calls `onChange` on each message, returns a teardown); it survives
  the Houdini migration untouched. `ux/client/automation/LiveSync.js` is the React + Relay glue
  that supplies the one client-specific atom (see below) and is mounted as `<LiveSync/>` next to the
  existing `<Automation/>`. (The portable file is `eventStream.js`, not `liveSync.js`, because
  `liveSync.js` and `LiveSync.js` collide on a case-insensitive filesystem.)

### Isolating the GraphQL client (Relay → Houdini)

Everything portable — opening the `EventSource`, reconnection, parsing frames,
topic filtering — is plain DOM, lives in `eventStream.js`, and survives the Houdini migration
untouched. The **only** Relay-specific atom is "given an event, re-pull the affected query into the
store." `subscribe(onChange)` takes that as a single injected callback; `LiveSync.js` supplies it,
marked:

```js
// RELAY-SPECIFIC — swap this body for the Houdini equivalent on migration
const refetch = () => fetchQuery(
    environment, stateQuery, {}, { fetchPolicy: "network-only" },
).toPromise()
```

`stateQuery` is the top-level `useFetchQEDQuery` taggedNode, re-exported from
`context/useFetchQED.js`. Refetching it `network-only` writes fresh records into the Relay store,
and every component reading them through `useFragment` re-renders — so the whole UI reconciles from
one refetch.

Deliberately **avoid** Relay's `requestSubscription` / network `subscribe`: that
path is deeply Relay-coupled and would be discarded in the move to Houdini. When
migrating, you replace one function body, not the wiring.

## Toward GraphQL subscriptions

`Hub` + `EventStream` is precisely the transport layer `graphql-sse` expects. The
later subscriptions layer becomes a thin adapter: each subscription operation maps
to a `Hub` topic; values a subscription resolver yields are `publish`-ed as SSE
events on that topic; the client carries them over the same `/events`-style stream.
Keeping `Hub` topic-aware now is what makes that a layer rather than a refit.

## Extension points (not in this work)

- **Out-of-band pushes.** Events not triggered by an incoming request (timers,
  watchers, external processes) need a dispatcher alarm or a self-pipe to wake
  `select()`. `nexus` is the right home when that arrives — see the external
  tile-fetch/prep process work, which is when `nexus` gets poked.
- **Generalizing the queue.** Only streaming responses use the queue+flush path
  here; normal responses keep the synchronous `write`. The same pump could back all
  responses later if it proves worthwhile. Step back to this only if the streaming
  split is clean and stable first.

## Change map

`pyre` (`sse` branch) — package root is `packages/pyre/`:

- `http/EventStream.py` *(new)* — response type (framing, SSE headers, `streaming`, `topic`,
  `event()`).
- `http/Hub.py` *(new)* — subscriber registry + write pump (`subscribe`/`unsubscribe`/`publish`/
  `send`/`flush`, arm-once).
- `http/Server.py` — `activate` override builds `self.hub`; streaming branch + `stream()` in
  `respond()`; `hub.unsubscribe` in the disconnect branch; `eventStream`/`Hub` exposed as types.
- `http/Response.py` — `streaming = False`.
- `weaver/HTTP.py` — body-less `preamble()` rendering; `render()` reuses it for the status line and
  headers; renderer prefers HTTP/1.1 (the SSE keep-alive stream needs 1.1 semantics).
- `ipc/SelectorPSL.py` — `watch()` fix: recompute the fd mask from the live table after dispatch
  (so write interest armed by a read handler survives) + tolerate an fd closed mid-dispatch.
- No `ipc/SocketTCP.py` change — the inherited `socket.send` is already the partial non-blocking
  send. No `http/__init__.py` change — the surface is reached through the `Server` class types, as
  the existing http modules are.

`qed` (`sse` branch):

- `pkg/ux/Dispatcher.py` — `/events` route + `events` handler returning `server.eventStream(...)`.
- `pkg/ux/GraphQL.py` — the single broadcast choke point: `_isMutation` gate + `_notify` →
  `server.hub.publish` after a successful mutation (NOT `Store.py`).
- `ux/client/context/useFetchQED.js` — export the `useFetchQEDQuery` taggedNode for the refetch.
- `ux/client/automation/eventStream.js` *(new)* — portable `subscribe(onChange)`.
- `ux/client/automation/LiveSync.js` *(new)* — React + Relay glue, the one `RELAY-SPECIFIC` refetch.
- `ux/client/qed.js` — mount `<LiveSync/>` next to `<Automation/>`.

Build with `mm` from the `qed` scope. Commit `pyre` and `qed` separately.
