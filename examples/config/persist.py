#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Persist the state of a component in a configuration file, and get it back

The driver keeps the state of a weather station in {station-state.yaml}. The first run seeds
that file from {station.yaml}; every run loads it, builds the station, shows the state it came
up with, changes some of it, and writes it back. Run the script from this directory a few
times: each run picks up where the previous one left off, and the comments and layout of the
file survive every trip

Restoring is plain configuration: {pyre.loadConfiguration} and then build the component.
Persisting is {pyre_persist}, which every component has: it records what was configured, for
the component and everything it references, leaving the rest of the file as it found it.
{pyre.saveConfiguration} does the same for several components at once
"""

# support
import pyre
import pyre.config


# the sensor protocol
class Sensor(pyre.protocol, family="examples.sensors"):
    """
    The requirements of sensors
    """

    @classmethod
    def pyre_default(cls, **kwds):
        """
        The default sensor
        """
        # is a thermometer
        return Thermometer


# a sensor
class Thermometer(pyre.component, family="examples.sensors.thermometer", implements=Sensor):
    """
    A thermometer
    """

    # user configurable state
    gain = pyre.properties.float()
    gain.default = 1.0
    gain.doc = "the amplification of the raw signal"

    calibrated = pyre.properties.bool()
    calibrated.default = False
    calibrated.doc = "whether the sensor has been calibrated"


# the component whose state is persisted
class Station(pyre.component, family="examples.stations.weather"):
    """
    A weather station
    """

    # user configurable state
    label = pyre.properties.str()
    label.default = "station"
    label.doc = "the name of the station"

    elevation = pyre.properties.dimensional()
    elevation.default = "0*m"
    elevation.doc = "the elevation of the station"

    cadence = pyre.properties.int()
    cadence.default = 60
    cadence.doc = "the number of minutes between reports"

    visits = pyre.properties.int()
    visits.default = 0
    visits.doc = "the number of times the station has been serviced"

    crew = pyre.properties.list(schema=pyre.properties.str())
    crew.default = []
    crew.doc = "the people that have serviced the station"

    track = pyre.properties.list(schema=pyre.properties.tuple(schema=pyre.properties.float()))
    track.default = []
    track.doc = "the places the station has been, as (longitude, latitude) pairs"

    archive = pyre.properties.path()
    archive.default = "/tmp"
    archive.doc = "the directory with the reports"

    feed = pyre.properties.uri()
    feed.default = "file:/tmp/feed"
    feed.doc = "the location of the live feed"

    sensor = Sensor()
    sensor.doc = "the instrument"

    readings = pyre.properties.list(schema=pyre.properties.float())
    readings.default = []
    readings.doc = "the readings of the current session; runtime state, so it is not persisted"
    readings.persistent = False


def show(*, station: Station) -> None:
    """
    Print the state of {station}
    """
    # the properties
    print(f"  label: {station.label!r}")
    print(f"  elevation: {station.elevation}")
    print(f"  cadence: {station.cadence}")
    print(f"  visits: {station.visits}")
    print(f"  crew: {list(station.crew)}")
    print(f"  track: {list(station.track)}")
    print(f"  archive: {station.archive}")
    print(f"  feed: {station.feed}")
    # the sensor
    print(f"  sensor: {station.sensor.pyre_spec}")
    print(f"    gain: {station.sensor.gain}")
    print(f"    calibrated: {station.sensor.calibrated}")
    # and the runtime state
    print(f"  readings: {list(station.readings)}")
    # all done
    return


def main() -> int:
    """
    Load the state of the station, change it, and persist it
    """
    # the editor rides on {ruamel.yaml}; if it is not available
    if not pyre.config.yaml.editor.available():
        # there is nothing to show
        print("the editor needs 'ruamel.yaml', which is not importable in this environment")
        # so bail
        return 1

    # the file with the state of the station
    state = pyre.primitives.path("station-state.yaml")
    # on the first run
    if not state.exists():
        # seed it with a copy of the configuration that ships with the example, so the
        # original is left alone
        pyre.config.newYamlEditor(uri="station.yaml").save(uri=state)
        # and say so
        print(f"seeded {state} from station.yaml")

    # restoring is plain configuration: load the file
    pyre.loadConfiguration(str(state))
    # and build the component; its traits pull their values from the configuration store
    station = Station(name="station")
    # show what it came up with
    print("restored:")
    show(station=station)

    # the station gets serviced: another visit
    station.visits += 1
    # by the next member of the crew
    station.crew = list(station.crew) + [f"tech-{station.visits}"]
    # it moves a little to the east
    station.track = list(station.track) + [(-118.06 + station.visits / 100, 34.22)]
    # the first visit
    if station.visits == 1:
        # moves the reports
        station.archive = "/var/tmp/reports"
        # and calibrates the sensor
        station.sensor.calibrated = True
    # the session takes some readings; these are not configuration
    station.readings = [20.5, 21.0]
    # show the new state
    print("serviced:")
    show(station=station)

    # persist it: the station, and the sensor it references, in one call
    station.pyre_persist(uri=state)
    # and show the document
    print(f"persisted in {state}:")
    print(state.open(mode="r", encoding="utf-8").read())
    # all done
    return 0


# main
if __name__ == "__main__":
    # run
    raise SystemExit(main())


# end of file
