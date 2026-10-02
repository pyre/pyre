<!--
-*- markdown -*-
-*- coding: utf-8 -*-

michael a.g. aïvázis <michael.aivazis@para-sim.com>
(c) 1998-2026 all rights reserved
-->

# crew members from a clean process

A design for recruiting the members of a `pyre.nexus` team from a helper process that is
started with the application, instead of forking them from the process that manages the team.
The members talk to their team exactly as they do today; what changes is which process they are
a copy of.

Branch: `forkserver` in `pyre`.

Status: **built**, as `pyre.nexus.recruiters.forkserver` (`nexus/Forkserver.py`) and the shell
`pyre.shells.forkserver` (`shells/Forkserver.py`). The facts about the code that predates it were
read out of the source on 2026-09-28, with the file cited. What was built differs from the design
below in these details:

- The helper is started by `Forkserver.start()`, which an application calls as early as it needs,
  e.g. a server while it activates; otherwise the first recruitment starts it. One helper serves
  every team of the process.
- The helper runs the command line of the application, with the script made absolute when the
  recruiter is imported, followed by `--shell=forkserver --shell.control=<fd>
  --shell.journal=<fd>`; only a pyre application can be re-run this way, so a plain script keeps
  `Fork`.
- The control channel is a unix datagram socket pair, so each request keeps its own descriptors;
  the messages are pickled. The helper's first message describes the interpreter, the
  interpreter options and the script, and the installation of pyre it runs; a mismatch with the
  team's process breaches a firewall.
- The crew class travels pickled, with the file its module was loaded from in the team's
  process. The helper passes it along without loading it; the member loads it after the fork,
  and refuses to serve, with a firewall on the journal it ships to the team, if its module comes
  from another file.
- The helper routes its own journal to the process that started it, which replays the entries
  when it listens on an event loop. Journal controls reach the helper through the new recruiter
  obligation `instruct`, which `Pool.instruct` calls; `Fork` has nothing to pass along.
- `Staff.disband` hands the members it kills to its recruiter to collect, since only the
  recruiter knows whose children they are.


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

A **helper** process is started with the application, before any product is opened, and every
crew member is forked from the helper instead of from the team's process. The helper does
nothing but wait for requests, so it never holds the threads of a library, and every member it
forks is as clean as the application was when it started.

```
team's process ──control channel──> helper           requests, pids, exit reports
      │                                │ fork
      └──crew channel + journal channel┴──> crew member   as today
```

### Starting the helper

The helper is **spawned**, not forked: a fresh interpreter that runs the application's own
driver, with the same command line, in a shell whose only job is to serve recruitment requests.
It therefore loads the same code and the same configuration as the application, and it is clean
whenever it starts, so it can be started lazily, with the first team that recruits, and restarted
if it dies. It costs the start of one interpreter, once; how long that takes for a real
application is to be measured.

The team's process and the helper share a control channel, a socket pair whose far end the helper
receives as an inherited descriptor, named on its command line.

### Recruiting a member

1. The recruiter opens the crew channel, and the journal channel if the team wants one, exactly as
   `Fork.deploy` does today.
2. It sends the helper a recruitment request over the control channel: which crew class to build,
   by its family, and whether a journal channel comes with it. The member's ends of the channels
   travel with the request as ancillary data, the way the spools of rendered tiles travel between
   a member and its team today.
3. The recruiter closes its copies of the member's ends and keeps its own, as it does after a fork
   today.
4. The helper forks. The child closes the control channel, builds the crew member on the
   descriptors it received, installs the journal courier, registers, and runs, which is the child
   branch of `Fork.deploy` without the `team` object.
5. The helper answers with the pid of the child. The answer is a local round trip, so the
   recruiter can wait for it and keep recruitment synchronous, as it is today.

From here on the team and the member exchange tasks, reports, descriptors, and journal entries
directly. The helper is not on the data path.

### Members leaving

A member is the helper's child, so only the helper can harvest its exit status. The helper
reaps every child that exits and reports its pid and status over the control channel.

- The team still learns of a death first from the end of its crew channel, as it does today.
- `Fork.dismiss` keeps its escalation: the team's process can still send `SIGTERM` and `SIGKILL` to
  the member, which belongs to the same user. What changes is how it waits: instead of `waitpid`,
  it waits for the helper's exit report, with the same deadline.
