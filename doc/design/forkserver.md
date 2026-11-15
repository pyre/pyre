<!--
-*- markdown -*-
-*- coding: utf-8 -*-

michael a.g. aïvázis <michael.aivazis@para-sim.com>
(c) 1998-2026 all rights reserved
-->

# crew members from a clean process

A design for recruiting the members of a `pyre.nexus` team from a staffing agency, a process that
is started with the application, instead of forking them from the process that manages the team.
The members talk to their team exactly as they do today; what changes is which process they are
a copy of, and how a team learns that a member has left.

Branch: `teardown` in `pyre`.

Status: **built**, on branch `teardown`, as the design below describes. On the same server, the
event loop of the team's process now never waits for a member: a query from outside the browser
was answered within 76 ms throughout a build, and 32 members leaving at first contact were gone
within about a quarter of a second. A first version was built on branch `forkserver`
(pyre#294, merged 2026-09-29) as `pyre.nexus.recruiters.forkserver` and the shell
`pyre.shells.forkserver`. It worked, but it did not look like pyre: loose functions and module
state, a plain class of 340 lines beside the recruiter in one file, a hand-written event loop, and
waits that block the event loop of the team's process. The last of these is what made a server
stall: dismissing a crew took about a tenth of a second per member, on the server's event loop
(16 builders, 1.55 s; 32 members at first contact, 3.2 s; measured with qed on 2026-11-15). The
design below replaces it; the choices behind it were made in a tracker on 2026-11-15, and are
recorded here as the permanent record. The facts about the code that predates both versions were
read out of the source on 2026-09-28, with the file cited.


## The problem

`Fork.deploy` (`nexus/Fork.py`) creates a crew member by forking the process that manages the
team, which for a server is the server itself. The child is a copy of that process as it is at
that moment, including whatever state the libraries it has loaded keep. A fork copies only the
thread that called it, so any library that runs threads of its own is left, in the child, with
its bookkeeping describing threads that do not exist.

HDF5 2.x reads files in S3 through the AWS C libraries, which run an event loop on threads of
their own, started the first time a file in a bucket is opened. In a process that has opened one,
a child that opens a file in a bucket waits forever, at no cpu, on a thread that does not exist on
its side of the fork. HDF5 1.14 read S3 through libcurl, on the calling thread, which is why this
never showed before.

Measured on Linux, with HDF5 2.1, reading a public file in a bucket without credentials, with the
child forked after the parent did one of the following:

| The parent, before the fork | The child |
|-----------------------------|-----------|
| imports `pyre.h5` | opens the file |
| asks whether the library supports S3 | opens the file |
| configures a file access list for S3 | opens the file |
| opens a local file | opens the file |
| opens a file in a bucket | waits forever |

Python itself warns, at the fork of the last case, that the process is multi-threaded. The
reproduction:

```python
import os, time, pyre

uri = "s3://noaa-goes16/ABI-L2-CMIPF/2023/001/00/OR_ABI-L2-CMIPF-M6C01_G16_s20230010000206_e20230010009514_c20230010009594.nc"
grant = {"region": "us-east-1", "access_key": "", "secret_key": "", "token": ""}

def touch():
    return pyre.h5.reader(uri=uri, credentials=grant).read() is not None

touch()                      # the parent opens a file in a bucket
pid = os.fork()
if pid == 0:
    touch()                  # the child never returns from this
    os._exit(0)
```

A server that forks its workers is exposed to this whenever anything in its own process opens a
file in a bucket before a team recruits, or before a team replaces a member it lost. In qed this
happens as soon as a product in a bucket is connected from an archive: the client asks for the
metadata of the product, and the NISAR reader answers by opening the file in the server's process
(`qed.readers.nisar.metadata`). A server in that state was sampled on macOS with eight
`AwsEventLoop` threads beside its main thread, and the member its next team sent to survey the
product never came back. The same
holds for any library that starts threads, e.g. `boto3`'s transfer manager, and
`nexus/Fork.py` already carries one workaround of the kind, `shield`, for the part of macOS that
does not survive a fork.


## The design

A **staffing agency** is started with the application, before any product is opened, and every
crew member is forked by the agency instead of by the team's process. The agency does nothing
but wait for requests, so it never holds the threads of a library, and every member it forks is
as clean as the application was when it started. One agency serves every team of the process.

```
team's process ──control channel──> staffing agency      requests, pids, exit reports
      │                                     │ fork
      └──crew channel + journal channel─────┴──> crew member   as today
```

### The pieces, one class per file

- **`Recruiter`** (`nexus/Recruiter.py`), the protocol, keeps its obligations, with `dismiss`
  taking `crew`, the name its implementations and its caller use. Recruiters are told when a
  member leaves on its own (see *Members leaving*).
- **`Fork`** (`nexus/Fork.py`) forks members from the team's process, as today, and fulfils its
  obligations with `@pyre.export`, like every other component.
- **`Forkserver`** (`nexus/Forkserver.py`), the recruiter that asks the staffing agency for its
  members; it derives from `Fork`, which it shares the crew side of a member with.
- **`StaffingAgency`** (`nexus/StaffingAgency.py`), the component that runs in the agency's
  process: it serves recruitment requests on an event loop of its own, forks the members, and
  reports their exits.
- **`Liaison`** (`nexus/Liaison.py`), the agency's handle in the team's process: spawns the
  agency, holds the team's end of the control channel, sends requests, and turns the agency's
  reports into events on the team's event loop. It is a component with a fixed name, so pyre hands
  every recruiter in the process the same one, which is how the process keeps a single agency.
- **The messages** on the control channel, each a small class in a file of its own: a recruitment
  request, its answer with the pid, a journal control, an exit report, and the agency's greeting
  that describes what it runs.

Nothing lives at the top level of a module. What the first version kept in loose functions moves
to the entity that owns the knowledge:

- the command line that launches the agency, the application's own with the script made
  absolute, is the `Liaison`'s, which is what spawns the agency; it is captured before the working
  directory can change, which is why the first version captured it at import;
- the description of what a process runs (interpreter, installation of pyre, script) belongs to
  the agency, which has to prove it runs what the team's process runs;
- the file a crew class was loaded from travels with the recruitment request;
- the workaround for the macOS proxy lookup that does not survive a fork (`shield`) is a step of
  `Fork`'s configuration, which happens before any member is forked.

The whole life of a team recruited this way, from the start of the agency to the shutdown of
the application, is drawn as a sequence diagram by `etc/introspection/recruiter-lifecycle.py`.

### Starting the agency

The agency is **spawned**, not forked: a fresh interpreter that runs the application's own
driver, with the same command line, in the shell `pyre.shells.forkserver`. It therefore loads the
same code and the same configuration as the application, and it is clean whenever it starts, so
it can be started lazily, with the first team that recruits, and restarted if it dies. An
application may start it early, e.g. a server while it activates.

The shell builds the `StaffingAgency` component and runs its event loop: a pyre dispatcher, like
every other event loop in the framework.

- Requests arrive through `whenReadReady` on the agency's end of the control channel.
- The exits of its children arrive through `whenSignal(SIGCHLD)`, which `pyre.ipc.Signals`
  delivers as an ordinary read event; a member forked from the agency starts without the relay,
  so it never hears its siblings' exits.
- The end of the control channel is how the team's process lets go, so the agency's loop ends
  when it reads the end of the channel; nothing polls.

### The control channel

The control channel is a `pyre.ipc.SocketPair`, a stream, whose far end the agency inherits as a
descriptor named on its command line. Messages are instances of the message classes, carried by
the `Pickler` marshaler, which frames each one with its length. A message that carries
descriptors announces how many follow, and the descriptors ride right after it through
`SocketPair.sendDescriptors`, the way a member's report carries a trailer outside the marshaled
stream. The agency's first message is its greeting; a greeting that does not describe what the
team's process runs breaches a firewall.

### Recruiting a member

1. The recruiter opens the crew channel, and the journal channel if the team wants one, exactly as
   `Fork.deploy` does.
2. It sends a recruitment request: the crew class, pickled, with the file its module was loaded
   from, and whether a journal channel comes with it; the member's ends of the channels follow as
   descriptors.
3. The recruiter closes its copies of the member's ends and keeps its own, as after a fork.
4. The agency forks. The child builds the crew member on the descriptors it received, refuses to
   serve if the crew class's module came from another file, installs the journal courier,
   registers, and runs.
5. The agency answers with the pid of the child. The answer is a local round trip, so recruitment
   stays synchronous.

From here on the team and the member exchange tasks, reports, descriptors, and journal entries
directly. The agency is not on the data path.

### Members leaving

Nothing in the team's process waits for a member to leave. A departure is an event on the team's
event loop, whichever way it comes about.

- **Dismissal.** `Pool.dismiss` tells the member it is dismissed and hands it to the recruiter,
  which returns at once. The recruiter puts the member on its ledger of departures (`Departure`,
  with a deadline one grace period away and the reminders `SIGTERM` and `SIGKILL` still to come),
  collects it on the spot if it is gone already, and keeps one alarm per event loop: the alarm's
  handler reminds every member whose deadline has passed and reschedules itself to the next
  deadline, or ends by returning `None` once the ledger is empty. Nothing is ever cancelled: a
  member that leaves is simply taken off the ledger.
- **Exits.** For `Fork`, a member is a child of the team's process, and its exit arrives through
  `whenSignal(SIGCHLD)`, after which the recruiter reaps it without waiting. For `Forkserver`, a
  member is the agency's child; the agency reaps it and sends an exit report, which arrives
  through `whenReadReady` on the control channel, where the `Liaison` hands it to the recruiters
  that subscribed. Either way, the recruiter takes the member off its ledger and tells the team
  through the hook `departed(crew, status)`, which does nothing by default and which a team may
  override.
- **Deaths.** The team still learns of a death first from the end of its crew channel. It hands
  the member to its recruiter through the new recruiter obligation `bury(team, crew)`, instead of
  reaping it itself: `Pool.bury` no longer calls `waitpid`, since only the recruiter knows whose
  child the member is.
- **Shutdown.** When the application ends, `Staff.disband` tells every member to leave, hands each
  to the recruiter, and then calls the recruiter's `settle`, once, so the exit costs one grace
  period at most, however many members there are. The team's own event loop may have stopped, or
  may be the one that called `disband`, and a loop cannot be nested, so `settle` makes a fresh loop
  of the same kind, watches the departures on it, and stops it once the ledger is empty.
- If the agency dies, the team's process sees the end of the control channel. It starts a new
  agency, and the members already running are unaffected, since they never talk to it; the ones
  that were the old agency's children are reparented to `init`, which reaps them.

### Where it lives

`pyre.nexus.recruiters.forkserver`, beside `Fork`, selected by configuration. `Fork` stays the
default (`Recruiter.pyre_default`), since only a pyre application can be re-run in the agency's
shell; an application that never opens files in buckets pays nothing for the agency. Pools and
staffs get either recruiter the same way.


## States and transitions

What state each party is in, and what moves it to the next one, as built. The sequence diagram
drawn by `etc/introspection/recruiter-lifecycle.py` shows the same transitions in the order they
happen, on the lifeline where each happens.

**The staff** (`Staff`):

| State | Entered by | Left by |
|---|---|---|
| serving | construction; `assign` after a stand-down | `standDown`, `disband` |
| resting | `standDown`: parked members are released, members that finish a task go home, nobody is recruited | `assign` |
| disbanded | `disband`, at exit or by the application | never: `assign` lets its callers down at once |

**A member, as its team sees it** (the team side of `Crew`, on the rosters of `Pool` and `Staff`):

| State | Entered by | Left by |
|---|---|---|
| registered | `Pool.recruit`: the recruiter deployed it | its check-in: `Pool.activate` |
| active | check-in; woken by `assemble` | `submit` with nothing to do: parked; a report: scheduled again |
| idle | parked by `submit`, with a vigil on its channel | `assemble` with work; `_release`; the vigil firing: buried |
| dismissed | `Pool.dismiss`: told to leave, off the rosters, handed to the recruiter | `departed` |
| buried | `Pool.bury`: its channel ended without a dismissal; handed to the recruiter | `departed` |
| gone | `departed(crew, status)`, from the recruiter | |

**A departure** (`Departure`, on the recruiter's ledger):

| State | Entered by | Left by |
|---|---|---|
| leaving | `depart`, from `dismiss` or `bury`: due one grace period later | its exit; its deadline |
| reminded | a deadline passed: `SIGTERM`, and a new deadline | its exit; the next deadline: `SIGKILL` |
| killed | the second deadline passed: `SIGKILL`; only its exit is left | its exit |
| collected | `collect` found its process gone: off the ledger, the team told | |

**The recruiter** (`Fork`, `Forkserver`):

| State | Entered by | Left by |
|---|---|---|
| quiet | construction; the last departure collected | the first departure |
| watching | a departure on an event loop that is not watched yet: it listens for exits (`SIGCHLD` for `Fork`, the liaison's reports for `Forkserver`) and keeps one alarm there | the last departure collected: the exit handler and the alarm end themselves |
| settling | `settle`: a fresh loop of its own, watched the same way | the last departure collected: the loop is stopped and closed |

**The liaison** (`Liaison`, one per process):

| State | Entered by | Left by |
|---|---|---|
| idle | construction; `stop` | `start` |
| spawning | `start` with no agency running: the agency is spawned, its greeting awaited | the greeting: checked, a firewall on a mismatch |
| running | the greeting; listening on every event loop it is started with | the end of the control channel; `stop` |
| lost | the end of the control channel: the agency died; its members keep working | the next `start`: every listening loop forgets the old channels, they are closed, and a new agency is spawned |

**The staffing agency** (`StaffingAgency`, in a process of its own):

| State | Entered by | Left by |
|---|---|---|
| serving | the shell builds it and runs its loop: requests on the control channel, exits by `SIGCHLD` | the end of the control channel |
| gone | its loop stopped, its process exits | |

**A member's process** (`Crew`, on the worker side):

| State | Entered by | Left by |
|---|---|---|
| forked | `enlist` (agency) or `deploy` (`Fork`) | `route`: its journal goes to the team before anything else happens |
| loaded | its class loaded, refusing one from another file | registration with the team |
| working | `register`, then `work`: tasks until there is nothing more to do | the end-of-tasks marker; the end of its channel; a signal |
| exited | `leave`: affairs in order, streams flushed, the process ended without the inherited exit handlers | |


## What a member inherits today, and what it will not

Today a member inherits the state of the team's process at the moment it is recruited. With the
agency, it inherits the state of the application as it was at startup. Whatever the member needs
that is set after startup has to travel with its tasks, or be sent to it when it joins.

The worker side of pyre and qed was read for everything a member takes from the process it was
forked from, on 2026-09-28.

**Already carried by the task, or built by the member, and unaffected.** The member's event loop,
serializer, and timer are its own (`nexus/Peer.py:23-27, 84-93`); the loop that takes tasks and
reports on them uses only its channels and the task (`nexus/Crew.py:338-534`); the journal courier
is built in the member (`Fork.route`); the member leaves through `Fork.leave`, so inherited exit
handlers never run. In qed, the registries of readers and archives are fresh in every member
(`nexus/Crew.py:132-134`); every task carries the recipe of its reader, the credentials, with the
fresh tokens of the archive it came from (`Chore._harvestReader`), the budgets of the caches of its
team, the state of the controllers and the statistics a tile needs, and the location of the
workspace; a listing carries the recipe of its archive; a spool is a new temporary file.

**Set at startup, and therefore present in an agency that starts with the application.** The code
of the application and of its readers, resolved by family; the configuration store, filled from
the configuration files and the command line at startup, from which every component a member builds
takes its settings; the journal settings of the configuration; the environment, from which the
member resolves AWS credentials when a reader names no profile (`qed/readers/access.py:87`); the
working directory, since the workspace and `file:` uris may be relative; the umask. A spawned agency
has all of these only if it is started with the same interpreter path, environment, working
directory, and command line as the application.

**Set after startup, which a member built by the agency would not have.**

1. *The two channel ends, and which crew to build.* Today the child picks up both ends of the fork
   and reads `team.crew`, and whether to route the journal, from the team object. With the agency,
   the recruitment request carries the ends, the family of the crew class, and the journal flag. The
   member no longer needs `Fork.shed`, since the agency holds none of the team's descriptors.
2. *Journal settings changed while the application runs.* A client that switches a channel on
   (`qed/gql/journal/JournalChannelSet.py:50-60`) reaches the members that exist through
   `Pool.instruct`, whose docstring states the assumption this design breaks: "A member forked after
   this inherits the new state, so only the ones already deployed need to be told"
   (`nexus/Pool.py:98-99`). The team keeps the controls it has applied and writes them to the
   journal channel of every member it recruits; `Crew.heed` applies them before the first task
   (`nexus/Crew.py:459-461`).
3. *The descriptor ceiling.* `qed.nexus.Server._widen` raises it when the server activates, before
   the fleet exists, so that every member inherits it. The agency has to be started after that, or
   raise its own.
4. *The environment, changed at run time.* The GDAL reader writes `AWS_PROFILE` and `AWS_REGION` into
   the environment of the server when it opens a raster in a bucket (`qed/readers/native/GDAL.py:
   130-136`), and every member forked since reads them when it resolves credentials. Members built
   by the agency would not. This is a leak today rather than a feature, but removing it changes
   what a reader without an explicit profile resolves to, so it should be settled explicitly: the
   GDAL reader keeps its settings to itself, and a reader that needs a profile names it.
5. *The journal device of the server.* `Server._listen` installs the device that reaches the browser,
   "so the crews inherit it". A member that routes its journal replaces it with the courier, so this
   matters only for a team that does not route, whose members then write to the terminal.

**Hazards that go away.** Descriptors a member inherits today and never uses: cached spools, client
connections, the channels of other teams' members, and the product handles the server holds; the
state of native libraries the server has touched, which is the reason for this design; and a
replacement member inheriting the exception of the failure it replaces (`Fork.py:144-148`).

**Rules the agency has to keep.**

- It never builds a component under a name a member builds. pyre hands back the existing instance
  for a name it knows and ignores the constructor's arguments (`components/Actor.py:127-133`), and
  members build theirs under derived names, `{reader}.crew`, `{reader}.crew.workspace`,
  `{archive}.crew`; an agency that had built one would hand every member a stale instance, and the
  recipe the task carries would be silently ignored.
- It opens no product, mounts no archive, and makes no http request, so that it never holds threads
  of its own; that includes the proxy lookup `Fork.shield` guards against on macOS.
- It holds no descriptor of the application's except its end of the control channel: in particular
  not the listening socket of a server.

**Found along the way.** A member's workspace receives only the path of the application's
workspace; its `caches` setting, the name of the folder under the path, comes from the configuration
of the family, so an application that sets it on its own workspace would find its members building
under a different folder (`qed/nexus/Tile.py:132-133`, `Decimate.py:176-177`). SIGTERM, which
`Fork.dismiss` sends to a member that does not leave, reaches the signal handler the member inherited
from the nexus node, which stops a loop the member does not run, so today it is SIGKILL that
removes such a member; a member built by a spawned agency would leave on SIGTERM.


## Open questions

- Whether a component made by name before the configuration is loaded, as the `Liaison` may be
  when an application starts the agency early, picks up its settings.
- Whether the agency should be spawned with the application's command line, which reproduces the
  configuration exactly, or with a smaller command line naming just the configuration files, which
  would skip whatever the command line does besides configuring.
- What a team does when the agency cannot be restarted: refuse to recruit and say so, or fall back
  to forking itself.
- Whether `shield` is still needed for members forked from the agency, which never builds an http
  client; `Fork` needs it either way.
- Where in the startup of a server the agency is started: after `Server._widen` raises the
  descriptor ceiling, and before anything mounts an archive or opens a product; the order in which
  a server loads its archives and sources relative to its activation has not been checked.


## Blind alleys

Approaches tried and abandoned, with why, and what would justify trying them again.

1. **A wakeup for the first version's hand-written loop** (`7f8d28f47` on `teardown`,
   2026-11-15). The helper reported a member's exit only between its 0.1 s waits, and the team's
   process dismissed members one at a time, waiting for each report, so a stand-down cost about a
   tenth of a second per member. A `SIGCHLD` handler writing into a socket pair registered with
   `signal.set_wakeup_fd` woke the helper at once, and the stand-down of 16 builders fell from
   1.55 s to about 75 ms. It was abandoned because it duplicated `pyre.ipc.Signals`, which already
   delivers signals to an event loop and handles forked children, and because it left dismissal
   waiting on the event loop of the team's process, which is the defect itself. It stays on the
   branch as a record and as the baseline the redesign is measured against, with the test
   `tests/pyre.pkg/nexus/forkserver_standdown.py`. Worth trying again only for a recruiter that
   cannot use a pyre dispatcher.


<!-- end of file -->