- If the helper dies, the team's process sees the end of the control channel. It starts a new
  helper, and the members already running are unaffected, since they never talk to it; the ones
  that were the old helper's children are reparented to `init`, which reaps them.

### Where it lives

A new recruiter, `pyre.nexus.recruiters.forkserver`, beside `Fork`, selected by configuration.
`Fork` stays as it is, so that the two can be run side by side and measured, and so that an
application that never opens files in buckets pays nothing for the helper. Pools and staffs get
the new recruiter the same way they get `Fork`.


## What a member inherits today, and what it will not

Today a member inherits the state of the team's process at the moment it is recruited. With the
helper, it inherits the state of the application as it was at startup. Whatever the member needs
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

**Set at startup, and therefore present in a helper that starts with the application.** The code
of the application and of its readers, resolved by family; the configuration store, filled from
the configuration files and the command line at startup, from which every component a member builds
takes its settings; the journal settings of the configuration; the environment, from which the
member resolves AWS credentials when a reader names no profile (`qed/readers/access.py:87`); the
working directory, since the workspace and `file:` uris may be relative; the umask. A spawned helper
has all of these only if it is started with the same interpreter path, environment, working
directory, and command line as the application.

**Set after startup, which a member built by the helper would not have.**

1. *The two channel ends, and which crew to build.* Today the child picks up both ends of the fork
   and reads `team.crew`, and whether to route the journal, from the team object. With the helper,
   the recruitment request carries the ends, the family of the crew class, and the journal flag. The
   member no longer needs `Fork.shed`, since the helper holds none of the team's descriptors.
2. *Journal settings changed while the application runs.* A client that switches a channel on
   (`qed/gql/journal/JournalChannelSet.py:50-60`) reaches the members that exist through
   `Pool.instruct`, whose docstring states the assumption this design breaks: "A member forked after
   this inherits the new state, so only the ones already deployed need to be told"
   (`nexus/Pool.py:98-99`). The team keeps the controls it has applied and writes them to the
   journal channel of every member it recruits; `Crew.heed` applies them before the first task
   (`nexus/Crew.py:459-461`).
3. *The descriptor ceiling.* `qed.nexus.Server._widen` raises it when the server activates, before
   the fleet exists, so that every member inherits it. The helper has to be started after that, or
   raise its own.
4. *The environment, changed at run time.* The GDAL reader writes `AWS_PROFILE` and `AWS_REGION` into
   the environment of the server when it opens a raster in a bucket (`qed/readers/native/GDAL.py:
   130-136`), and every member forked since reads them when it resolves credentials. Members built
   by the helper would not. This is a leak today rather than a feature, but removing it changes
   what a reader without an explicit profile resolves to, so it should be settled explicitly: the
   GDAL reader keeps its settings to itself, and a reader that needs a profile names it.
5. *The journal device of the server.* `Server._listen` installs the device that reaches the browser,
   "so the crews inherit it". A member that routes its journal replaces it with the courier, so this
   matters only for a team that does not route, whose members then write to the terminal.

**Hazards that go away.** Descriptors a member inherits today and never uses: cached spools, client
connections, the channels of other teams' members, and the product handles the server holds; the
state of native libraries the server has touched, which is the reason for this design; and a
replacement member inheriting the exception of the failure it replaces (`Fork.py:144-148`).

**Rules the helper has to keep.**

- It never builds a component under a name a member builds. pyre hands back the existing instance
  for a name it knows and ignores the constructor's arguments (`components/Actor.py:127-133`), and
  members build theirs under derived names, `{reader}.crew`, `{reader}.crew.workspace`,
  `{archive}.crew`; a helper that had built one would hand every member a stale instance, and the
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
removes such a member; a member built by a spawned helper would leave on SIGTERM.


## Open questions

- Whether the helper should be spawned with the application's command line, which reproduces the
  configuration exactly, or with a smaller command line naming just the configuration files, which
  would skip whatever the command line does besides configuring.
- What a team does when the helper cannot be restarted: refuse to recruit and say so, or fall back
  to forking itself.
- Whether the macOS workaround in `Fork`, `shield`, is still needed for members forked from the
  helper, which never builds an http client.
- Where in the startup of a server the helper is started: after `Server._widen` raises the
  descriptor ceiling, and before anything mounts an archive or opens a product; the order in which
  a server loads its archives and sources relative to its activation has not been checked.


<!-- end of file -->
